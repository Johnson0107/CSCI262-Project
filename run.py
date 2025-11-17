import sys
import random #For 2
import csv #For 2
from initial_input import parse_events_file, parse_stats_file, check_consistency
from activityEngine import simulate_activity

def main():
    if len(sys.argv) != 4:
        print("Usage: python run.py Events.txt Stats.txt Days")
        return

    events_file = sys.argv[1]
    stats_file = sys.argv[2]
    try:
        days = int(sys.argv[3])
    except ValueError:
        print("Days must be an integer.")
        return

    # Load input files
    print("Loading event definitions...")
    events = parse_events_file(events_file)
    stats = parse_stats_file(stats_file)

    # Print loaded info
    print("Loaded Events:")
    for e in events.values():
        print(f"  - {e}")

    print("\nLoaded Stats:")
    for k, s in stats.items():
        print(f"  - {k}: {s}")

    # Check consistency
    print("\nChecking consistency...")
    errors = check_consistency(events, stats)
    if errors:
        print("Issues found:")
        for err in errors:
            print(err)
        return
    else:
        print("All files consistent. Proceeding to activity simulation.")

    if len(sys.argv) != 4:
        print("Usage: python activityEngine.py Events.txt Stats.txt DAYS")
        return

    events_file = sys.argv[1]
    stats_file = sys.argv[2]
    try:
        days = int(sys.argv[3])
    except ValueError:
        print("DAYS must be an integer.")
        return

    # Parse input files
    events = parse_events_file(events_file)
    stats = parse_stats_file(stats_file)

    # Check consistency before simulating
    errors = check_consistency(events, stats)
    if errors:
        print("Inconsistencies found; aborting simulation:")
        for err in errors:
            print(" -", err)
        return

    # Actually run the simulation for the requested number of days
    random.seed(0)  # For reproducible results
    simulate_activity(events, stats, days, log_file="activity_log.csv")


if __name__ == "__main__":
    main()