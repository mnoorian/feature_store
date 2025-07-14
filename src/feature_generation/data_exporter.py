"""
Data Export Module

This module handles exporting engineered features to CSV files for use in the feature store.
"""

import os
import pandas as pd
from typing import Dict, Optional
from datetime import datetime


def ensure_directory_exists(directory: str) -> None:
    """
    Ensure a directory exists, create it if it doesn't
    
    Args:
        directory: Directory path to ensure exists
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"📁 Created directory: {directory}")


def export_features_to_csv(
    engineered_features: Dict[str, pd.DataFrame],
    output_dir: str = "data/transformed"
) -> bool:
    """
    Export engineered features to CSV files
    
    Args:
        engineered_features: Dictionary containing engineered feature DataFrames
        output_dir: Directory to save CSV files
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        ensure_directory_exists(output_dir)
        
        print(f"📤 Exporting features to {output_dir}...")
        
        # Export each feature set
        for feature_name, df in engineered_features.items():
            # Create filename
            filename = f"{feature_name}_features.csv"
            filepath = os.path.join(output_dir, filename)
            
            # Export to CSV
            df.to_csv(filepath, index=False)
            
            print(f"✅ Exported {feature_name} features: {df.shape[0]} rows, {df.shape[1]} columns")
        
        print("✅ All features exported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting features: {e}")
        return False


def export_raw_data_to_csv(
    raw_data: Dict[str, pd.DataFrame],
    output_dir: str = "data/raw"
) -> bool:
    """
    Export raw data to CSV files for reference
    
    Args:
        raw_data: Dictionary containing raw data DataFrames
        output_dir: Directory to save CSV files
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        ensure_directory_exists(output_dir)
        
        print(f"📤 Exporting raw data to {output_dir}...")
        
        # Export each dataset
        for data_name, df in raw_data.items():
            # Create filename
            filename = f"{data_name}.csv"
            filepath = os.path.join(output_dir, filename)
            
            # Export to CSV
            df.to_csv(filepath, index=False)
            
            print(f"✅ Exported {data_name} data: {df.shape[0]} rows, {df.shape[1]} columns")
        
        print("✅ All raw data exported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting raw data: {e}")
        return False


def create_feature_summary(
    engineered_features: Dict[str, pd.DataFrame],
    output_file: str = "data/feature_summary.txt"
) -> bool:
    """
    Create a summary of all engineered features
    
    Args:
        engineered_features: Dictionary containing engineered feature DataFrames
        output_file: Path to save the summary file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir:
            ensure_directory_exists(output_dir)
        
        with open(output_file, 'w') as f:
            f.write("Feature Engineering Summary\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            total_features = 0
            total_rows = 0
            
            for feature_name, df in engineered_features.items():
                f.write(f"Feature Set: {feature_name}\n")
                f.write("-" * 30 + "\n")
                f.write(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
                f.write(f"Columns: {', '.join(df.columns)}\n")
                f.write(f"Missing values: {df.isnull().sum().sum()}\n")
                f.write(f"Duplicates: {df.duplicated().sum()}\n")
                f.write("\n")
                
                total_features += df.shape[1]
                total_rows += df.shape[0]
            
            f.write("Summary Statistics\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total feature sets: {len(engineered_features)}\n")
            f.write(f"Total features: {total_features}\n")
            f.write(f"Total rows: {total_rows}\n")
        
        print(f"✅ Feature summary created: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating feature summary: {e}")
        return False


def validate_exported_files(
    engineered_features: Dict[str, pd.DataFrame],
    output_dir: str = "data/transformed"
) -> bool:
    """
    Validate that exported files exist and have correct content
    
    Args:
        engineered_features: Dictionary containing engineered feature DataFrames
        output_dir: Directory containing exported files
    
    Returns:
        bool: True if all files are valid, False otherwise
    """
    try:
        print("🔍 Validating exported files...")
        
        for feature_name, df in engineered_features.items():
            filename = f"{feature_name}_features.csv"
            filepath = os.path.join(output_dir, filename)
            
            # Check if file exists
            if not os.path.exists(filepath):
                print(f"❌ File not found: {filepath}")
                return False
            
            # Check file size
            file_size = os.path.getsize(filepath)
            if file_size == 0:
                print(f"❌ Empty file: {filepath}")
                return False
            
            # Load and validate content
            exported_df = pd.read_csv(filepath)
            
            # Check shape
            if exported_df.shape != df.shape:
                print(f"❌ Shape mismatch for {feature_name}: expected {df.shape}, got {exported_df.shape}")
                return False
            
            # Check columns
            if list(exported_df.columns) != list(df.columns):
                print(f"❌ Column mismatch for {feature_name}")
                return False
            
            print(f"✅ Validated {feature_name}: {exported_df.shape[0]} rows, {exported_df.shape[1]} columns")
        
        print("✅ All exported files validated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error validating exported files: {e}")
        return False


def cleanup_old_files(output_dir: str = "data/transformed", days: int = 7) -> bool:
    """
    Clean up old feature files
    
    Args:
        output_dir: Directory containing feature files
        days: Number of days to keep files
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not os.path.exists(output_dir):
            return True
        
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        removed_count = 0
        
        for filename in os.listdir(output_dir):
            if filename.endswith('_features.csv'):
                filepath = os.path.join(output_dir, filename)
                file_time = os.path.getmtime(filepath)
                
                if file_time < cutoff_time:
                    os.remove(filepath)
                    removed_count += 1
                    print(f"🗑️ Removed old file: {filename}")
        
        if removed_count > 0:
            print(f"✅ Cleaned up {removed_count} old files")
        else:
            print("✅ No old files to clean up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up old files: {e}")
        return False 