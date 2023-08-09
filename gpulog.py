import subprocess
import csv
import os
from datetime import datetime

activity_threshold = 1  # 默认值为1%
low_utilization_duration = 20  # 默认低利用率持续时间为10秒

def generate_filename(timestamp):
    return f"gpulog_{timestamp.replace(' ', '_').replace(':', '-').replace('/', '-')}.csv"

def write_to_csv(filename, data):
    if not filename:
        return

    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)  # Write header first if file doesn't exist
            writer.writerow(data)
            print(f"Started writing to {filename}")
    else:
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

def main():
    cmd = ["nvidia-smi", "--query-gpu=timestamp,pci.bus_id,utilization.gpu,utilization.memory,memory.used,temperature.gpu,temperature.memory,power.draw,ecc.errors.corrected.volatile.total,ecc.errors.corrected.aggregate.total", "--format=csv", "-l", "1"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    current_file = None
    global header
    header = None
    low_utilization_start_time = None

    try:
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            if "timestamp" in line:  # This is the header line
                header = line.split(", ")
                continue
            
            columns = line.split(", ")
            try:
                gpu_utilization = float(columns[2].replace('%', '').strip())
            except ValueError:
                # 当utilization.gpu为非数字时
                if not current_file:
                    current_file = generate_filename(columns[0])
                write_to_csv(current_file, columns)
                print(f"Finished writing to {current_file} due to non-numeric GPU utilization.")
                break

            if gpu_utilization > activity_threshold:
                if not current_file:
                    current_file = generate_filename(columns[0])
                write_to_csv(current_file, columns)
                low_utilization_start_time = None  # Reset the timer
            else:
                if not low_utilization_start_time:
                    low_utilization_start_time = datetime.now()
                elif (datetime.now() - low_utilization_start_time).seconds >= low_utilization_duration:
                    if current_file:
                        print(f"Finished writing to {current_file} due to low GPU utilization.")
                        current_file = None
                    low_utilization_start_time = None  # Reset the timer
                elif current_file:
                    write_to_csv(current_file, columns)
    finally:
        process.terminate()

if __name__ == "__main__":
    main()
