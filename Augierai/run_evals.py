import json
from quote_agent import LogisticsQuoteAgent, QuoteRequest

def run_evaluation_suite():
    # Define our test dataset: raw messy inputs mapped to expected outputs/rules
    test_cases = [
        {
            "id": "TC-01 (Standard Valid)",
            "input": """
            Hello, we need a rate for 3 standard 40FT containers of fans from Karachi to Jebel Ali.
            Total weight is 8500 kg.
            """,
            "expected_status": "Approved",
            "mock_extract": {
                "origin": "Karachi",
                "destination": "Jebel Ali",
                "container_count": 3,
                "container_type": "40FT High Cube",
                "items": [{"commodity": "Industrial Fans", "weight_kg": 8500.0}]
            }
        },
        {
            "id": "TC-02 (Invalid Negative Weight)",
            "input": """
            Urgent quote request: Shanghai to Rotterdam. 1 container of parts. 
            Weight is listed as -500 kg (typo in sheet).
            """,
            "expected_status": "Pydantic Validation Error",
            "mock_extract": {
                "origin": "Shanghai",
                "destination": "Rotterdam",
                "container_count": 1,
                "container_type": "20FT Standard",
                "items": [{"commodity": "Parts", "weight_kg": -500.0}] # Typo trigger
            }
        },
        {
            "id": "TC-03 (Weight Limit Exceeded)",
            "input": """
            Please check rate for 1 container from Mumbai to Hamburg.
            Weight of heavy machinery is 28,000 kg.
            """,
            "expected_status": "Rejected (Overweight)",
            "mock_extract": {
                "origin": "Mumbai",
                "destination": "Hamburg",
                "container_count": 1,
                "container_type": "20FT Standard",
                "items": [{"commodity": "Heavy Machinery", "weight_kg": 28000.0}]
            }
        },
        {
            "id": "TC-04 (Invalid Container Count)",
            "input": """
            Need pricing for 0 containers from Karachi to Jebel Ali.
            """,
            "expected_status": "Pydantic Validation Error",
            "mock_extract": {
                "origin": "Karachi",
                "destination": "Jebel Ali",
                "container_count": 0,
                "container_type": "20FT Standard",
                "items": [{"commodity": "Cargo", "weight_kg": 1000.0}]
            }
        }
    ]

    print("==============================================================")
    print("[INFO] LOGISTICS QUOTE AGENT - SYSTEM EVALUATION SUITE")
    print("==============================================================")
    
    passed_evals = 0
    total_evals = len(test_cases)
    
    results_summary = []

    for case in test_cases:
        print(f"\n[RUNNING] {case['id']}...")
        
        # Override the agent's internal parser to use the test case mock extraction
        agent = LogisticsQuoteAgent(use_mock_llm=True)
        agent._call_llm_for_parsing = lambda raw_text, me=case["mock_extract"]: me
        
        output_str = agent.process_shipment_request(case["input"])
        output = json.loads(output_str)
        
        # Determine actual classification state
        if "status" in output and output["status"] == "error":
            actual_status = "Pydantic Validation Error"
            msg = output["message"]
        elif not output["is_approved"]:
            actual_status = "Rejected (Overweight)"
            msg = output["rejection_reason"]
        else:
            actual_status = "Approved"
            msg = f"Quote: ${output['total_quote_usd']}"
            
        is_pass = (actual_status == case["expected_status"])
        if is_pass:
            passed_evals += 1
            status_tag = "[PASS]"
        else:
            status_tag = "[FAIL]"
            
        print(f"{status_tag} Expected: {case['expected_status']} | Actual: {actual_status}")
        results_summary.append({
            "id": case["id"],
            "expected": case["expected_status"],
            "actual": actual_status,
            "pass": is_pass,
            "details": msg
        })
        
    print("\n==============================================================")
    print(f"[SUMMARY] EVALUATION SUMMARY: {passed_evals}/{total_evals} Test Cases Passed")
    print("==============================================================")
    
    # Print clean Markdown Table for documentation
    print("| Test Case ID | Expected Outcome | Actual Outcome | Status | Details |")
    print("|---|---|---|---|---|")
    for r in results_summary:
        status_icon = "PASS" if r["pass"] else "FAIL"
        print(f"| {r['id']} | {r['expected']} | {r['actual']} | {status_icon} | {r['details']} |")
    print("==============================================================")

if __name__ == "__main__":
    run_evaluation_suite()
