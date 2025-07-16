#!/usr/bin/env python3
"""
Run All Discovery Methods

Executes all feature discovery methods sequentially for comprehensive exploration.
"""

import sys
import subprocess
from pathlib import Path

def run_method(method_name, script_path):
    """Run a discovery method and handle errors"""
    print(f"\n{'='*60}")
    print(f"🚀 Running {method_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_path], check=True)
        print(f"✅ {method_name} completed successfully!")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {method_name} failed")
        return False

def main():
    print("🔍 Feature Discovery - All Methods")
    print("=" * 60)
    
    # Get the directory of this script
    script_dir = Path(__file__).parent
    
    # Define methods to run
    methods = [
        ("Method 1: Built-in Function", script_dir / "method1_builtin.py"),
        ("Method 2: Feast CLI", script_dir / "method2_cli.py"),
        ("Method 3: Interactive Python", script_dir / "method3_interactive.py"),
        ("Method 4: JSON Metadata", script_dir / "method4_metadata.py"),
    ]
    
    # Track results
    results = {}
    
    # Run each method
    for method_name, script_path in methods:
        success = run_method(method_name, script_path)
        results[method_name] = success
        
        # Add separator between methods
        print("\n" + "🔄" * 60)
        input("Press Enter to continue to next method (or Ctrl+C to stop)...")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 DISCOVERY SUMMARY")
    print(f"{'='*60}")
    
    for method_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status:12} {method_name}")
    
    successful_methods = sum(results.values())
    total_methods = len(results)
    
    print(f"\n🎯 Overall Result: {successful_methods}/{total_methods} methods completed successfully")
    
    if successful_methods == total_methods:
        print("🎉 All discovery methods completed successfully!")
    else:
        print("⚠️  Some methods failed. Check the error messages above.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Discovery stopped by user") 