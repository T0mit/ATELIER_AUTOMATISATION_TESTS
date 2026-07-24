def run_all_tests(client):
    results = []

    # Test 1 : GET /random returns 200 OK and valid JSON
    res1 = client.request("GET", "/random")
    t1_pass = (res1["status_code"] == 200 and 
               res1["headers"].get("content-type", "").startswith("application/json"))
    results.append({
        "name": "GET /random - Status 200 & Content-Type JSON",
        "status": "PASS" if t1_pass else "FAIL",
        "latency_ms": res1["latency_ms"],
        "details": f"Status: {res1['status_code']}" if t1_pass else f"Error/Status: {res1.get('error') or res1['status_code']}"
    })

    # Test 2 : GET /random - Schema validation
    res2 = client.request("GET", "/random")
    data = res2.get("json") or {}
    required_fields = ["_id", "content", "author", "tags", "length"]
    has_fields = all(field in data for field in required_fields)
    valid_types = (
        isinstance(data.get("_id"), str) and
        isinstance(data.get("content"), str) and
        isinstance(data.get("author"), str) and
        isinstance(data.get("tags"), list) and
        isinstance(data.get("length"), int)
    ) if has_fields else False

    results.append({
        "name": "GET /random - Schema & Types check",
        "status": "PASS" if (has_fields and valid_types) else "FAIL",
        "latency_ms": res2["latency_ms"],
        "details": "All fields and types valid" if (has_fields and valid_types) else "Missing fields or bad types"
    })

    # Test 3 : GET /quotes - Pagination list check
    res3 = client.request("GET", "/quotes")
    qdata = res3.get("json") or {}
    t3_pass = (res3["status_code"] == 200 and 
               isinstance(qdata.get("results"), list) and 
               isinstance(qdata.get("count"), int))
    results.append({
        "name": "GET /quotes - Valid paginated list",
        "status": "PASS" if t3_pass else "FAIL",
        "latency_ms": res3["latency_ms"],
        "details": f"Retrieved {qdata.get('count', 0)} quotes" if t3_pass else "Invalid structure"
    })

    # Test 4 : GET /quotes?author=albert-einstein - Filter by author
    res4 = client.request("GET", "/quotes", params={"author": "albert-einstein"})
    adata = res4.get("json") or {}
    results_list = adata.get("results", [])
    t4_pass = res4["status_code"] == 200 and len(results_list) > 0 and all("Einstein" in q.get("author", "") for q in results_list)
    results.append({
        "name": "GET /quotes?author=albert-einstein - Filter test",
        "status": "PASS" if t4_pass else "FAIL",
        "latency_ms": res4["latency_ms"],
        "details": f"Found {len(results_list)} quotes for Einstein" if t4_pass else "Filtering failed"
    })

    # Test 5 : GET /authors - List of authors
    res5 = client.request("GET", "/authors")
    auth_data = res5.get("json") or {}
    t5_pass = res5["status_code"] == 200 and "results" in auth_data
    results.append({
        "name": "GET /authors - Endpoint validity",
        "status": "PASS" if t5_pass else "FAIL",
        "latency_ms": res5["latency_ms"],
        "details": f"Status {res5['status_code']}"
    })

    # Test 6 : GET /quotes?maxLength=10 - Parameter contract (short quote)
    res6 = client.request("GET", "/quotes", params={"maxLength": 10})
    short_data = res6.get("json") or {}
    t6_pass = res6["status_code"] == 200 and isinstance(short_data.get("results"), list)
    results.append({
        "name": "GET /quotes?maxLength=10 - Param contract",
        "status": "PASS" if t6_pass else "FAIL",
        "latency_ms": res6["latency_ms"],
        "details": "Handled custom parameters correctly" if t6_pass else "Param failed"
    })

    # Test 7 : GET /nonexistent - Error 404 Expected (Robustness)
    res7 = client.request("GET", "/unknown_endpoint_xyz")
    t7_pass = res7["status_code"] == 404
    results.append({
        "name": "GET /unknown_endpoint_xyz - Expected 404 handling",
        "status": "PASS" if t7_pass else "FAIL",
        "latency_ms": res7["latency_ms"],
        "details": f"Got HTTP {res7['status_code']} as expected" if t7_pass else f"Unexpected status: {res7['status_code']}"
    })

    return results
