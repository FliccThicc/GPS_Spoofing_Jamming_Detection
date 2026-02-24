import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_navigation_data():
    """
    Generate synthetic navigation data for GPS spoofing detection system.
    Creates 100 seconds of vehicle movement with a spoofing event at T=50s.
    """
    
    # Time parameters
    duration_seconds = 100
    sampling_rate = 1  # 1 Hz sampling
    timestamps = [datetime.now() + timedelta(seconds=i) for i in range(duration_seconds)]
    
    # Initial position (starting point)
    initial_lat = 40.7128  # NYC coordinates
    initial_lon = -74.0060
    
    # Vehicle parameters
    steady_velocity = 15.0  # m/s (about 33 mph)
    
    # Initialize arrays
    gps_lats = []
    gps_lons = []
    ins_velocities = []
    
    current_lat = initial_lat
    current_lon = initial_lon
    
    for i, timestamp in enumerate(timestamps):
        # INS velocity remains steady throughout
        ins_velocities.append(steady_velocity)
        
        if i == 50:
            # Spoofing event: GPS coordinates jump impossibly far
            # Jump approximately 1 km away (impossible at steady velocity)
            gps_lats.append(current_lat + 0.009)  # ~1km north
            gps_lons.append(current_lon + 0.009)  # ~1km east
        elif i > 50:
            # After spoofing, continue from spoofed position with normal movement
            # Calculate movement based on steady velocity
            distance = steady_velocity * 1  # 1 second interval
            # Convert distance to degrees (approximate)
            lat_change = distance / 111320  # meters per degree latitude
            lon_change = distance / (111320 * np.cos(np.radians(current_lat)))
            
            current_lat += lat_change * 0.1  # Moving northeast
            current_lon += lon_change * 0.1
            
            gps_lats.append(current_lat)
            gps_lons.append(current_lon)
        else:
            # Normal movement before spoofing event
            distance = steady_velocity * 1  # 1 second interval
            # Convert distance to degrees (approximate)
            lat_change = distance / 111320  # meters per degree latitude
            lon_change = distance / (111320 * np.cos(np.radians(current_lat)))
            
            current_lat += lat_change * 0.1  # Moving northeast
            current_lon += lon_change * 0.1
            
            gps_lats.append(current_lat)
            gps_lons.append(current_lon)
    
    # Create DataFrame
    navigation_df = pd.DataFrame({
        'Timestamp': timestamps,
        'GPS_Lat': gps_lats,
        'GPS_Long': gps_lons,
        'INS_Velocity': ins_velocities
    })
    
    return navigation_df

def main():
    print("Generating synthetic navigation data...")
    
    # Generate data
    nav_data = generate_navigation_data()
    
    # Save to CSV
    nav_data.to_csv('navigation_data.csv', index=False)
    
    print(f"Generated {len(nav_data)} data points")
    print("Data saved to navigation_data.csv")
    
    # Display first few and last few rows
    print("\nFirst 5 rows:")
    print(nav_data.head())
    print("\nLast 5 rows:")
    print(nav_data.tail())
    
    # Highlight spoofing event
    print(f"\nSpoofing event at T=50s:")
    print(f"  Before: Lat={nav_data.iloc[49]['GPS_Lat']:.6f}, Lon={nav_data.iloc[49]['GPS_Long']:.6f}")
    print(f"  After:  Lat={nav_data.iloc[50]['GPS_Lat']:.6f}, Lon={nav_data.iloc[50]['GPS_Long']:.6f}")

if __name__ == "__main__":
    main()
