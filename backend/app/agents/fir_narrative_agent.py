"""
FIR Narrative Generator - Professional Police-Style FIR Writing

Converts structured FIR data into formal, professional police-style narratives
suitable for official filing and legal purposes.
"""

import json
from typing import Dict, List
from datetime import datetime
from backend.app.utils.performance import timed_agent


class FIRNarrativeGenerator:
    """Generates professional FIR narratives from structured case data."""
    
    # Narrative templates for different offence types
    TEMPLATES = {
        "theft": {
            "single": """On {date} at approximately {time}, the complainant {victim_name} reported that their {property_type} was stolen from {location}. The complainant stated that the {property_type} was parked/kept at the mentioned location and was found missing upon return. The estimated value of the stolen {property_type} is {property_value}. Based on the complaint and after preliminary investigation, a case under Section 305/304 of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated.""",
            "multiple": """On {primary_date} at approximately {primary_time}, the complainant {victim_name} reported that their {property_type} was stolen from {location}. Prior to this incident on {related_date}, the complainant had reported a related incident of theft. The complainant stated that the {property_type} was parked/kept at the mentioned location and was found missing upon return. The estimated value of the stolen {property_type} is {property_value}. Based on the complaint and after preliminary investigation, a case under Section 305/304 of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated."""
        },
        
        "vehicle_theft": {
            "single": """On {date} at approximately {time}, the complainant {victim_name} reported that his {vehicle_model} bearing registration number {vehicle_number} was stolen from {location}. The complainant stated that the vehicle was parked at the mentioned location and was found missing upon return. The complainant has provided the registration certificate and other required documents. Based on the complaint and after preliminary investigation, a case under Section 305/304 of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated. The vehicle has been entered into the centralized database.""",
            "multiple": """On {primary_date} at approximately {primary_time}, the complainant {victim_name} reported that his {vehicle_model} bearing registration number {vehicle_number} was stolen from {location}. Prior to this incident on {related_date}, the complainant had reported a related incident. The complainant stated that the vehicle was parked at the mentioned location and was found missing upon return. The complainant has provided the registration certificate and other required documents. Based on the complaint and after preliminary investigation, a case under Section 305/304 of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated. The vehicle has been entered into the centralized database."""
        },
        
        "mobile_theft": {
            "single": """On {date} at approximately {time}, the complainant {victim_name} reported that his/her mobile phone valued at {property_value} was stolen from {location}. The complainant stated that the mobile device was forcibly snatched by unknown persons. Based on the complaint and after preliminary investigation, a case under Section 305/304 of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated. The IMEI number and other mobile details have been recorded and circulated to prevent unauthorized use.""",
            "multiple": """On {primary_date} at approximately {primary_time}, the complainant {victim_name} reported that his/her mobile phone valued at {property_value} was stolen from {location}. Prior to this incident on {related_date}, the complainant had reported a related incident. The complainant stated that the mobile device was forcibly snatched by unknown persons. Based on the complaint and after preliminary investigation, a case under Section 305/304 of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated. The IMEI number and other mobile details have been recorded and circulated to prevent unauthorized use."""
        },
        
        "stalking": {
            "single": """On {date} at approximately {time}, the complainant {victim_name} reported that she/he is being stalked and followed by {accused_name} from {location}. The complainant stated that the accused has been persistently following, contacting, and attempting to engage in unwanted interaction causing fear and annoyance. The complainant further stated that this conduct has been repetitive and is causing mental trauma. Based on the complaint and after preliminary investigation, a case under Section 354D of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated.""",
            "multiple": """On {primary_date} at approximately {primary_time}, the complainant {victim_name} reported that she/he is being stalked and followed by {accused_name} from {location}. The complainant stated that the accused has been persistently following, contacting, and attempting to engage in unwanted interaction causing fear and annoyance since {related_date}. The conduct has been repetitive and escalating, causing mental trauma. Based on the complaint and after preliminary investigation, a case under Section 354D of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated."""
        },
        
        "sexual_harassment": {
            "single": """On {date} at approximately {time}, the complainant {victim_name} reported that she/he has been subjected to sexual harassment by {accused_name} at {location}. The complainant stated that unwanted sexual conduct and advances have been made with intent to cause humiliation and harm. The complainant reported the following details: {incident_summary}. Based on the complaint and after preliminary investigation, a case under Sections 354/354A of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated. The victim has been informed about counseling and support services available.""",
            "multiple": """On {primary_date} at approximately {primary_time}, the complainant {victim_name} reported that she/he has been subjected to repeated sexual harassment by {accused_name} at {location}. The first incident occurred on {related_date}, and subsequent incidents have followed. The complainant reported unwanted sexual conduct and advances with intent to cause humiliation and harm. Details: {incident_summary}. Based on the complaint and after preliminary investigation, a case under Sections 354/354A of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated. The victim has been informed about counseling and support services available."""
        },
        
        "assault": {
            "single": """On {date} at approximately {time}, the complainant {victim_name} reported that he/she was assaulted by {accused_name} at {location}. The complainant stated that he/she was subjected to physical violence and use of criminal force. The nature of injuries sustained: {incident_summary}. Medical examination of the complainant has been conducted. Based on the complaint and after preliminary investigation, a case under Sections 351/352 of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated.""",
            "multiple": """On {primary_date} at approximately {primary_time}, the complainant {victim_name} reported that he/she was assaulted by {accused_name} at {location}. A prior incident of assault occurred on {related_date}. The complainant stated that he/she was subjected to physical violence and use of criminal force on multiple occasions. Nature of injuries: {incident_summary}. Medical examination of the complainant has been conducted. Based on the complaint and after preliminary investigation, a case under Sections 351/352 of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated."""
        },
        
        "cyber_fraud": {
            "single": """On {date} at approximately {time}, the complainant {victim_name} reported that he/she has been defrauded through online/digital means. The complainant stated that an amount of {property_value} was fraudulently transferred from their bank account/digital wallet through {incident_summary}. The transaction details and communication records have been provided by the complainant. Based on the complaint and after preliminary investigation, a case under Sections 419/420 of the Bharatiya Nyaya Sanhita (BNS), 2023 and relevant provisions of the Information Technology Act has been registered and investigation is initiated. Cyber cell has been intimated for tracing the fraudulent transactions.""",
            "multiple": """On {primary_date} at approximately {primary_time}, the complainant {victim_name} reported that he/she has been subjected to cyber fraud on multiple occasions. Prior incident occurred on {related_date}. The complainant stated that a total amount of {property_value} was fraudulently transferred through {incident_summary}. The complainant has provided transaction details, communication records, and bank statements. Based on the complaint and after preliminary investigation, a case under Sections 419/420 of the Bharatiya Nyaya Sanhita (BNS), 2023 and relevant provisions of the Information Technology Act has been registered and investigation is initiated. Cyber cell has been intimated for tracing the fraudulent transactions."""
        },
        
        "missing_person": {
            "single": """On {date} at approximately {time}, the complainant {victim_name} reported that {accused_name} is missing from {location} since {date}. The missing person is described as {incident_summary}. The last known location and relevant identification details have been provided. Based on the complaint, a case under relevant sections of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and search operations are initiated. The details have been circulated to all police stations and concerned agencies for locating the missing person.""",
            "multiple": """On {primary_date} at approximately {primary_time}, the complainant {victim_name} reported that {accused_name} is missing from {location}. A prior missing report was filed on {related_date}. The missing person is described as {incident_summary}. Last known location and identification details have been provided. Based on the complaint, a case under relevant sections of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and intensive search operations are initiated. The details have been circulated to all police stations and concerned agencies for locating the missing person."""
        },
        
        "attempt_offence": {
            "single": """On {date} at approximately {time}, the complainant {victim_name} reported that an attempt was made to commit a crime against him/her at {location}. The complainant stated that {accused_name} attempted to {incident_summary}. Due to the intervention/alertness of the complainant, the attempt could not be completed. Based on the complaint and after preliminary investigation, a case under relevant sections of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated.""",
            "multiple": """On {primary_date} at approximately {primary_time}, the complainant {victim_name} reported that multiple attempts have been made to commit crimes against him/her at {location}. A prior attempt occurred on {related_date}. The complainant stated that {accused_name} have repeatedly attempted to {incident_summary}. Based on the complaint and after preliminary investigation, a case under relevant sections of the Bharatiya Nyaya Sanhita (BNS), 2023 has been registered and investigation is initiated. Enhanced surveillance and security measures have been recommended."""
        },
        
        "default": {
            "single": """On {date} at approximately {time}, the complainant {victim_name} reported an incident at {location}. The complainant stated that {incident_summary}. Based on the complaint and after preliminary investigation, a case has been registered and investigation is initiated.""",
            "multiple": """On {primary_date} at approximately {primary_time}, the complainant {victim_name} reported an incident at {location}. A related incident was reported on {related_date}. The complainant stated that {incident_summary}. Based on the complaint and after preliminary investigation, a case has been registered and investigation is initiated."""
        }
    }
    
    @classmethod
    def get_offence_category(cls, offences: List[str]) -> str:
        """
        Determine the primary offence category from the list of offences.
        
        Args:
            offences: List of offence types
            
        Returns:
            The primary offence category
        """
        
        if not offences:
            return "default"
        
        # Map offences to categories
        offence_map = {
            "vehicle theft": "vehicle_theft",
            "vehicle_theft": "vehicle_theft",
            "bike theft": "vehicle_theft",
            "car theft": "vehicle_theft",
            "mobile theft": "mobile_theft",
            "phone theft": "mobile_theft",
            "theft": "theft",
            "stalking": "stalking",
            "sexual harassment": "sexual_harassment",
            "harassment": "sexual_harassment",
            "assault": "assault",
            "attack": "assault",
            "cyber fraud": "cyber_fraud",
            "online fraud": "cyber_fraud",
            "upi fraud": "cyber_fraud",
            "missing person": "missing_person",
            "missing": "missing_person",
            "attempt": "attempt_offence",
        }
        
        primary_offence = offences[0].lower()
        
        # Check for direct match
        if primary_offence in offence_map:
            return offence_map[primary_offence]
        
        # Check for keyword in offence
        for keyword, category in offence_map.items():
            if keyword in primary_offence:
                return category
        
        return "default"
    
    @classmethod
    def format_date_time(cls, date_str: str, time_str: str) -> tuple:
        """
        Format date and time for narrative.
        
        Args:
            date_str: Date string (e.g., "14 January 2026")
            time_str: Time string (e.g., "6:30 PM")
            
        Returns:
            Tuple of (formatted_date, formatted_time)
        """
        
        # Date is already formatted properly
        date = date_str if date_str else "the date"
        
        # Time formatting
        if time_str:
            time = time_str
        else:
            time = "the time"
        
        return date, time
    
    @classmethod
    def generate_narrative(cls, fir_data: Dict) -> Dict:
        """
        Generate a professional FIR narrative from structured data.
        
        Args:
            fir_data: Dictionary containing FIR information
            
        Returns:
            Dictionary with 'narrative' key containing the generated narrative
        """
        
        # Extract key information
        offences = fir_data.get('possible_offences', [])
        offence_category = cls.get_offence_category(offences)
        
        victim_name = fir_data.get('victim_name', 'the complainant')
        accused_name = fir_data.get('accused_name', '')
        accused_name_display = accused_name if accused_name else 'unknown persons'
        
        incident_summary = fir_data.get('incident_summary', 'an incident')
        location = fir_data.get('location', 'the reported location')
        incident_date = fir_data.get('incident_date', '')
        incident_time = fir_data.get('incident_time', '')
        property_type = fir_data.get('property_type', 'property')
        property_value = fir_data.get('property_value', '')
        vehicle_model = fir_data.get('vehicle_model', '')
        vehicle_number = fir_data.get('vehicle_number', '')
        amount_lost = fir_data.get('amount_lost', property_value)
        
        # Format amount with currency symbol if present
        if amount_lost and not amount_lost.startswith('₹'):
            amount_lost = f"₹{amount_lost}"
        
        # Get template
        template_set = cls.TEMPLATES.get(offence_category, cls.TEMPLATES['default'])
        
        # Determine if single or multiple incidents
        is_multiple = len(fir_data.get('related_incidents', [])) > 0
        template_key = "multiple" if is_multiple else "single"
        template = template_set.get(template_key, template_set['single'])
        
        # Format date and time
        date_formatted, time_formatted = cls.format_date_time(incident_date, incident_time)
        
        # Build related incident info if exists
        related_date = ""
        if is_multiple and fir_data.get('related_incidents'):
            related_incident = fir_data['related_incidents'][0]
            related_date = related_incident.get('date', 'an earlier date')
        
        # Format property value with currency
        if property_value and not property_value.startswith('₹'):
            property_value = f"₹{property_value}"
        
        # Replace placeholders in template
        try:
            narrative = template.format(
                victim_name=victim_name,
                accused_name=accused_name_display,
                date=date_formatted,
                time=time_formatted,
                primary_date=date_formatted,
                primary_time=time_formatted,
                related_date=related_date,
                incident_summary=incident_summary,
                location=location,
                property_type=property_type,
                property_value=property_value or amount_lost or "undisclosed",
                vehicle_model=vehicle_model,
                vehicle_number=vehicle_number,
                amount_lost=amount_lost or property_value or "undisclosed"
            )
        except KeyError as e:
            # Fallback if placeholders don't match
            narrative = f"On {date_formatted} at approximately {time_formatted}, the complainant {victim_name} reported an incident at {location}. {incident_summary}"
        
        return {
            "narrative": narrative,
            "offence_category": offence_category,
            "primary_offences": offences[:1] if offences else ["Unknown"],
            "is_multiple_incidents": is_multiple
        }


