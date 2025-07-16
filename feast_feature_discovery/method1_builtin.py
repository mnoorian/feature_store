#!/usr/bin/env python3
"""
Method 1: Built-in Function Discovery

Uses the existing list_registered_features function from your codebase.
Best for: Quick overview of registered features.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def main():
    print("🔍 Method 1: Built-in Function Discovery")
    print("=" * 60)
    
    try:
        from feature_store.registry import list_registered_features
        list_registered_features()
        print("\n✅ Discovery completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you're in the project root directory")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main() 