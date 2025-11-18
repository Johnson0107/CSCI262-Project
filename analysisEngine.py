import csv
import math
import sys

def analyze_activity_log(log_file="activity_log.csv", output_file="baseline_stats.csv"):
    """
    Reads the activity log produced by the Activity Engine, computes baseline
    statistics (mean and standard deviation) for each event, and writes them
    to a new CSV file.
    """
    print("Starting analysis phase...")
    print(f"Reading activity log from {log_file} ...")

    # Open the log and read header
    with open(log_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("Log file is empty, cannot perform analysis.")

        # First column is 'day', remaining are event names
        if not header or header[0].lower() != "day":
            print("Warning: first column is not 'day' as expected.")
        event_names = header[1:]

        # Prepare a list of values for each event
        values = {name: [] for name in event_names}

        total_days = 0
        for row in reader:
            if not row:
                continue
            total_days += 1

            # For each event column, parse the value as float
            for col_index, event_name in enumerate(event_names, start=1):
                if col_index >= len(row):
                    # malformed row; skip remaining
                    break
                cell = row[col_index].strip()
                if cell == "":
                    continue
                try:
                    v = float(cell)
                except ValueError:
                    # Non-numeric value; skip
                    continue
                values[event_name].append(v)

            # Progress feedback (not too spammy)
            if total_days == 1 or total_days % 10 == 0:
                print(f"Processed {total_days} days from log...")

    if total_days == 0:
        raise ValueError("No data rows found in log file.")

    print(f"Finished reading {total_days} days. Computing statistics...")

    # Compute mean and sample standard deviation for each event
    stats_rows = []
    for event_name in event_names:
        data = values[event_name]
        if not data:
            mean = 0.0
            std = 0.0
        else:
            n = len(data)
            mean = sum(data) / n
            if n > 1:
                var = sum((x - mean) ** 2 for x in data) / (n - 1)
                std = math.sqrt(var)
            else:
                std = 0.0

        stats_rows.append((event_name, f"{mean:.2f}", f"{std:.2f}"))

    # Write baseline statistics to output CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Event", "Mean", "StdDev"])
        writer.writerows(stats_rows)

    print(f"Baseline statistics written to {output_file}")
    print("Analysis phase complete.")


if __name__ == "__main__":
    # Allow running the analysis engine directly from the command line.
    # Usage:
    #   python analysisEngine.py activity_log.csv baseline_stats.csv
    if len(sys.argv) >= 2:
        log_file = sys.argv[1]
    else:
        log_file = "activity_log.csv"

    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = "baseline_stats.csv"

    analyze_activity_log(log_file, output_file)
