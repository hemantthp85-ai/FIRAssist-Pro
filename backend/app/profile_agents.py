import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import asyncio
import json
import time
import re
from backend.app.agents.extraction_agent import extract_complaint_details
from backend.app.agents.validation_agent import validate_case_data
from backend.app.orchestrator.case_orchestrator import run_case_orchestration_async
from backend.app.utils.performance import get_slowest_agents, _timings, _cache

def clean_json_str(s):
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1:
        s = s[start:end+1]
    s = re.sub(r',\s*}', '}', s)
    s = re.sub(r',\s*\]', ']', s)
    return s

async def run_profiling():
    complaint = """
    On 5 June 2026 at around 6:30 PM, my mobile phone worth Rs. 15,000 was stolen 
    at Trichy Central Bus Stand. I was waiting for the bus to Madurai when someone 
    took it from my pocket. Complainant: Hemantth, phone: 8610595920.
    """
    
    print("\n==================================================")
    # Clear memory cache to measure cold start vs warm cache correctly
    _cache.clear()
    _timings.clear()
    print("PHASE 1: RUNNING AGENTS (COLD START - UNCACHED)")
    print("==================================================")
    
    start_time = time.perf_counter()
    
    # 1. Extraction Agent
    print("Running Extraction Agent...")
    t0 = time.perf_counter()
    extracted = extract_complaint_details(complaint)
    d_extract = time.perf_counter() - t0
    print(f"Extraction took {d_extract:.2f} seconds.")
    
    # 2. Validation Agent
    print("Running Validation Agent...")
    t0 = time.perf_counter()
    try:
        extracted_json = json.loads(clean_json_str(extracted))
    except Exception as e:
        print(f"Extraction JSON parse failed: {e}. Using fallback...")
        extracted_json = {
            "victim_name": "Hemantth",
            "victim_phone": "8610595920",
            "possible_offences": ["Theft"],
            "property_value": "15000",
            "incident_summary": "Mobile phone theft",
            "location": "Trichy Bus Stand",
            "incident_date": "5 June 2026",
            "incident_time": "6:30 PM"
        }
        
    validated_json = validate_case_data(extracted_json)
    d_validate = time.perf_counter() - t0
    print(f"Validation took {d_validate:.2f} seconds.")
    
    # 3. Case Orchestrator (runs remaining 10 agents)
    print("Running Case Orchestrator (Concurrent Agents)...")
    t0 = time.perf_counter()
    dashboard = await run_case_orchestration_async(validated_json)
    d_orchestrator = time.perf_counter() - t0
    print(f"Orchestrator took {d_orchestrator:.2f} seconds.")
    
    cold_duration = time.perf_counter() - start_time
    print(f"\n>>> Total Cold Start Duration: {cold_duration:.2f} seconds <<<")
    
    # Print timings recorded in performance utility
    print("\nRecorded Agent Durations:")
    slowest = get_slowest_agents(limit=20)
    for s in slowest:
        print(f"  - {s['agent']}: {s['total_ms']:.2f} ms ({s['calls']} calls)")
        
    print("\n==================================================")
    print("PHASE 2: RUNNING AGENTS (WARM RUN - CACHED)")
    print("==================================================")
    
    start_time = time.perf_counter()
    
    # 1. Extraction Agent (Cached)
    print("Running Extraction Agent...")
    t0 = time.perf_counter()
    extracted_cached = extract_complaint_details(complaint)
    d_extract_cached = time.perf_counter() - t0
    print(f"Extraction took {d_extract_cached:.4f} seconds.")
    
    # 2. Validation Agent (Cached)
    print("Running Validation Agent...")
    t0 = time.perf_counter()
    try:
        extracted_json_cached = json.loads(clean_json_str(extracted_cached))
    except Exception:
        extracted_json_cached = extracted_json
    validated_json_cached = validate_case_data(extracted_json_cached)
    d_validate_cached = time.perf_counter() - t0
    print(f"Validation took {d_validate_cached:.4f} seconds.")
    
    # 3. Case Orchestrator (Cached)
    print("Running Case Orchestrator (Concurrent Agents)...")
    t0 = time.perf_counter()
    dashboard_cached = await run_case_orchestration_async(validated_json_cached)
    d_orchestrator_cached = time.perf_counter() - t0
    print(f"Orchestrator took {d_orchestrator_cached:.4f} seconds.")
    
    warm_duration = time.perf_counter() - start_time
    print(f"\n>>> Total Warm Run Duration: {warm_duration:.4f} seconds <<<")
    
    # Print comparison report
    print("\n==================================================")
    print("PERFORMANCE BREAKDOWN REPORT")
    print("==================================================")
    print(f"{'Agent / Step':<30} | {'Cold Run (s)':<15} | {'Warm Run (s)':<15} | {'Speedup':<10}")
    print("-" * 80)
    print(f"{'Extraction Agent':<30} | {d_extract:<15.3f} | {d_extract_cached:<15.4f} | {d_extract / (d_extract_cached or 0.001):.1f}x")
    print(f"{'Validation Agent':<30} | {d_validate:<15.3f} | {d_validate_cached:<15.4f} | {d_validate / (d_validate_cached or 0.001):.1f}x")
    print(f"{'Orchestrator (10 Agents)':<30} | {d_orchestrator:<15.3f} | {d_orchestrator_cached:<15.4f} | {d_orchestrator / (d_orchestrator_cached or 0.001):.1f}x")
    print("-" * 80)
    print(f"{'TOTAL SYSTEM LATENCY':<30} | {cold_duration:<15.3f} | {warm_duration:<15.4f} | {cold_duration / (warm_duration or 0.001):.1f}x")

if __name__ == "__main__":
    asyncio.run(run_profiling())
