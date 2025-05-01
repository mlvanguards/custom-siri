import json
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Dict, List, Tuple


def run_function(func: Callable, args: dict) -> dict:
    try:
        result = func(**args)
        return {"success": True, "output": result}
    except Exception as e:
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}


def run_execution_checker_parallel(
    dataset: List[dict], function_map: Dict[str, Callable], max_workers=8
) -> dict:
    total = 0
    passed = 0
    failed = 0
    detailed_results = []

    tasks: List[Tuple[int, str, Callable, dict]] = []

    # Step 1: Prepare all calls
    for item in dataset:
        entry_id = item["id"]
        query = item.get("query", "")
        call_results = []

        for call in item.get("answers", []):
            func_name = call["name"]
            args = call.get("arguments", {})
            func = function_map.get(func_name)

            if not func:
                call_results.append(
                    {
                        "function": func_name,
                        "status": "error",
                        "message": f"Function '{func_name}' not found",
                    }
                )
                failed += 1
                continue

            tasks.append((entry_id, query, func_name, func, args))

        detailed_results.append(
            {
                "id": entry_id,
                "query": query,
                "results": call_results,  # Will update this below
            }
        )

    # Step 2: Execute in parallel
    result_map = {}  # Map entry_id to results

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run_function, func, args): (entry_id, func_name)
            for (entry_id, _, func_name, func, args) in tasks
        }

        for future in as_completed(futures):
            entry_id, func_name = futures[future]
            try:
                result = future.result()
                total += 1
                status = "success" if result["success"] else "fail"
                if result["success"]:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                result = {
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }
                status = "fail"
                failed += 1
                total += 1

            # Append result
            if entry_id not in result_map:
                result_map[entry_id] = []
            result_map[entry_id].append(
                {"function": func_name, "status": status, "result": result}
            )

    # Step 3: Merge results back into detailed report
    for entry in detailed_results:
        rid = entry["id"]
        if rid in result_map:
            entry["results"].extend(result_map[rid])

    report = {
        "total_function_calls": total,
        "passed": passed,
        "failed": failed,
        "success_rate": round((passed / total) * 100, 2) if total else 0,
        "detailed": detailed_results,
    }

    return report


def save_execution_report(report: dict, path="execution_report.json"):
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[✓] Execution report saved to {path}")


if __name__ == "__main__":
    from src.functions.functions import (
        available_function_calls,  # your function registry
    )

    with open("data/dataset.json") as f:
        dataset = json.load(f)[:10]

    report = run_execution_checker_parallel(
        dataset, available_function_calls, max_workers=8
    )
    save_execution_report(report)

    print(f"✅ Executed {report['total_function_calls']} calls")
    print(f"✔️  Passed: {report['passed']}")
    print(f"❌ Failed: {report['failed']}")
    print(f"📊 Success Rate: {report['success_rate']}%")
