#!/usr/bin/env python3
"""
Process and save data from .lzma files to .dat files
This module provides functionality to:
1. Load and process data using process_and_load_data
2. Save processed data to .dat files in the extracted folder structure
"""

import os
import numpy as np
from data_loader import process_and_load_data

class ProcessAndSaveData:
    def __init__(self, source_folder):
        self.source_folder = source_folder
        self.extracted_folder = None
        self.processed_data = {}

    def _check_dat_file_exists(self, sensor):
        """
        Check if .dat file already exists for a sensor
        """
        sensor_folders = {
            'eeg': 'EEG2', 'imu': 'IMU2', 'ppg': 'PPG2', 'hr': 'HR', 'spo2': 'SPO2'
        }
        source_folder_name = os.path.basename(self.source_folder)
        expected_extracted_folder = f"./extracted_{source_folder_name}"
        sensor_folder = sensor_folders.get(sensor, sensor.upper())
        sensor_path = os.path.join(expected_extracted_folder, sensor_folder)
        dat_filename = f"{sensor}_full_data.dat"
        dat_filepath = os.path.join(sensor_path, dat_filename)
        return os.path.exists(dat_filepath)

    def process_all_sensors(self):
        print("🔄 Starting to process all sensor data...")
        sensors = ['eeg', 'imu', 'ppg', 'hr', 'spo2']
        source_folder_name = os.path.basename(self.source_folder)
        self.extracted_folder = f"./extracted_{source_folder_name}" # Initialize extracted_folder here

        for sensor in sensors:
            try:
                print(f"\n📊 Processing {sensor.upper()} data...")
                if self._check_dat_file_exists(sensor):
                    print(f"⚠️  {sensor.upper()} .dat file already exists, skipping processing...")
                    self.processed_data[sensor] = {
                        'data': None,
                        'start_time': 'Already exists',
                        'shape': 'Already exists',
                        'exists': True
                    }
                    continue

                data_array, start_time, extracted_folder = process_and_load_data(
                    source_folder=self.source_folder,
                    sensor=sensor
                )
                if self.extracted_folder is None: # This check is now redundant due to early initialization
                    self.extracted_folder = extracted_folder

                processed_data = self._process_sensor_data(sensor, data_array)
                self.processed_data[sensor] = {
                    'data': processed_data,
                    'start_time': start_time,
                    'shape': processed_data.shape,
                    'exists': False
                }
                print(f"✅ {sensor.upper()} processed: {processed_data.shape}")
            except Exception as e:
                print(f"❌ Error processing {sensor}: {str(e)}")
                self.processed_data[sensor] = None
        return self.processed_data

    def _process_sensor_data(self, sensor, data_array):
        """
        Process data array based on sensor type (reshaping/sorting)
        """
        if len(data_array) == 0:
            return data_array
        if sensor == 'eeg':
            if len(data_array.shape) >= 2 and data_array.shape[1] >= 7:
                # First rearrange channels: [1,2,3,4,5,6,0] -> [1,2,3,4,5,6,0]
                rearranged_data = data_array[:, [1, 2, 3, 4, 5, 6, 0]]
                
                # Then sort by timestamp (last column) while preserving order within same timestamp
                # Get unique timestamps and their indices
                timestamps = rearranged_data[:, -1]
                unique_timestamps = np.unique(timestamps)
                
                # Create sorted indices
                sorted_indices = []
                for ts in sorted(unique_timestamps):
                    # Find all indices with this timestamp
                    ts_indices = np.where(timestamps == ts)[0]
                    # Keep original order within same timestamp
                    sorted_indices.extend(ts_indices)
                
                return rearranged_data[sorted_indices]
        elif sensor == 'imu':
            if len(data_array.shape) >= 2 and data_array.shape[1] >= 4:
                # First rearrange channels: [1,2,3,0] -> [1,2,3,0]
                rearranged_data = data_array[:, [1, 2, 3, 0]]
                
                # Then sort by timestamp (last column) while preserving order within same timestamp
                timestamps = rearranged_data[:, -1]
                unique_timestamps = np.unique(timestamps)
                
                # Create sorted indices
                sorted_indices = []
                for ts in sorted(unique_timestamps):
                    # Find all indices with this timestamp
                    ts_indices = np.where(timestamps == ts)[0]
                    # Keep original order within same timestamp
                    sorted_indices.extend(ts_indices)
                
                return rearranged_data[sorted_indices]
        elif sensor == 'ppg':
            if len(data_array.shape) >= 2 and data_array.shape[1] >= 4:
                # First rearrange channels: [1,2,3,0] -> [1,2,3,0]
                rearranged_data = data_array[:, [1, 2, 3, 0]]
                
                # Then sort by timestamp (last column) while preserving order within same timestamp
                timestamps = rearranged_data[:, -1]
                unique_timestamps = np.unique(timestamps)
                
                # Create sorted indices
                sorted_indices = []
                for ts in sorted(unique_timestamps):
                    # Find all indices with this timestamp
                    ts_indices = np.where(timestamps == ts)[0]
                    # Keep original order within same timestamp
                    sorted_indices.extend(ts_indices)
                
                return rearranged_data[sorted_indices]
        elif sensor == 'hr' or sensor == 'spo2':
            if len(data_array.shape) >= 2 and data_array.shape[1] >= 2:
                sorted_indices = np.argsort(data_array[:, -1])
                return data_array[sorted_indices]
        print(f"Warning: {sensor.upper()} data shape not as expected: {data_array.shape}")
        return data_array

    def save_to_dat_files(self):
        """
        Save processed data to .dat files
        """
        if not self.processed_data or self.extracted_folder is None:
            print("❌ No processed data available. Run process_all_sensors() first.")
            return {}
        saved_files = {}
        sensor_folders = {
            'eeg': 'EEG2', 'imu': 'IMU2', 'ppg': 'PPG2', 'hr': 'HR', 'spo2': 'SPO2'
        }
        for sensor, data_info in self.processed_data.items():
            if data_info is None:
                print(f"⚠️  Skipping {sensor} - no data available")
                continue
            sensor_folder = sensor_folders.get(sensor, sensor.upper())
            sensor_path = os.path.join(self.extracted_folder, sensor_folder)
            dat_filename = f"{sensor}_full_data.dat"
            dat_filepath = os.path.join(sensor_path, dat_filename)

            if data_info.get('exists', False) or os.path.exists(dat_filepath):
                print(f"⚠️  {sensor.upper()} .dat file already exists, skipping save: {dat_filepath}")
                saved_files[sensor] = {
                    'filepath': dat_filepath,
                    'shape': 'Already exists',
                    'start_time': 'Already exists'
                }
                continue
            if data_info['data'] is None:
                print(f"⚠️  Skipping {sensor} - no data to save")
                saved_files[sensor] = None
                continue

            if not os.path.exists(sensor_path):
                os.makedirs(sensor_path)
            data_info['data'].astype(np.float64).tofile(dat_filepath)
            saved_files[sensor] = {
                'filepath': dat_filepath,
                'shape': data_info['shape'],
                'start_time': data_info['start_time']
            }
            print(f"💾 Saved {sensor} data: {dat_filepath} ({data_info['shape']})")
        return saved_files

    def print_summary(self):
        """
        Print summary of processed data
        """
        if not self.processed_data:
            print("❌ No processed data available. Run process_all_sensors() first.")
            return
        print("\n📊 PROCESSED DATA SUMMARY:")
        print("=" * 60)
        for sensor, data_info in self.processed_data.items():
            if data_info is None:
                print(f"{sensor.upper():8}: No data")
                continue
            if data_info.get('exists', False):
                print(f"{sensor.upper():8}: File already exists (skipped processing)")
                continue
            data = data_info['data']
            if data is None or len(data) == 0:
                print(f"{sensor.upper():8}: Empty data")
                continue
            timestamps = data[:, -1]
            print(f"{sensor.upper():8}: {timestamps[0]:.3f} → {timestamps[-1]:.3f} ({len(timestamps)} samples, shape: {data.shape})")
        print("=" * 60)

    def run_complete_workflow(self):
        """
        Run complete workflow: process all sensors and save to .dat files
        """
        print("🚀 Starting complete workflow...")
        print(f"📁 Source folder: {self.source_folder}")
        self.process_all_sensors()
        self.print_summary()
        saved_files = self.save_to_dat_files()
        print(f"\n✅ Workflow completed!")
        print(f"📁 Extracted folder: {self.extracted_folder}")
        return saved_files

def main():
    source_folder = "./RAW_DATA_F25AUZ05FX1U_1753868352000"
    processor = ProcessAndSaveData(source_folder)
    saved_files = processor.run_complete_workflow()
    print("\n💾 SAVED FILES:")
    print("=" * 60)
    for sensor, file_info in saved_files.items():
        if file_info is None:
            print(f"{sensor.upper():8}: Failed to save")
        else:
            print(f"{sensor.upper():8}: {file_info['filepath']}")
            print(f"{'':8}  Shape: {file_info['shape']}, Start time: {file_info['start_time']}")

if __name__ == "__main__":
    main() 