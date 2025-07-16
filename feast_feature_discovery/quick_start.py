#!/usr/bin/env python3
"""
Quick Start Feature Discovery

Simple script to get started with feature discovery immediately.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def quick_discovery():
    """Run a quick feature discovery"""
    print("🚀 Quick Start Feature Discovery")
    print("=" * 50)
    
    try:
        # Import and check Feast
        import feast
        print(f"✅ Feast is available (version {feast.__version__})")
        
        # Get feature store
        from feature_store.registry import get_feature_store
        store = get_feature_store()
        
        # Quick stats
        feature_views = list(store.list_feature_views())
        feature_services = list(store.list_feature_services())
        entities = list(store.list_entities())
        
        print(f"\n📊 Quick Overview:")
        print(f"   • {len(feature_views)} Feature Views")
        print(f"   • {len(feature_services)} Feature Services")
        print(f"   • {len(entities)} Entities")
        
        # List feature views
        print(f"\n📋 Your Feature Views:")
        for i, fv in enumerate(feature_views, 1):
            features_count = len(fv.schema)
            print(f"   {i}. {fv.name} ({features_count} features)")
        
        # List entities
        print(f"\n🔑 Your Entities:")
        for i, entity in enumerate(entities, 1):
            print(f"   {i}. {entity.name} ({entity.value_type})")
        
        print(f"\n🎯 Next Steps:")
        print("   Choose a discovery method:")
        print("   • python feature_discovery/method1_builtin.py      (Quick overview)")
        print("   • python feature_discovery/method2_cli.py          (Detailed CLI)")
        print("   • python feature_discovery/method3_interactive.py  (Custom search)")
        print("   • python feature_discovery/method4_metadata.py     (JSON metadata)")
        print("   • python feature_discovery/run_all_methods.py      (Run all methods)")
        
        return True
        
    except ImportError:
        print("❌ Import Error: Make sure you're in the project root directory")
        print("💡 Setup: conda activate feast-env")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    success = quick_discovery()
    
    if success:
        print(f"\n✅ Quick discovery completed!")
        
        # Ask if user wants to run a specific method
        print(f"\n❓ Want to run a specific discovery method now?")
        print("   1. Method 1 (Built-in Function)")
        print("   2. Method 2 (Feast CLI)")
        print("   3. Method 3 (Interactive Python)")
        print("   4. Method 4 (JSON Metadata)")
        print("   5. Run All Methods")
        print("   0. Exit")
        
        try:
            choice = input("\nEnter your choice (0-5): ").strip()
            
            if choice == "1":
                os.system("python feature_discovery/method1_builtin.py")
            elif choice == "2":
                os.system("python feature_discovery/method2_cli.py")
            elif choice == "3":
                os.system("python feature_discovery/method3_interactive.py")
            elif choice == "4":
                os.system("python feature_discovery/method4_metadata.py")
            elif choice == "5":
                os.system("python feature_discovery/run_all_methods.py")
            elif choice == "0":
                print("👋 Happy feature discovering!")
            else:
                print("Invalid choice. Run scripts manually.")
                
        except KeyboardInterrupt:
            print("\n👋 Happy feature discovering!")
    else:
        print(f"\n❌ Quick discovery failed. Please check the setup instructions above.")

if __name__ == "__main__":
    main() 