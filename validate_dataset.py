#!/usr/bin/env python3
"""
Simple dataset validation using existing functions
"""
import json
import sys


from src.dataset.check_format import run_format_checker
from src.dataset.clean import deduplicate_and_decontaminate_dataset
from src.dataset.execution_checker import run_execution_checker_parallel, save_execution_report


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_dataset.py <dataset.json>")
        return
    
    dataset_path = sys.argv[1]
    
    # Load dataset
    print(f"Loading dataset from {dataset_path}...")
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
    print(f"Loaded {len(dataset)} entries")
    
    # Step 1: Format checking
    print("\n1. Format validation...")
    try:
        valid, invalid = run_format_checker(dataset)
        print(f"   Valid: {len(valid)}")
        print(f"   Invalid: {len(invalid)}")
        
        if invalid:
            print("   Invalid entries:")
            for entry_id, reason in invalid[:5]:
                print(f"     - ID {entry_id}: {reason}")
        
        dataset = valid
    except Exception as e:
        print(f"   Format checking failed: {e}")
    
    # Step 2: Deduplication
    print("\n2. Deduplication...")
    try:
        original_count = len(dataset)
        dataset = deduplicate_and_decontaminate_dataset(dataset)
        removed = original_count - len(dataset)
        print(f"   Removed {removed} duplicates")
        print(f"   Remaining: {len(dataset)} entries")
    except Exception as e:
        print(f"   Deduplication failed: {e}")
    
    # Step 3: Execution validation (optional - requires functions.py)
    print("\n3. Execution validation...")
    try:
        from src.functions.functions import available_function_calls
        
        # Test first 10 entries only
        test_dataset = dataset[:10]
        report = run_execution_checker_parallel(test_dataset, available_function_calls, max_workers=8)

        save_execution_report(report)
        
        print(f"✅ Tested {report['total_function_calls']} function calls")
        print(f"📊 Success rate: {report['success_rate']}%")
        print(f"✔️ Passed: {report['passed']}")
        print(f"❌ Failed: {report['failed']}")
        
    except ImportError:
        print("❌ Functions module not found, skipping execution validation")
    except Exception as e:
        print(f"❌ Execution validation failed: {e}")
    
    # Save cleaned dataset
    output_path = dataset_path.replace('.json', '_cleaned.json')
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"\n✅ Cleaned dataset saved to {output_path}")
    print(f"Final count: {len(dataset)} entries")


if __name__ == "__main__":
    main()
