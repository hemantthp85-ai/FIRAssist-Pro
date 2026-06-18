from backend.app.rag.retriever import search_bns
from backend.app.models.qwen_loader import ask_qwen
from backend.app.utils.performance import timed_agent
from backend.app.agents.offence_mapper import (
    OffenceMapper,
    get_recommended_sections
)

import json


@timed_agent("legal_agent.function")
def recommend_sections(fir_data):
    """
    Recommend BNS sections for a case using rule-based mapping and RAG fallback.
    
    Args:
        fir_data: FIR case data dictionary
        
    Returns:
        JSON string with recommended sections and legal analysis
    """

    offences = fir_data.get('possible_offences', [])
    
    print("\n" + "="*80)
    print("LEGAL AGENT - SECTION RECOMMENDATION")
    print("="*80)
    
    print(f"\nDetected Offences: {offences}")
    
    # Step 1: Try rule-based mapping first (high accuracy)
    if offences:
        rule_based_result = get_recommended_sections(offences)
        recommended_sections_from_rules = rule_based_result.get("recommended_sections", [])
        
        print(f"\n✓ Rule-Based Mapping Results:")
        print(f"  Found {rule_based_result['total_sections']} sections with high confidence")
        
        if rule_based_result['has_matches']:
            # We have high-confidence matches, use them
            print(f"  Sections: {rule_based_result['section_numbers']}")
            
            formatted_sections = []
            for section in recommended_sections_from_rules:
                formatted_sections.append({
                    "section": section["section"],
                    "title": section["title"],
                    "reason": f"Matches offence: {', '.join(section['offences'])}",
                    "description": section["description"]
                })
            
            # Generate legal summary
            legal_summary = f"The case involves {len(offences)} offence(s): {', '.join(offences)}. "
            legal_summary += f"Based on rule-based legal mapping, the following {len(formatted_sections)} BNS section(s) apply: "
            
            section_str = ", ".join([f"Section {s['section']} ({s['title']})" for s in formatted_sections])
            legal_summary += f"{section_str}."
            
            return json.dumps({
                "recommended_sections": formatted_sections,
                "legal_summary": legal_summary,
                "mapping_source": "rule_based",
                "confidence": "high"
            })
    
    # Step 2: Fallback to RAG-based retrieval if rules don't match
    print(f"\n⚠️  No high-confidence rule-based matches. Using RAG retrieval as fallback...")
    
    query = f"""
Incident Summary:
{fir_data.get('incident_summary', '')}

Possible Offences:
{fir_data.get('possible_offences', [])}

Location:
{fir_data.get('location', '')}

Accused:
{fir_data.get('accused_name', '')}
"""

    # Retrieve relevant BNS sections from Qdrant
    results = search_bns(query)
    
    print(f"\nRAG Search Results: {len(results)} sections retrieved")

    retrieved_sections = []

    for result in results:
        retrieved_sections.append(
            {
                "section": result.payload.get(
                    "section",
                    "Unknown"
                ),

                "text": result.payload.get(
                    "text",
                    ""
                )[:1500]
            }
        )

    prompt = f"""
You are an Expert Bharatiya Nyaya Sanhita Legal Analysis Agent.

CASE DATA:

{json.dumps(fir_data, indent=2)}

RETRIEVED BNS SECTIONS FROM DATABASE:

{json.dumps(retrieved_sections, indent=2)}

IMPORTANT RULES:

1. Use ONLY retrieved sections from the database above.
2. Never invent or guess section numbers.
3. Match offences with retrieved sections carefully.
4. Prioritize sections that best match the complaint description.
5. Return at least one section if a matching section exists in the retrieved data.
6. Provide reasoning for each selected section.
7. Return valid JSON only.

OUTPUT FORMAT:

{{
    "recommended_sections": [
        {{
            "section": "305",
            "title": "Theft",
            "reason": "The complaint describes theft of property worth ₹25,000."
        }}
    ],

    "legal_summary": "The case primarily involves theft of personal property, which falls under Section 305 of BNS."
}}
"""

    response = ask_qwen(prompt)
    
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    return response


if __name__ == "__main__":

    sample_fir = {

        "incident_summary":
        "My motorcycle was stolen near Coimbatore Bus Stand",

        "possible_offences":
        [
            "Theft"
        ],

        "location":
        "Coimbatore Bus Stand"
    }

    result = recommend_sections(
        sample_fir
    )

    print("\n" + "="*80)
    print("FINAL RESULT")
    print("="*80)
    print(result)
