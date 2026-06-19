from app.agents.fir_narrative_agent import FIRNarrativeGenerator
import json


from app.utils.performance import timed_agent


@timed_agent("fir_writer_agent.function")
def generate_fir_narrative(fir_data):
    """
    Generate a professional FIR narrative from structured FIR data.
    Uses template-based generation for consistency and accuracy.
    
    Args:
        fir_data: Dictionary with FIR information
        
    Returns:
        Dictionary with narrative and metadata
    """
    
    # Extract information from fir_data in various formats
    # Support both old and new data structures
    
    # Build standardized data for narrative generator
    processed_data = {
        'victim_name': fir_data.get('Complainant', {}).get('Name') or 
                      fir_data.get('victim_name', 'the complainant'),
        'accused_name': fir_data.get('Accused', {}).get('Name') or 
                       fir_data.get('accused_name', ''),
        'incident_summary': fir_data.get('Incident', {}).get('Summary') or 
                           fir_data.get('incident_summary', ''),
        'incident_date': fir_data.get('Incident', {}).get('Date') or 
                        fir_data.get('incident_date', ''),
        'incident_time': fir_data.get('Incident', {}).get('Time') or 
                        fir_data.get('incident_time', ''),
        'location': fir_data.get('Incident', {}).get('Location') or 
                   fir_data.get('location', ''),
        'vehicle_model': fir_data.get('Property', {}).get('Model') or 
                        fir_data.get('vehicle_model', ''),
        'vehicle_number': fir_data.get('Property', {}).get('RegistrationNumber') or 
                         fir_data.get('vehicle_number', ''),
        'property_type': fir_data.get('Property', {}).get('Type') or 
                        fir_data.get('property_type', ''),
        'property_value': str(fir_data.get('Property', {}).get('EstimatedValue') or 
                             fir_data.get('property_value', '')),
        'possible_offences': fir_data.get('Offences', []) or fir_data.get('possible_offences', []),
        'related_incidents': fir_data.get('related_incidents', [])
    }
    
    # Generate narrative using template-based generator
    result = FIRNarrativeGenerator.generate_narrative(processed_data)
    
    return result['narrative']


if __name__ == "__main__":

    sample_fir = {

        "FIR_Number": "AUTO-GENERATED",

        "Complainant": {
            "Name": "Hemantth",
            "Phone": "8610595920"
        },

        "Incident": {
            "Summary": "Mobile phone theft",
            "Date": "5 June 2026",
            "Time": "6:30 PM",
            "Location": "Trichy Bus Stand"
        },

        "Property": {
            "Type": "Mobile Phone",
            "Value": "15000"
        },

        "Possible_Offences": [
            "Theft"
        ]
    }

    result = generate_fir_narrative(
        sample_fir
    )

    print(result)
