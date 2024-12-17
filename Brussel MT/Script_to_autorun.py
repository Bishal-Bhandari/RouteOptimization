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

# Interval
interval = 3600

while True:
    try:
        # Run each file
        for python_file in python_files:
            print(f"Running {python_file}...")
            subprocess.run(['python', python_file], check=True)

        # Wait for 60 min
        print(f"All scripts executed. Waiting for {interval/60} minutes...")
        time.sleep(interval)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
