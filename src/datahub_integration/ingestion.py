"""
Simple DataHub ingestion for Feast feature store.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_datahub_ingestion(verbose: bool = True) -> bool:
    """Run DataHub ingestion for Feast metadata.
    
    Args:
        verbose: Whether to print detailed output.
        
    Returns:
        True if successful, False otherwise.
    """
    # Get paths
    project_root = Path(__file__).parent.parent.parent
    config_path = project_root / "configs" / "datahub_config.yaml"
    
    # Basic validation
    if not config_path.exists():
        print("❌ Error: datahub_config.yaml not found")
        return False
    
    if not os.environ.get('CONDA_DEFAULT_ENV') == 'feast-env':
        print("⚠️  Warning: Not in feast-env environment")
        print("Please run: conda activate feast-env")
        return False
    
    if verbose:
        print("🚀 Starting DataHub ingestion...")
    
    try:
        # Run ingestion
        result = subprocess.run(
            ["datahub", "ingest", "-c", str(config_path)],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        if verbose:
            print("✅ DataHub ingestion completed successfully!")
            print("🌐 Check your DataHub instance at http://localhost:9002")
        
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        if verbose:
            print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = run_datahub_ingestion()
    sys.exit(0 if success else 1) 