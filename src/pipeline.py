"""
Main Feature Pipeline

This module orchestrates the entire feature generation and registration process,
including data loading, feature engineering, export, and Feast registration.
"""

import sys
import os
from typing import Dict, Optional

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feature_generation.data_loader import load_raw_data, validate_raw_data
from feature_generation.feature_engineering import engineer_all_features, validate_engineered_features
from feature_generation.data_exporter import (
    export_features_to_csv, export_raw_data_to_csv,
    create_feature_summary, validate_exported_files
)
from feature_store.registry import register_all_features, export_metadata, validate_feature_store


def generate_all_features(
    data_dir: str = "data",
    export_raw: bool = True,
    create_summary: bool = True,
    validate_export: bool = True
) -> Dict:
    """
    Generate all features from raw data
    
    Args:
        data_dir: Base directory for data
        export_raw: Whether to export raw data to CSV
        create_summary: Whether to create feature summary
        validate_export: Whether to validate exported files
    
    Returns:
        Dictionary containing raw and engineered data
    """
    print("🚀 Starting feature generation pipeline...")
    print("=" * 60)
    
    # Step 1: Load raw data
    print("\n📊 Step 1: Loading raw data...")
    raw_data = load_raw_data(f"{data_dir}/raw")
    
    if not validate_raw_data(raw_data):
        print("❌ Raw data validation failed!")
        return {}
    
    # Step 2: Export raw data (optional)
    if export_raw:
        print("\n📤 Step 2: Exporting raw data...")
        export_raw_data_to_csv(raw_data, f"{data_dir}/raw")
    
    # Step 3: Engineer features
    print("\n🔧 Step 3: Engineering features...")
    engineered_features = engineer_all_features(raw_data)
    
    if not validate_engineered_features(engineered_features):
        print("❌ Feature engineering validation failed!")
        return {}
    
    # Step 4: Export engineered features
    print("\n📤 Step 4: Exporting engineered features...")
    if not export_features_to_csv(engineered_features, f"{data_dir}/transformed"):
        print("❌ Feature export failed!")
        return {}
    
    # Step 5: Create summary (optional)
    if create_summary:
        print("\n📋 Step 5: Creating feature summary...")
        create_feature_summary(engineered_features, f"{data_dir}/feature_summary.txt")
    
    # Step 6: Validate exported files (optional)
    if validate_export:
        print("\n🔍 Step 6: Validating exported files...")
        if not validate_exported_files(engineered_features, f"{data_dir}/transformed"):
            print("❌ File validation failed!")
            return {}
    
    print("\n✅ Feature generation pipeline completed successfully!")
    print("=" * 60)
    
    return {
        'raw_data': raw_data,
        'engineered_features': engineered_features
    }


def register_features_in_feast(
    repo_path: str = ".",
    use_s3: bool = False,
    should_export_metadata: bool = True
) -> bool:
    """
    Register features in Feast feature store
    
    Args:
        repo_path: Path to feature store repository
        use_s3: Whether to use S3 sources instead of local CSV files
        export_metadata: Whether to export metadata for DataHub
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("\n🏪 Registering features in Feast...")
    print("=" * 60)
    
    # Step 1: Register all features
    print("\n📝 Step 1: Registering features in Feast...")
    if not register_all_features(repo_path, use_s3):
        print("❌ Feature registration failed!")
        return False
    
    # Step 2: Validate feature store
    print("\n🔍 Step 2: Validating feature store...")
    if not validate_feature_store(repo_path):
        print("❌ Feature store validation failed!")
        return False
    
    # Step 3: Export metadata (optional)
    if should_export_metadata:
        print("\n📤 Step 3: Exporting metadata for DataHub...")
        if not export_metadata(repo_path, "data/feature_metadata.json"):
            print("⚠️ Metadata export failed, but continuing...")
    
    # Step 4: Run DataHub ingestion (optional)
    print("\n🔗 Step 4: Running DataHub ingestion...")
    try:
        from datahub_integration import run_datahub_ingestion
        if not run_datahub_ingestion(verbose=False):
            print("⚠️ DataHub ingestion failed, but continuing...")
    except ImportError:
        print("⚠️ DataHub integration not available, skipping...")
    
    print("\n✅ Feature registration completed successfully!")
    print("=" * 60)
    
    return True


def run_complete_pipeline(
    data_dir: str = "data",
    repo_path: str = ".",
    use_s3: bool = False,
    export_raw: bool = True,
    create_summary: bool = True,
    validate_export: bool = True,
    export_metadata: bool = True
) -> bool:
    """
    Run the complete feature pipeline from data generation to Feast registration
    
    Args:
        data_dir: Base directory for data
        repo_path: Path to feature store repository
        use_s3: Whether to use S3 sources instead of local CSV files
        export_raw: Whether to export raw data to CSV
        create_summary: Whether to create feature summary
        validate_export: Whether to validate exported files
        export_metadata: Whether to export metadata for DataHub
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("🎯 Running complete feature pipeline...")
    print("=" * 80)
    
    # Phase 1: Feature Generation
    result = generate_all_features(
        data_dir=data_dir,
        export_raw=export_raw,
        create_summary=create_summary,
        validate_export=validate_export
    )
    
    if not result:
        print("❌ Feature generation phase failed!")
        return False
    
    # Phase 2: Feature Registration
    if not register_features_in_feast(
        repo_path=repo_path,
        use_s3=use_s3,
        should_export_metadata=export_metadata
    ):
        print("❌ Feature registration phase failed!")
        return False
    
    print("\n🎉 Complete pipeline executed successfully!")
    print("=" * 80)
    print("\n📊 Summary:")
    print(f"- Raw data: {len(result['raw_data'])} datasets")
    print(f"- Engineered features: {len(result['engineered_features'])} feature sets")
    print(f"- Data directory: {data_dir}")
    print(f"- Feature store: {repo_path}")
    print(f"- S3 sources: {use_s3}")
    
    return True


def main():
    """Main entry point for the pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Feature Store Pipeline")
    parser.add_argument("--data-dir", default="data", help="Data directory")
    parser.add_argument("--repo-path", default=".", help="Feature store repository path")
    parser.add_argument("--use-s3", action="store_true", help="Use S3 sources instead of local CSV")
    parser.add_argument("--skip-raw-export", action="store_true", help="Skip raw data export")
    parser.add_argument("--skip-summary", action="store_true", help="Skip feature summary creation")
    parser.add_argument("--skip-validation", action="store_true", help="Skip file validation")
    parser.add_argument("--skip-metadata", action="store_true", help="Skip metadata export")
    parser.add_argument("--generate-only", action="store_true", help="Only generate features, don't register")
    parser.add_argument("--register-only", action="store_true", help="Only register features, don't generate")
    
    args = parser.parse_args()
    
    if args.generate_only:
        # Only generate features
        result = generate_all_features(
            data_dir=args.data_dir,
            export_raw=not args.skip_raw_export,
            create_summary=not args.skip_summary,
            validate_export=not args.skip_validation
        )
        return bool(result)
    
    elif args.register_only:
        # Only register features
        return register_features_in_feast(
            repo_path=args.repo_path,
            use_s3=args.use_s3,
            should_export_metadata=not args.skip_metadata
        )
    
    else:
        # Run complete pipeline
        return run_complete_pipeline(
            data_dir=args.data_dir,
            repo_path=args.repo_path,
            use_s3=args.use_s3,
            export_raw=not args.skip_raw_export,
            create_summary=not args.skip_summary,
            validate_export=not args.skip_validation,
            export_metadata=not args.skip_metadata
        )


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 