#!/usr/bin/env python3
"""
Data Reader for .dat files
This module provides functionality to read and display data from .dat files
created by the process_and_save_data module.
"""

import os
import numpy as np
from datetime import datetime

class DatReader:
    def __init__(self, extracted_folder):
        """
        Initialize the data reader
        
        Args:
            extracted_folder: str - Path to the extracted folder containing .dat files
        """
        self.extracted_folder = extracted_folder
        self.sensor_folders = {
            'eeg': 'EEG2',
            'imu': 'IMU2', 
            'ppg': 'PPG2',
            'hr': 'HR',
            'spo2': 'SPO2'
        }
        
    def read_sensor_data(self, sensor):
        """
        Read data from a specific sensor's .dat file
        
        Args:
            sensor: str - Sensor type ('eeg', 'imu', 'ppg', 'hr', 'spo2')
            
        Returns:
            numpy.ndarray - Data array from the .dat file
        """
        if sensor not in self.sensor_folders:
            raise ValueError(f"Unknown sensor: {sensor}")
            
        # Construct file path
        sensor_folder = self.sensor_folders[sensor]
        dat_filename = f"{sensor}_full_data.dat"
        dat_filepath = os.path.join(self.extracted_folder, sensor_folder, dat_filename)
        
        # Check if file exists
        if not os.path.exists(dat_filepath):
            raise FileNotFoundError(f"Data file not found: {dat_filepath}")
        
        # Read binary data
        data = np.fromfile(dat_filepath, dtype=np.float64)
        
        # Reshape data based on sensor type
        if sensor == 'eeg':
            # EEG: (samples, 7) - 6 channels + 1 timestamp
            samples = len(data) // 7
            return data.reshape(samples, 7)
        elif sensor == 'imu':
            # IMU: (samples, 4) - 3 channels + 1 timestamp
            samples = len(data) // 4
            return data.reshape(samples, 4)
        elif sensor == 'ppg':
            # PPG: (samples, 4) - 3 channels + 1 timestamp
            samples = len(data) // 4
            return data.reshape(samples, 4)
        elif sensor == 'hr':
            # HR: (samples, 2) - 1 channel + 1 timestamp
            samples = len(data) // 2
            return data.reshape(samples, 2)
        elif sensor == 'spo2':
            # SPO2: (samples, 2) - 1 channel + 1 timestamp
            samples = len(data) // 2
            return data.reshape(samples, 2)
        else:
            return data
    
    def print_sensor_info(self, sensor):
        """
        Print detailed information about a sensor's data
        
        Args:
            sensor: str - Sensor type ('eeg', 'imu', 'ppg', 'hr', 'spo2')
        """
        try:
            print(f"\n📊 {sensor.upper()} DATA INFO:")
            print("=" * 50)
            
            # Read data
            data = self.read_sensor_data(sensor)
            
            # Basic info
            print(f"Shape: {data.shape}")
            print(f"Data type: {data.dtype}")
            print(f"Total samples: {len(data)}")
            
            # Channel info
            if len(data.shape) == 2:
                n_channels = data.shape[1]
                print(f"Number of channels: {n_channels}")
                
                # Show first and last few samples
                print(f"\nFirst 3 samples:")
                for i in range(min(3, len(data))):
                    if sensor in ['hr', 'spo2']:
                        print(f"  Sample {i}: Value={data[i, 0]:.2f}, Timestamp={data[i, 1]:.3f}")
                    else:
                        channels = data[i, :-1]  # All except timestamp
                        timestamp = data[i, -1]
                        print(f"  Sample {i}: Channels={channels}, Timestamp={timestamp:.3f}")
                
                print(f"\nLast 3 samples:")
                for i in range(max(0, len(data)-3), len(data)):
                    if sensor in ['hr', 'spo2']:
                        print(f"  Sample {i}: Value={data[i, 0]:.2f}, Timestamp={data[i, 1]:.3f}")
                    else:
                        channels = data[i, :-1]  # All except timestamp
                        timestamp = data[i, -1]
                        print(f"  Sample {i}: Channels={channels}, Timestamp={timestamp:.3f}")
                
                # Timestamp range
                if n_channels > 1:
                    timestamps = data[:, -1]
                    start_time = timestamps[0]
                    end_time = timestamps[-1]
                    duration = end_time - start_time
                    
                    print(f"\nTimestamp Range:")
                    print(f"  Start: {start_time:.3f} ({datetime.fromtimestamp(start_time)})")
                    print(f"  End: {end_time:.3f} ({datetime.fromtimestamp(end_time)})")
                    print(f"  Duration: {duration:.3f} seconds ({duration/60:.2f} minutes)")
                
                # Data statistics
                if sensor in ['hr', 'spo2']:
                    values = data[:, 0]
                    print(f"\nValue Statistics:")
                    print(f"  Min: {np.min(values):.2f}")
                    print(f"  Max: {np.max(values):.2f}")
                    print(f"  Mean: {np.mean(values):.2f}")
                    print(f"  Std: {np.std(values):.2f}")
                else:
                    print(f"\nChannel Statistics:")
                    for i in range(n_channels - 1):  # Exclude timestamp
                        channel_data = data[:, i]
                        print(f"  Channel {i+1}: Min={np.min(channel_data):.2f}, Max={np.max(channel_data):.2f}, Mean={np.mean(channel_data):.2f}")
            
        except Exception as e:
            print(f"❌ Error reading {sensor} data: {str(e)}")
    
    def read_all_sensors(self):
        """
        Read data from all available sensors
        
        Returns:
            dict - Dictionary containing data for all sensors
        """
        all_data = {}
        
        for sensor in self.sensor_folders.keys():
            try:
                data = self.read_sensor_data(sensor)
                all_data[sensor] = data
                print(f"✅ Loaded {sensor.upper()}: {data.shape}")
            except Exception as e:
                print(f"❌ Failed to load {sensor.upper()}: {str(e)}")
                all_data[sensor] = None
        
        return all_data
    
    def print_summary(self):
        """
        Print summary of all available sensor data
        """
        print(f"\n📁 READING FROM: {self.extracted_folder}")
        print("=" * 60)
        
        all_data = self.read_all_sensors()
        
        print(f"\n📊 DATA SUMMARY:")
        print("=" * 60)
        
        for sensor, data in all_data.items():
            if data is not None:
                print(f"{sensor.upper():8}: {data.shape}")
            else:
                print(f"{sensor.upper():8}: Not available")
        
        print("=" * 60)
        
        return all_data
    
    def compare_with_original(self, original_data_info):
        """
        Compare loaded .dat data with original processing info
        
        Args:
            original_data_info: dict - Original data info from process_and_save_data
        """
        print(f"\n🔍 COMPARISON WITH ORIGINAL DATA:")
        print("=" * 60)
        
        for sensor in self.sensor_folders.keys():
            try:
                dat_data = self.read_sensor_data(sensor)
                print(f"\n{sensor.upper()}:")
                print(f"  .dat file shape: {dat_data.shape}")
                
                if sensor in original_data_info and original_data_info[sensor] is not None:
                    original_shape = original_data_info[sensor]['shape']
                    print(f"  Original shape: {original_shape}")
                    
                    if dat_data.shape == original_shape:
                        print(f"  ✅ Shapes match!")
                    else:
                        print(f"  ❌ Shapes don't match!")
                else:
                    print(f"  Original data: Not available")
                    
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")


def main():
    """
    Example usage of DatReader
    """
    # Example extracted folder
    extracted_folder = "./extracted_RAW_DATA_F24AUN05FX1U_1753868352000"
    
    # Create reader
    reader = DatReader(extracted_folder)
    
    # Print summary
    all_data = reader.print_summary()
    
    # Print detailed info for each sensor
    for sensor in ['eeg', 'imu', 'ppg', 'hr', 'spo2']:
        if all_data[sensor] is not None:
            reader.print_sensor_info(sensor)


if __name__ == "__main__":
    main() 