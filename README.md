# GPS Spoofing Detection System

## Overview
A 2-week autonomous navigation security project that detects GPS spoofing attacks by comparing GPS-derived velocity with INS (Inertial Navigation System) velocity data.

## Project Structure
- `generate_navigation_data.py` - Creates synthetic navigation data with spoofing event
- `gps_spoofing_detector.py` - Analyzes data and detects spoofing anomalies
- `navigation_data.csv` - Generated synthetic navigation data
- `navigation_analysis_results.csv` - Analysis results with GPS velocities
- `requirements.txt` - Python dependencies

## Step-by-Step Instructions

### 1. Setup Environment
```bash
# Install required packages
pip install -r requirements.txt
```

### 2. Generate Synthetic Data
```bash
# Run the data generator
python generate_navigation_data.py
```
**Expected Output:**
- Creates `navigation_data.csv` with 100 seconds of vehicle data
- Shows spoofing event at T=50s where GPS coordinates jump ~1km
- INS velocity remains steady at 15 m/s throughout

### 3. Run Detection Analysis
```bash
# Run the spoofing detector
python gps_spoofing_detector.py
```
**Expected Output:**
- Reads navigation data
- Calculates GPS velocity between consecutive points
- Compares GPS velocity vs INS velocity
- Prints alert when difference > 20 m/s threshold
- Saves results to `navigation_analysis_results.csv`

## Key Features

### Data Generation (Week 1)
- **Duration:** 100 seconds of vehicle movement
- **Columns:** Timestamp, GPS_Lat, GPS_Long, INS_Velocity
- **Spoofing Event:** At T=50s, GPS coordinates jump ~1km while INS velocity stays normal
- **Sampling Rate:** 1 Hz (1 second intervals)

### Detection Logic (Week 2)
- **Geodesic Distance Calculation:** Uses geopy library for accurate Earth surface distances
- **Velocity Comparison:** GPS-derived velocity vs INS velocity
- **Threshold:** 20 m/s difference triggers alert
- **Alert Format:** `[ALERT] Anomaly Detected at T={timestamp}`

## Presentation Points for Your Presenter

### 1. Problem Statement
- GPS spoofing is a critical threat to autonomous navigation
- Attackers can broadcast false GPS signals to manipulate vehicle position
- Need real-time detection methods to ensure navigation safety

### 2. Our Solution Approach
- **Multi-sensor fusion:** Compare GPS with INS (Inertial Navigation System)
- **Physics-based detection:** Real vehicles can't teleport - sudden position jumps indicate spoofing
- **Threshold-based alerting:** Simple, effective, and computationally efficient

### 3. Demonstration Flow
1. **Show normal movement:** First 50 seconds show consistent GPS/INS data
2. **Introduce spoofing:** At T=50s, GPS jumps while INS stays steady
3. **Detection in action:** System immediately flags the anomaly
4. **Results:** Clear alert message with timestamp and velocity differences

### 4. Key Metrics
- **Detection Time:** < 1 second after spoofing event
- **False Positive Rate:** Low (only triggers on impossible movements)
- **Computational Cost:** Minimal (simple velocity calculations)

### 5. Future Extensions
- Real-time implementation for live navigation systems
- Machine learning for more sophisticated attack patterns
- Integration with vehicle control systems for automatic mitigation

## Technical Details

### Spoofing Detection Algorithm
```
For each consecutive GPS point:
    1. Calculate geodesic distance between points
    2. Compute GPS velocity = distance / time_interval
    3. Compare with INS velocity
    4. If |GPS_velocity - INS_velocity| > threshold:
           Trigger spoofing alert
```

### Why This Works
- **Physical constraints:** Vehicles can't instantly change position
- **Sensor independence:** GPS and INS use different physical principles
- **Attack signature:** Spoofing creates impossible velocity discrepancies

## Quick Test Commands
```bash
# Test everything in sequence
python generate_navigation_data.py && python gps_spoofing_detector.py
```

This will generate the spoofed data and immediately detect the anomaly, demonstrating the complete detection system in action.
"# GPS_Spoofing_Jamming_Detection" 
