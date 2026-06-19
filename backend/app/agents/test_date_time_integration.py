"""
Test script to validate the Date & Time Extraction Agent integration
"""

from app.agents.extraction_agent import extract_complaint_details
from app.agents.validation_agent import validate_case_data
from app.agents.date_time_agent import extract_date_and_time, parse_incident_timeline
import json


def test_date_time_extraction():
    """Test the date_time_agent directly"""
    
    print("\n" + "="*80)
    print("TEST 1: Date & Time Extraction Agent")
    print("="*80)
    
    test_cases = [
        "Stalked on 12 Jan and abused on 14 Jan at 9:30 PM",
        "On 5 June 2026 at around 6:30 PM, my phone was stolen at Trichy Central Bus Stand",
        "Yesterday at 3:45 PM someone stole my wallet near the market",
    ]
    
    for complaint in test_cases:
        print(f"\n📋 Complaint: {complaint}")
        result = extract_date_and_time(complaint)
        print(f"✓ Date: {result['date']}")
        print(f"✓ Time: {result['time']}")
        print(f"✓ All Dates: {result['all_dates']}")
        
        timeline = parse_incident_timeline(complaint)
        print(f"✓ Timeline: {json.dumps(timeline, indent=2)}")


def test_validation():
    """Test the validation agent with date_time extraction"""
    
    print("\n" + "="*80)
    print("TEST 2: Validation Agent with Date/Time Extraction")
    print("="*80)
    
    sample_case = {
        "victim_phone": "Phone: 9876543210",
        "incident_date": "stalked on 12 jan and abused on 14 jan",
        "incident_time": "at 9:30 PM",
        "property_value": "₹15,000",
        "location": "Central Bus Stand"
    }
    
    print(f"\n📋 Input Case Data:")
    print(json.dumps(sample_case, indent=2))
    
    validated = validate_case_data(sample_case)
    
    print(f"\n✓ Validated Case Data:")
    print(json.dumps(validated, indent=2))
    
    # Check results
    assert validated['incident_date'] == "14 January 2026", f"Expected '14 January 2026', got '{validated['incident_date']}'"
    assert validated['incident_time'] == "9:30 PM", f"Expected '9:30 PM', got '{validated['incident_time']}'"
    assert validated['victim_phone'] == "9876543210", f"Expected '9876543210', got '{validated['victim_phone']}'"
    assert validated['property_value'] == "15000", f"Expected '15000', got '{validated['property_value']}'"
    
    print("\n✅ All validation tests passed!")


def test_extraction_integration():
    """Test the extraction agent (requires Qwen)"""
    
    print("\n" + "="*80)
    print("TEST 3: Extraction Agent with Date/Time Integration")
    print("="*80)
    
    complaint = "On 14 January 2026 at 9:30 PM, I was stalked and abused near Othakalmandapam by an unknown person. My phone worth ₹25,000 was stolen."
    
    print(f"\n📋 Complaint: {complaint}")
    
    try:
        result = extract_complaint_details(complaint)
        print(f"\n✓ Extraction Result:")
        
        result_json = json.loads(result)
        print(json.dumps(result_json, indent=2))
        
        # Verify date and time extraction
        assert result_json['incident_date'], "incident_date should not be empty"
        assert result_json['incident_time'], "incident_time should not be empty"
        
        print("\n✅ Extraction test passed!")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Raw response: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("\n🔬 Testing Date & Time Extraction Agent Integration\n")
    
    # Test 1: Direct date_time_agent
    test_date_time_extraction()
    
    # Test 2: Validation agent integration
    test_validation()
    
    # Test 3: Extraction agent integration (requires Qwen)
    print("\n⏳ Running extraction integration test (requires Qwen API)...")
    try:
        test_extraction_integration()
    except Exception as e:
        print(f"⚠️  Skipping extraction integration test: {e}")
    
    print("\n✅ All tests completed!")
