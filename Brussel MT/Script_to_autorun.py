import time
import subprocess

# Python files to run
python_files = [
    'Shape_file.py',
    'Vehicle_distance.py',
    'Vehicle_position.py',
    'Vehicle_speed.py',
    'Vehicle_Stops.py'
]

# Interval in seconds (1 hour)
interval = 3600  # 60 minutes * 60 seconds

while True:
    try:
        # Run each Python file in the list
        for python_file in python_files:
            print(f"Running {python_file}...")
            subprocess.run(['python', python_file], check=True)

        # Wait for 1 hour before running the scripts again
        print(f"All scripts executed. Waiting for {interval/60} minutes...")
        time.sleep(interval)  # Wait for 1 hour (3600 seconds)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
