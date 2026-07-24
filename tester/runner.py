from datetime import datetime, timezone
import numpy as np
from tester.client import APIClient
from tester.tests import run_all_tests

def execute_run():
    client = APIClient(base_url="https://api.quotable.io", timeout=4.0)
    test_results = run_all_tests(client)
    
    passed_count = sum(1 for t in test_results if t["status"] == "PASS")
    failed_count = sum(1 for t in test_results if t["status"] == "FAIL")
    total_tests = len(test_results)
    
    latencies = [t["latency_ms"] for t in test_results]
    
    avg_latency = float(np.mean(latencies)) if latencies else 0.0
    p95_latency = float(np.percentile(latencies, 95)) if latencies else 0.0
    error_rate = float(failed_count / total_tests) if total_tests > 0 else 0.0

    timestamp_iso = datetime.now(timezone.utc).isoformat()

    return {
        "api": "Quotable API",
        "timestamp": timestamp_iso,
        "summary": {
            "passed": passed_count,
            "failed": failed_count,
            "error_rate": round(error_rate, 3),
            "latency_ms_avg": round(avg_latency, 2),
            "latency_ms_p95": round(p95_latency, 2)
        },
        "tests": test_results
    }
