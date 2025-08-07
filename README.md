# FRENZ UTILS
A comprehensive Python package for processing and analyzing Frenz wearable device data. This package provides utilities for handling EEG, IMU, PPG, HR, and SPO2 sensor data.

## 🚀 Features

- **Multi-sensor Support**: Process EEG, IMU, PPG, HR, and SPO2 data
- **Data Processing**: Extract, parse, and convert binary sensor data
- **Cross-platform**: Works on Windows, macOS
- **Data Validation**: Built-in data quality checks and validation

## 🔧 Installation

### Prerequisites

**System Requirements:**
- Python 3.9 (required for compatibility)
- macOS (Intel/Apple Silicon) or Windows 64-bit
- Valid product key (contact Earable's sales department)

### Step 1: Install Python 3.9

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python@3.9

# Or download from python.org
# https://www.python.org/downloads/release/python-3913/
```

**Windows:**
```bash
# Download from python.org
# https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe
```

### Step 2: Create Virtual Environment

```bash
# Check Python version
python3.9 --version

# Create virtual environment
python3.9 -m venv vir_name

# Activate virtual environment
# macOS:
source vir_name/bin/activate

# Windows:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\vir_name\Scripts\Activate.ps1
```

### Step 3: Install Frenz Utils

**macOS Apple Silicon (M1/M2...):**
```bash
pip install frenz_utils-1.0.0-cp39-cp39-macosx_14_0_arm64.whl
```

**macOS Intel:**
```bash
pip install frenz_utils-1.0.0-cp39-cp39-macosx_10_9_universal2.whl
```

**Windows 64-bit:**
```bash
pip install frenz_utils-1.0.0-cp39-cp39-win_amd64.whl
```

### Step 4: Verify Installation

```python
import frenz_utils
print("✅ Frenz Utils installed successfully!")
```

## 🚀 Quick Start

### 1. Convert LZMA Data to DAT Files

```python
import frenz_utils

# Process sensor data from LZMA files
from frenz_utils.process_and_save_data import ProcessAndSaveData

processor = ProcessAndSaveData(
    source_folder="./RAW_DATA_F24AUN05FX1U_1753868352000",
    product_key="your_product_key_here"
)
saved_files = processor.run_complete_workflow()
```

## 📖 Usage Examples

### Using Script Files

This repository includes several ready-to-use scripts for common tasks:

#### 1. `convert_lzma.py` - Convert LZMA Files to DAT

**Purpose:** Process raw LZMA compressed sensor data into readable DAT files.

**Usage:**
```bash
# Run the script
python convert_lzma.py
```

**Configuration:**
Edit the script to modify:
- `source_folder`: Path to your raw data folder
- `product_key`: Your valid product key

**Output:**
- Creates `extracted_[folder_name]` directory
- Generates `.dat` files for each sensor type
- Provides processing summary and statistics

#### 2. `dat_reader.py` - Read and Analyze DAT Files

**Purpose:** Read, display, and analyze processed DAT files.

**Usage:**
```python
from dat_reader import DatReader

# Initialize reader
reader = DatReader("./extracted_RAW_DATA_F24AUN05FX1U_1753868352000")

# Read all sensor data
all_data = reader.read_all_sensors()

# Get detailed info for specific sensor
reader.print_sensor_info('eeg')

# Print summary of all sensors
reader.print_summary()
```

**Features:**
- Read data from all sensor types (EEG, IMU, PPG, HR, SPO2)
- Display detailed statistics and data quality metrics
- Show timestamp ranges and data samples
- Validate data integrity

#### 3. `demo_reader.py` - Interactive Data Demo

**Purpose:** Demonstrate data reading capabilities with visual output.

**Usage:**
```bash
# Run the demo
python demo_reader.py
```

**Features:**
- Comprehensive data overview
- Sample data preview
- Data quality checks
- Performance metrics

## 🔄 Data Processing Workflow

The complete data processing workflow consists of these steps:

1. **Extract LZMA files**: Decompress compressed data files
2. **Parse Binary Data**: Convert binary sensor data to numpy arrays
3. **Process Sensors**: Handle EEG, IMU, PPG, HR, and SPO2 data
4. **Save Results**: Export processed data to .dat files
5. **Validate Data**: Check data quality and integrity
6. **Analyze Results**: Read and analyze processed data

### Example Workflow

```python
# Step 1: Process raw data
from frenz_utils.process_and_save_data import ProcessAndSaveData

processor = ProcessAndSaveData(
    source_folder="./RAW_DATA_F24AUN05FX1U_1753868352000",
    product_key="your_product_key_here"
)
saved_files = processor.run_complete_workflow()

# Step 2: Read and analyze processed data
from dat_reader import DatReader

reader = DatReader("./extracted_RAW_DATA_F24AUN05FX1U_1753868352000")
all_data = reader.read_all_sensors()

# Step 3: Convert JSON scores
from frenz_utils.json_to_csv_converter import JsonToCsvConverter

converter = JsonToCsvConverter("your_product_key_here")
csv_file = converter.convert_json_to_csv("FOCUS_SCORE.json")
```

## 📊 Supported Sensor Types

| Sensor | Data Shape | Channels | Description | Sample Rate |
|--------|------------|----------|-------------|-------------|
| **EEG** | (samples, 7) | 6 + timestamp | Brain activity signals | ~250 Hz |
| **IMU** | (samples, 4) | 3 + timestamp | Motion and orientation data | ~50 Hz |
| **PPG** | (samples, 4) | 3 + timestamp | Photoplethysmography signals | ~25 Hz |
| **HR** | (samples, 2) | 1 + timestamp | Heart rate measurements | ~1 Hz |
| **SPO2** | (samples, 2) | 1 + timestamp | Blood oxygen saturation | ~1 Hz |

### Data Format

Each sensor data file contains:
- **Timestamp**: Unix timestamp in seconds
- **Sensor Values**: Raw sensor readings
- **Data Type**: 64-bit floating point (float64)

### Example Output

```
📊 PROCESSED DATA SUMMARY:
============================================================
EEG     : 1753868351.000 → 1753872338.000 (498393 samples)
IMU     : 1753868351.000 → 1753872337.000 (199350 samples)
PPG     : 1753868351.000 → 1753872322.000 (88620 samples)
HR      : 1753868353.000 → 1753872333.000 (797 samples)
SPO2    : 1753868353.000 → 1753872333.000 (797 samples)
============================================================
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. "not a supported wheel on this platform"
**Cause:** Python version mismatch
**Solution:** Ensure you're using Python 3.9
```bash
python3.9 --version
python3.9 -m venv vir_name
source vir_name/bin/activate
```

#### 2. "No input was expected ($PIP_NO_INPUT set)"
**Cause:** Environment variable blocking pip prompts
**Solution:** Use `--yes` flag
```bash
pip uninstall frenz-utils --yes
```

#### 3. "Product key validation failed"
**Cause:** Invalid or missing product key
**Solution:** Contact Earable's sales department for a valid key

#### 4. "Source folder does not exist"
**Cause:** Incorrect path to raw data folder
**Solution:** Verify the folder path exists and contains sensor data

### Performance Optimization

- Use virtual environment with Python 3.9
- Ensure sufficient disk space for data processing
- Close other applications during large data processing
- Use SSD storage for better I/O performance

### Data Quality Checks

The tools include built-in data validation:
- NaN value detection
- Infinite value detection
- Timestamp consistency checks
- Data range validation

## 📞 Support

For technical support or product key requests:
- Contact: Earable's sales department
- Website: [https://frenzband.com/]

## 📄 License

This software is proprietary and requires a valid license to use.

---

**Note:** Always ensure you have a valid product key before using any functionality. The product key is required for data decryption and processing.
