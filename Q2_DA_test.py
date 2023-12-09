import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the detection file 'Q2_detction_file_2.csv'
file_path = 'Q2_detection_file_2.csv'
data = pd.read_csv(file_path)

# Step 2: Plots the distance of the detected object as a function of time
plt.figure(figsize=(10, 6))
plt.plot(data['time_sec'], data['rw_kinematic_point_z'], label='Distance vs. Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Distance (meters)')
plt.title('Object Distance vs. Time')
plt.legend()
plt.show()

# Step 3: Detect and remove invalid distance measurements
# Assuming invalid distances are those less than a certain threshold (adjust as needed)
invalid_distance_threshold = 0.0
valid_data = data[data['rw_kinematic_point_z'] >= invalid_distance_threshold]

#Plot the same graph after the removal of bad readings
plt.figure(figsize=(10, 6))
plt.plot(valid_data['time_sec'], valid_data['rw_kinematic_point_z'], label='Valid Distance vs. Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Distance (meters)')
plt.title('Valid Object Distance vs. Time')
plt.legend()
plt.show()

# Step 5: Calculate the velocity of the object
# Assuming constant velocity is sufficient, velocity = change in distance / change in time
valid_data['velocity_z'] = valid_data['rw_kinematic_point_z'].diff() / valid_data['time_sec'].diff()

# Just fot test: Plots the velocity as a function of time
plt.figure(figsize=(10, 6))
plt.plot(valid_data['time_sec'][:-1], valid_data['velocity_z'][:-1], label='Velocity vs. Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Velocity (m/s)')
plt.title('Object Velocity vs. Time')
plt.legend()
plt.show()

# Bonus Question: Handle the file 'Q2_detction_file_2_bonus.csv'
bonus_file_path = 'Q2_detection_file_2_bonus.csv'
bonus_data = pd.read_csv(bonus_file_path)

# Function to detect and remove outliers
def remove_outliers(data, column, threshold=2):
    z_scores = (data[column] - data[column].mean()) / data[column].std()
    valid_data = data[abs(z_scores) < threshold]
    return valid_data

# Remove outliers from bonus data
cleaned_bonus_data = remove_outliers(bonus_data, 'rw_kinematic_point_z')

# Re-plot the graph from question 2 with cleaned bonus data
plt.figure(figsize=(10, 6))
plt.plot(cleaned_bonus_data['time_sec'], cleaned_bonus_data['rw_kinematic_point_z'], label='Cleaned Bonus Data')
plt.xlabel('Time (seconds)')
plt.ylabel('Distance (meters)')
plt.title('Cleaned Bonus Object Distance Over Time')
plt.legend()
plt.show()
