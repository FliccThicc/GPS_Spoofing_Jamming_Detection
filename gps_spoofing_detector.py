import pandas as pd
import numpy as np
from geopy.distance import geodesic
from datetime import datetime

def calculate_gps_velocity(df):
    """
    Calculate velocity between consecutive GPS points using geodesic distance.
    """
    gps_velocities = [0]  # First point has no previous point
    
    for i in range(1, len(df)):
        # Get consecutive coordinates
        prev_point = (df.iloc[i-1]['GPS_Lat'], df.iloc[i-1]['GPS_Long'])
        curr_point = (df.iloc[i]['GPS_Lat'], df.iloc[i]['GPS_Long'])
        
        # Calculate geodesic distance in meters
        distance = geodesic(prev_point, curr_point).meters
        
        # Calculate velocity (m/s) - assuming 1 second intervals
        velocity = distance / 1.0
        gps_velocities.append(velocity)
    
    return gps_velocities

def detect_spoofing_anomalies(df, threshold=20.0):
    """
    Detect GPS spoofing by comparing GPS calculated velocity with INS velocity.
    """
    # Calculate GPS velocities
    gps_velocities = calculate_gps_velocity(df)
    df['GPS_Calculated_Velocity'] = gps_velocities
    
    # Detect anomalies
    anomalies = []
    
    for i in range(1, len(df)):
        gps_vel = df.iloc[i]['GPS_Calculated_Velocity']
        ins_vel = df.iloc[i]['INS_Velocity']
        
        velocity_diff = abs(gps_vel - ins_vel)
        
        if velocity_diff > threshold:
            timestamp = df.iloc[i]['Timestamp']
            anomalies.append({
                'timestamp': timestamp,
                'gps_velocity': gps_vel,
                'ins_velocity': ins_vel,
                'difference': velocity_diff
            })
            print(f'[ALERT] Anomaly Detected at T={timestamp}')
    
    return anomalies, df

def main():
    print("GPS Spoofing Detection Analysis")
    print("=" * 40)
    
    try:
        # Read navigation data
        print("Reading navigation_data.csv...")
        df = pd.read_csv('navigation_data.csv')
        
        # Convert timestamp to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(df['Timestamp']):
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        print(f"Loaded {len(df)} data points")
        print("\nData preview:")
        print(df.head())
        
        # Detect anomalies
        print("\nAnalyzing for GPS spoofing anomalies...")
        anomalies, df_with_gps_vel = detect_spoofing_anomalies(df, threshold=20.0)
        
        # Summary
        print(f"\nAnalysis complete!")
        print(f"Total anomalies detected: {len(anomalies)}")
        
        if anomalies:
            print("\nAnomaly details:")
            for anomaly in anomalies:
                print(f"  Time: {anomaly['timestamp']}")
                print(f"  GPS Velocity: {anomaly['gps_velocity']:.2f} m/s")
                print(f"  INS Velocity: {anomaly['ins_velocity']:.2f} m/s")
                print(f"  Difference: {anomaly['difference']:.2f} m/s")
                print()
        
        # Save results with GPS velocities
        df_with_gps_vel.to_csv('navigation_analysis_results.csv', index=False)
        print("Analysis results saved to navigation_analysis_results.csv")
        
    except FileNotFoundError:
        print("Error: navigation_data.csv not found!")
        print("Please run generate_navigation_data.py first to create the data file.")
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()