# Convenience function
@timed_agent("fir_narrative_agent.function")
def generate_fir_narrative(fir_data: Dict) -> Dict:
    """
    Generate a professional FIR narrative.
    
    Args:
        fir_data: Dictionary containing FIR information
        
    Returns:
        Dictionary with narrative and metadata
    """
    return FIRNarrativeGenerator.generate_narrative(fir_data)


if __name__ == "__main__":
    
    # Test cases
    print("\n" + "="*80)
    print("FIR NARRATIVE GENERATOR - TEST SUITE")
    print("="*80)
    
    # Test 1: Vehicle Theft
    print("\n" + "─"*80)
    print("TEST 1: Vehicle Theft")
    print("─"*80)
    
    test_data_1 = {
        "victim_name": "Hemantth",
        "incident_summary": "Bike theft near Coimbatore Bus Stand",
        "incident_date": "14 January 2026",
        "incident_time": "6:30 PM",
        "location": "Coimbatore Bus Stand",
        "vehicle_model": "Honda Activa",
        "vehicle_number": "TN38AB1234",
        "possible_offences": ["Vehicle Theft"]
    }
    
    result = generate_fir_narrative(test_data_1)
    print(f"\n📋 Input FIR Data:")
    print(json.dumps(test_data_1, indent=2))
    print(f"\n📜 Generated Narrative:\n{result['narrative']}")
    
    # Test 2: Stalking with Multiple Incidents
    print("\n" + "─"*80)
    print("TEST 2: Stalking (Multiple Incidents)")
    print("─"*80)
    
    test_data_2 = {
        "victim_name": "Priya",
        "accused_name": "Rajesh Kumar",
        "incident_summary": "Persistent stalking and unwanted contact",
        "incident_date": "14 January 2026",
        "incident_time": "9:30 PM",
        "location": "Chennai City Center",
        "possible_offences": ["Stalking"],
        "related_incidents": [
            {
                "date": "12 January 2026",
                "time": "",
                "description": ""
            }
        ]
    }
    
    result = generate_fir_narrative(test_data_2)
    print(f"\n📋 Input FIR Data:")
    print(json.dumps(test_data_2, indent=2))
    print(f"\n📜 Generated Narrative:\n{result['narrative']}")
    
    # Test 3: Cyber Fraud
    print("\n" + "─"*80)
    print("TEST 3: Cyber Fraud")
    print("─"*80)
    
    test_data_3 = {
        "victim_name": "Arjun Desai",
        "incident_summary": "Fraudulent UPI transaction via fake mobile app",
        "incident_date": "15 January 2026",
        "incident_time": "2:00 PM",
        "location": "Online",
        "property_value": "50000",
        "possible_offences": ["Cyber Fraud"]
    }
    
    result = generate_fir_narrative(test_data_3)
    print(f"\n📋 Input FIR Data:")
    print(json.dumps(test_data_3, indent=2))
    print(f"\n📜 Generated Narrative:\n{result['narrative']}")
    
    # Test 4: Sexual Harassment
    print("\n" + "─"*80)
    print("TEST 4: Sexual Harassment")
    print("─"*80)
    
    test_data_4 = {
        "victim_name": "Sneha Sharma",
        "accused_name": "Office Senior",
        "incident_summary": "Unwanted physical contact and inappropriate remarks at workplace",
        "incident_date": "13 January 2026",
        "incident_time": "3:30 PM",
        "location": "Office Building",
        "possible_offences": ["Sexual Harassment"]
    }
    
    result = generate_fir_narrative(test_data_4)
    print(f"\n📋 Input FIR Data:")
    print(json.dumps(test_data_4, indent=2))
    print(f"\n📜 Generated Narrative:\n{result['narrative']}")
    
    # Test 5: Mobile Theft
    print("\n" + "─"*80)
    print("TEST 5: Mobile Theft")
    print("─"*80)
    
    test_data_5 = {
        "victim_name": "Ravi Kumar",
        "incident_summary": "Mobile phone snatched by unknown persons",
        "incident_date": "14 January 2026",
        "incident_time": "7:45 PM",
        "location": "Central Market",
        "property_type": "Samsung Galaxy A50",
        "property_value": "18000",
        "possible_offences": ["Mobile Theft"]
    }
    
    result = generate_fir_narrative(test_data_5)
    print(f"\n📋 Input FIR Data:")
    print(json.dumps(test_data_5, indent=2))
    print(f"\n📜 Generated Narrative:\n{result['narrative']}")
    
    # Test 6: Assault
    print("\n" + "─"*80)
    print("TEST 6: Assault")
    print("─"*80)
    
    test_data_6 = {
        "victim_name": "Vikram Singh",
        "accused_name": "Unknown",
        "incident_summary": "Physical assault with injuries to head and face",
        "incident_date": "14 January 2026",
        "incident_time": "10:00 PM",
        "location": "Street near Railway Station",
        "possible_offences": ["Assault"]
    }
    
    result = generate_fir_narrative(test_data_6)
    print(f"\n📋 Input FIR Data:")
    print(json.dumps(test_data_6, indent=2))
    print(f"\n📜 Generated Narrative:\n{result['narrative']}")
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80)
