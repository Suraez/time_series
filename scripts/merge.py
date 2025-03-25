import os
import pandas as pd
from datetime import datetime
import pytz

# Folder paths
folders = {
    "cpu": "/home/suraj/Downloads/huwaei_workload_dataset/cpu_usage_minute",
    "memory": "/home/suraj/Downloads/huwaei_workload_dataset/memory_usage_minute",
    "requests": "/home/suraj/Downloads/huwaei_workload_dataset/requests_minute"
}

def parse_index(input_str):
    try:
        i = int(input_str.strip())
        if i < 2:
            raise ValueError
        return i
    except:
        print("Please enter a valid column index >= 2")
        exit(1)

# Ask for number of days
try:
    num_days = int(input("Enter how many days of data you want to merge (max 235): "))
    if not (1 <= num_days <= 235):
        raise ValueError("Number of days must be between 1 and 235.")
except ValueError as e:
    print("Invalid input:", e)
    exit(1)

# Ask which ONE column to extract from each file
print("\nSpecify the column index (>=2) to extract from each file (just one per file).")
cpu_col = parse_index(input("CPU column index: "))
memory_col = parse_index(input("Memory column index: "))
request_col = parse_index(input("Request column index: "))

merged_data = []

for day in range(1, num_days + 1):
    day_str = f"day_{day:03}.csv"

    try:
        df_cpu = pd.read_csv(os.path.join(folders["cpu"], day_str))
        df_memory = pd.read_csv(os.path.join(folders["memory"], day_str))
        df_requests = pd.read_csv(os.path.join(folders["requests"], day_str))
    except FileNotFoundError as e:
        print(f"Missing file for day {day}: {e}")
        continue

    # Calculate start time for this day (0-based index)
    start_dt = pd.Timestamp("2023-10-01 00:00:00", tz="America/New_York") + pd.Timedelta(days=day - 1)
    timestamp_range = pd.date_range(start=start_dt, periods=len(df_cpu), freq="T")
    base_df = pd.DataFrame({"timestamp": timestamp_range.strftime("%Y-%m-%d %H:%M:%S")})



    # Select one column from each file and rename
    cpu_data = df_cpu.iloc[:, [cpu_col]].copy()
    cpu_data.columns = ["cpu"]

    memory_data = df_memory.iloc[:, [memory_col]].copy()
    memory_data.columns = ["memory"]

    request_data = df_requests.iloc[:, [request_col]].copy()
    request_data.columns = ["requests"]

    # Merge all columns
    merged = pd.concat([base_df, cpu_data, memory_data, request_data], axis=1)
    merged_data.append(merged)

# Combine all days
final_df = pd.concat(merged_data, axis=0)

# Save to file
output_file = f"merged_{num_days}_days_filtered.csv"
# Forward fill NaN values
final_df.fillna(method='ffill', inplace=True)

final_df.to_csv(output_file, index=False)
print(f"\n✅ Final data saved to: {output_file}")
