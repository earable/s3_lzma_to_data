#!/usr/bin/env python3
"""
Simple script to run the ProcessAndSaveData workflow using compiled frenz_utils package
This is a simplified version for quick testing with optimized performance
"""

import os
import sys

# Import from compiled frenz_utils package
try:
    from frenz_utils.process_and_save_data import ProcessAndSaveData
    print("✅ Using compiled frenz_utils package (optimized)")
except ImportError:
    # Fallback to source files if compiled package not available
    try:
        from process_and_save_data import ProcessAndSaveData
        print("⚠️  Using source files (not optimized)")
    except ImportError:
        print("❌ Error: Could not import ProcessAndSaveData")
        sys.exit(1)

def main():
    """
    Simple main function with hardcoded values for quick testing
    Uses compiled frenz_utils package for optimal performance
    """
    # Configuration - modify these values as needed
    source_folder = "./RAW_DATA_F24AUN05FX1U_1753868352000"
    product_key = "xxxxx"
    
    print("🚀 Starting data processing workflow with compiled package...")
    print(f"📁 Source folder: {source_folder}")
    print(f"🔐 Product key: {product_key[:20]}...")
    
    # Validate source folder exists
    if not os.path.exists(source_folder):
        print(f"❌ Error: Source folder does not exist: {source_folder}")
        return 1
    
    try:
        # Initialize processor with product key validation
        processor = ProcessAndSaveData(source_folder, product_key)
        
        # Run complete workflow
        saved_files = processor.run_complete_workflow()
        
        # Print results
        print("\n💾 SAVED FILES:")
        print("=" * 60)
        success_count = 0
        for sensor, file_info in saved_files.items():
            if file_info is None:
                print(f"{sensor.upper():8}: Failed to save")
            else:
                print(f"{sensor.upper():8}: {file_info['filepath']}")
                print(f"{'':8}  Shape: {file_info['shape']}, Start time: {file_info['start_time']}")
                success_count += 1
        
        print("=" * 60)
        print(f"✅ Successfully processed {success_count}/5 sensors")
        
        return 0
        
    except ValueError as e:
        print(f"❌ Validation Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 