#!/usr/bin/env python3
"""
Demo script for DatReader - Visual data display
"""

from dat_reader import DatReader
import numpy as np

def demo_reader():
    extracted_folder = "./extracted_RAW_DATA_F24AUN05FX1U_1753868352000"
    
    print("🎯 DAT READER DEMO")
    print("=" * 60)
    
    # Create reader
    reader = DatReader(extracted_folder)
    
    # Read all data
    all_data = reader.read_all_sensors()
    
    print(f"\n📊 SENSOR DATA OVERVIEW:")
    print("=" * 60)
    
    for sensor, data in all_data.items():
        if data is not None:
            print(f"\n🔹 {sensor.upper()}:")
            print(f"   Shape: {data.shape}")
            print(f"   Total samples: {len(data):,}")
            
            # Show data range
            if sensor in ['hr', 'spo2']:
                values = data[:, 0]
                timestamps = data[:, 1]
                print(f"   Value range: {np.min(values):.1f} → {np.max(values):.1f}")
                print(f"   Time range: {timestamps[0]:.0f} → {timestamps[-1]:.0f}")
            else:
                # For multi-channel sensors, show channel info
                n_channels = data.shape[1] - 1  # Exclude timestamp
                timestamps = data[:, -1]
                print(f"   Channels: {n_channels}")
                print(f"   Time range: {timestamps[0]:.0f} → {timestamps[-1]:.0f}")
                
                # Show channel ranges
                for i in range(n_channels):
                    channel_data = data[:, i]
                    print(f"   Channel {i+1}: {np.min(channel_data):.0f} → {np.max(channel_data):.0f}")
    
    print(f"\n🎨 SAMPLE DATA PREVIEW:")
    print("=" * 60)
    
    # Show sample data for each sensor
    for sensor, data in all_data.items():
        if data is not None and len(data) > 0:
            print(f"\n📈 {sensor.upper()} - First 5 samples:")
            
            if sensor in ['hr', 'spo2']:
                # Simple format for HR and SPO2
                for i in range(min(5, len(data))):
                    value = data[i, 0]
                    timestamp = data[i, 1]
                    print(f"   Sample {i+1}: {value:6.1f} | Time: {timestamp:.0f}")
            else:
                # Multi-channel format
                for i in range(min(5, len(data))):
                    channels = data[i, :-1]  # All except timestamp
                    timestamp = data[i, -1]
                    channel_str = " | ".join([f"{ch:8.0f}" for ch in channels])
                    print(f"   Sample {i+1}: [{channel_str}] | Time: {timestamp:.0f}")
    
    print(f"\n📋 DATA QUALITY CHECK:")
    print("=" * 60)
    
    for sensor, data in all_data.items():
        if data is not None:
            print(f"\n🔍 {sensor.upper()}:")
            
            # Check for NaN values
            nan_count = np.isnan(data).sum()
            if nan_count > 0:
                print(f"   ⚠️  Found {nan_count} NaN values")
            else:
                print(f"   ✅ No NaN values")
            
            # Check for infinite values
            inf_count = np.isinf(data).sum()
            if inf_count > 0:
                print(f"   ⚠️  Found {inf_count} infinite values")
            else:
                print(f"   ✅ No infinite values")
            
            # Check timestamp consistency
            if data.shape[1] > 1:
                timestamps = data[:, -1]
                time_diff = np.diff(timestamps)
                if np.any(time_diff < 0):
                    print(f"   ⚠️  Non-monotonic timestamps detected")
                else:
                    print(f"   ✅ Timestamps are monotonic")
                
                # Show time intervals
                if len(time_diff) > 0:
                    avg_interval = np.mean(time_diff)
                    print(f"   📊 Average time interval: {avg_interval:.2f} seconds")
    
    print(f"\n✅ DEMO COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    demo_reader() 