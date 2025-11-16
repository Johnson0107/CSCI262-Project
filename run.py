import sys
from initial_input import parse_events_file, parse_stats_file, check_consistency

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

if __name__ == "__main__":
    main()
