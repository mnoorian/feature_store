#!/usr/bin/env python3
"""
Method 2: Feast CLI Discovery

Automates Feast CLI commands for comprehensive feature discovery.
Best for: Detailed command-line exploration and scripting.
"""

import subprocess
import sys

def run_feast_command(command):
    """Run a feast CLI command and return the output"""
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, check=True)
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def main():
    print("🔍 Method 2: Feast CLI Discovery")
    print("=" * 60)
    
    # Check if feast CLI is available
    if not run_feast_command("feast --version"):
        print("❌ Feast CLI not found. Make sure Feast is installed and activated.")
        return
    
    # Basic listing commands
    commands = [
        ("📊 Feature Views", "feast feature-views list"),
        ("🛠️ Feature Services", "feast feature-services list"),
        ("🔑 Entities", "feast entities list"),
    ]
    
    for title, command in commands:
        print(f"\n{title}:")
        print("-" * 50)
        output = run_feast_command(command)
        if output:
            print(output)
        else:
            print("❌ Command failed")
    
    # Detailed descriptions
    feature_views = ["user_demographic_features", "user_behavior_features", 
                     "transaction_features", "product_features"]
    
    print("\n📋 Feature View Details:")
    print("=" * 60)
    
    for fv_name in feature_views:
        print(f"\n🔸 {fv_name}:")
        output = run_feast_command(f"feast feature-views describe {fv_name}")
        if output:
            lines = output.split('\n')
            for line in lines[:20]:  # Show first 20 lines
                if any(keyword in line.lower() for keyword in ['name:', 'entities:', 'features:', 'description:', 'uri:']):
                    print(line)
    
    print("\n✅ CLI Discovery completed successfully!")

if __name__ == "__main__":
    main() 