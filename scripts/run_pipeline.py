#!/usr/bin/env python3
"""
Feature Store Pipeline Runner

This script runs the complete feature store pipeline including:
- Data generation and feature engineering
- Feature registration in Feast
- Metadata export for DataHub

Usage:
    python scripts/run_pipeline.py [options]
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from pipeline import run_complete_pipeline, generate_all_features, register_features_in_feast


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Feature Store Pipeline Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run complete pipeline
    python scripts/run_pipeline.py
    
    # Generate features only
    python scripts/run_pipeline.py --generate-only
    
    # Register features only
    python scripts/run_pipeline.py --register-only
    
    # Export metadata only
    python scripts/run_pipeline.py --export-metadata-only
    
    # Use S3 sources
    python scripts/run_pipeline.py --use-s3
    
    # Custom data directory
    python scripts/run_pipeline.py --data-dir /path/to/data
        """
    )
    
    # Pipeline options
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Data directory (default: data)"
    )
    parser.add_argument(
        "--repo-path",
        default=".",
        help="Feature store repository path (default: current directory)"
    )
    parser.add_argument(
        "--use-s3",
        action="store_true",
        help="Use S3 sources instead of local CSV files"
    )
    
    # Pipeline phases
    parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Only generate features, don't register"
    )
    parser.add_argument(
        "--register-only",
        action="store_true",
        help="Only register features, don't generate"
    )
    parser.add_argument(
        "--export-metadata-only",
        action="store_true",
        help="Only export metadata from existing Feast registry"
    )
    
    # Optional steps
    parser.add_argument(
        "--skip-raw-export",
        action="store_true",
        help="Skip raw data export"
    )
    parser.add_argument(
        "--skip-summary",
        action="store_true",
        help="Skip feature summary creation"
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip file validation"
    )
    parser.add_argument(
        "--skip-metadata",
        action="store_true",
        help="Skip metadata export"
    )
    
    # Output options
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if sum([args.generate_only, args.register_only, args.export_metadata_only]) > 1:
        print("❌ Error: Cannot specify multiple 'only' options")
        return 1
    
    if not os.path.exists(args.data_dir):
        print(f"📁 Creating data directory: {args.data_dir}")
        os.makedirs(args.data_dir, exist_ok=True)
    
    # Show configuration
    print("🎯 Feature Store Pipeline Configuration")
    print("=" * 50)
    print(f"Data directory: {args.data_dir}")
    print(f"Repository path: {args.repo_path}")
    print(f"Use S3 sources: {args.use_s3}")
    print(f"Generate only: {args.generate_only}")
    print(f"Register only: {args.register_only}")
    print(f"Skip raw export: {args.skip_raw_export}")
    print(f"Skip summary: {args.skip_summary}")
    print(f"Skip validation: {args.skip_validation}")
    print(f"Skip metadata: {args.skip_metadata}")
    print(f"Verbose: {args.verbose}")
    print(f"Dry run: {args.dry_run}")
    print()
    
    if args.dry_run:
        print("🔍 Dry run mode - no actual execution")
        return 0
    
    try:
        if args.generate_only:
            # Only generate features
            print("🚀 Running feature generation only...")
            result = generate_all_features(
                data_dir=args.data_dir,
                export_raw=not args.skip_raw_export,
                create_summary=not args.skip_summary,
                validate_export=not args.skip_validation
            )
            success = bool(result)
            
        elif args.register_only:
            # Only register features
            print("🏪 Running feature registration only...")
            success = register_features_in_feast(
                repo_path=args.repo_path,
                use_s3=args.use_s3,
                export_metadata=not args.skip_metadata
            )
            
        elif args.export_metadata_only:
            # Only export metadata
            print("📤 Running metadata export only...")
            from feature_store.registry import export_metadata
            success = export_metadata()
            
        else:
            # Run complete pipeline
            print("🎯 Running complete pipeline...")
            success = run_complete_pipeline(
                data_dir=args.data_dir,
                repo_path=args.repo_path,
                use_s3=args.use_s3,
                export_raw=not args.skip_raw_export,
                create_summary=not args.skip_summary,
                validate_export=not args.skip_validation,
                export_metadata=not args.skip_metadata
            )
        
        if success:
            print("\n🎉 Pipeline completed successfully!")
            return 0
        else:
            print("\n❌ Pipeline failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Pipeline interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 