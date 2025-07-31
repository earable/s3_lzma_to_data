# S3 LZMA to Data Processing Pipeline

## 📖 Overview

A comprehensive data processing pipeline for extracting, processing, and analyzing sensor data from `.lzma` files. This project provides tools to decompress LZMA files, load sensor data, process and reshape the data, and save it to binary `.dat` files for further analysis.

## 🚀 Features

### Core Processing
- ✅ **LZMA Decompression**: Extract `.lzma` files from local folders
- ✅ **Multi-Sensor Support**: Process EEG, IMU, PPG, HR, and SPO2 data
- ✅ **Data Reshaping**: Automatically reshape data based on sensor type
- ✅ **Timestamp Handling**: Proper timestamp processing and sorting
- ✅ **Binary Export**: Save processed data to `.dat` files

### Data Reading & Analysis
- ✅ **Binary Data Reader**: Read and analyze `.dat` files
- ✅ **Data Quality Checks**: Validate data integrity and consistency
- ✅ **Visual Data Display**: Comprehensive data overview and statistics
- ✅ **Sample Preview**: View sample data with timestamps

### Workflow Automation
- ✅ **Complete Pipeline**: End-to-end processing from raw files to analysis
- ✅ **Idempotent Processing**: Skip processing if files already exist
- ✅ **Error Handling**: Robust error handling and reporting
- ✅ **Progress Tracking**: Real-time progress updates

## 📁 Project Structure

```
s3_lzma_to_data/
├── data_loader.pyc              # Core data loading and processing functions
├── binary_loader.pyc            # Binary data parsing for different sensors
├── process_and_save_data.py    # Main processing and saving pipeline
├── dat_reader.py              # Data reader for .dat files
├── demo_reader.py             # Demo script with visual data display
├── README.md                  # Main project documentation
└── RAW_DATA_F25AUZ05FX1U_1753868352000/  # Sample data folder
    ├── EEG2/                  # EEG sensor data
    ├── IMU2/                  # IMU sensor data
    ├── PPG2/                  # PPG sensor data
    ├── HR/                    # Heart rate data
    └── SPO2/                  # Blood oxygen data
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation
```bash
# Clone or download the project
git clone <repository-url>
cd s3_lzma_to_data

# Install required packages
pip install -r requirements.txt

# Or install individually
pip install numpy pandas
```

### Quick Start
```bash
# Clone or download the project
cd s3_lzma_to_data

# Process your data
python process_and_save_data.py

# Read and analyze the processed data
python demo_reader.py
```

## 📊 Supported Sensor Types

| Sensor | Data Shape | Channels | Description |
|--------|------------|----------|-------------|
| **EEG** | (samples, 7) | 6 + timestamp | Brain activity signals |
| **IMU** | (samples, 4) | 3 + timestamp | Motion and orientation data |
| **PPG** | (samples, 4) | 3 + timestamp | Photoplethysmography signals |
| **HR** | (samples, 2) | 1 + timestamp | Heart rate measurements |
| **SPO2** | (samples, 2) | 1 + timestamp | Blood oxygen saturation |

## 🎯 Usage Examples

### 1. Process Raw Data
```python
from process_and_save_data import ProcessAndSaveData

# Initialize processor
source_folder = "/path/to/your/raw/data"
processor = ProcessAndSaveData(source_folder)

# Run complete workflow
saved_files = processor.run_complete_workflow()
```

### 2. Read Processed Data
```python
from dat_reader import DatReader

# Initialize reader
extracted_folder = "./extracted_RAW_DATA_F25AUZ05FX1U_1753868352000"
reader = DatReader(extracted_folder)

# Read specific sensor data
eeg_data = reader.read_sensor_data('eeg')
print(f"EEG shape: {eeg_data.shape}")

# Read all sensors
all_data = reader.read_all_sensors()

# Print detailed information
reader.print_sensor_info('hr')
```

### 3. Demo Script
```bash
# Run the demo to see all data
python demo_reader.py
```

## 🔍 Data Processing Pipeline

### Step 1: LZMA Extraction
- Extract `.lzma` files from source folders
- Maintain folder structure in extracted directory
- Handle multiple sensor types automatically

### Step 2: Data Loading
- Load binary data using appropriate parsers
- Apply sensor-specific processing
- Handle timestamps and data validation

### Step 3: Data Export
- Save processed data to `.dat` files
- Maintain folder structure
- Use binary format for efficiency

## 📈 Data Quality Features

### Automatic Checks
- ✅ **NaN Detection**: Identify missing or invalid data
- ✅ **Infinite Value Check**: Detect overflow or calculation errors
- ✅ **Timestamp Consistency**: Verify chronological order
- ✅ **Data Range Validation**: Check for expected value ranges

### Statistics & Analysis
- 📊 **Sample Counts**: Total samples per sensor
- 📊 **Time Duration**: Recording duration and intervals
- 📊 **Value Ranges**: Min/max/mean statistics
- 📊 **Sampling Rates**: Calculated from timestamp intervals

## 🛠️ API Reference

### ProcessAndSaveData Class
```python
class ProcessAndSaveData:
    def __init__(self, source_folder)
    def process_all_sensors()
    def save_to_dat_files()
    def print_summary()
    def run_complete_workflow()
```

### DatReader Class
```python
class DatReader:
    def __init__(self, extracted_folder)
    def read_sensor_data(sensor)
    def read_all_sensors()
    def print_sensor_info(sensor)
    def print_summary()
```

## 📦 Dependencies

### Required Packages
- **numpy>=1.21.0**: For numerical computing and array operations
- **pandas>=1.3.0**: For data manipulation and analysis

## ⚠️ Important Notes

### Data Format
- All data is saved as `float64` for precision
- Timestamps are stored in the last column
- Binary format for efficient storage and reading

### File Naming
- Extracted folders: `./extracted_{source_folder_name}`
- Data files: `{sensor}_full_data.dat`
- Maintains original folder structure

### Error Handling
- Graceful handling of missing files
- Skip processing if files already exist
- Detailed error reporting and logging

## 🔧 Troubleshooting

### Common Issues
1. **File Not Found**: Check source folder path
2. **Permission Errors**: Ensure write access to target directory
3. **Memory Issues**: Process sensors individually for large datasets
4. **Timestamp Errors**: Verify data integrity in source files

### Debug Mode
```python
# Enable verbose output
processor = ProcessAndSaveData(source_folder)
processor.process_all_sensors()  # Detailed progress output
```

## 📄 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the project.

---

**Note**: This pipeline is designed for processing biomedical sensor data and includes specific optimizations for EEG, IMU, PPG, HR, and SPO2 data types.
