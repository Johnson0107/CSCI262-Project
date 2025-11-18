import csv
import random
from initial_input import parse_events_file, parse_stats_file, check_consistency
from activityEngine import simulate_activity

def load_baseline(baseline_file):
    baseline = {}

    with open(baseline_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header: Event,Mean,StdDev

        for row in reader:
            if len(row) < 3:
                continue
            name = row[0]
            mean = float(row[1])
            std = float(row[2])
            baseline[name] = (mean, std)

    return baseline

# Helper: Read daily values from log file
def load_log_values(log_file):
    days = {}
    with open(log_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        event_names = header[1:]  # skip 'day'

        for row in reader:
            day = int(row[0])
            values = list(map(float, row[1:]))
            days[day] = dict(zip(event_names, values))

    return days

# Compute anomaly score for each day
def compute_anomaly_scores(events, baseline, live_days):
    scores = {}

    # Threshold = 2 * total weight
    total_weight = sum(ev.weight for ev in events.values())
    threshold = 2 * total_weight

    for day, events_data in live_days.items():
        score = 0
        for name, daily_value in events_data.items():
            if name not in baseline:
                continue

            mean_b, std_b = baseline[name]

            if std_b == 0:
                z = 0
            else:
                z = abs(daily_value - mean_b) / std_b

            weight = events[name].weight
            score += z * weight

        scores[day] = (score, threshold)

    return scores

#  ALERT ENGINE MAIN FUNCTION
# ---------------------------------------------
def alert_engine():
    print("=== ALERT ENGINE STARTED ===")

    # Load fixed event definitions and baseline
    events = parse_events_file("Events.txt")

    # Ensure baseline exists
    baseline_file = "baseline_stats.csv"
    print(f"Loading baseline statistics from {baseline_file}...")
    baseline = load_baseline(baseline_file)

    # Interactive loop
    while True:
        print("\nEnter a live Stats file for analysis (or 'q' to quit):")
        stats_file = input("Live Stats file: ").strip()

        if stats_file.lower() == "q":
            print("Exiting Alert Engine...")
            break

        # Validate Stats file
        try:
            live_stats = parse_stats_file(stats_file)
        except Exception as e:
            print(f"Error loading stats file: {e}")
            continue

        print("\nNumber of days to generate (live data):")
        try:
            days = int(input("Days: "))
        except:
            print("Invalid number. Try again.")
            continue

        # Check consistency first
        errors = check_consistency(events, live_stats)
        if errors:
            print("Inconsistencies found:")
            for e in errors:
                print(" -", e)
            continue

        # Generate live data
        live_log = "live_log.csv"
        print("\nGenerating live data...")
        random.seed(1)  # new seed for live simulation
        simulate_activity(events, live_stats, days, log_file=live_log)

        # Load live data
        live_days = load_log_values(live_log)

        # Compute anomaly scores
        print("\nComputing anomaly scores...")
        scores = compute_anomaly_scores(events, baseline, live_days)

        # Display results
        print("\n=== DAILY ALERT RESULTS ===")
        for day in sorted(scores.keys()):
            score, threshold = scores[day]
            if score >= threshold:
                print(f"Day {day}: ALERT (Score={score:.2f} Threshold={threshold})")
            else:
                print(f"Day {day}: OK (Score={score:.2f} Threshold={threshold})")

        print("\n=== End of this analysis ===")
        print("You may enter another Stats file or 'q' to quit.\n")


# ---------------------------------------------
# Entry Point
# ---------------------------------------------
if __name__ == "__main__":
    alert_engine()
