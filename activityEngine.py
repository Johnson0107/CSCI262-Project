import random
import csv
import sys

from initial_input import parse_events_file, parse_stats_file, check_consistency

# For generating one day's value for a single event
def generate_value_for_event(event, stat):
    # Base sample from a normal (Gaussian) distribution
    if stat.std_dev == 0:
        x = stat.mean
    else:
        x = random.gauss(stat.mean, stat.std_dev)

    # Clamp to min / max if they are defined
    if event.min is not None:
        x = max(x, event.min)
    if event.max is not None:
        x = min(x, event.max)

    if event.type == 'D':  # Discrete event
        x = int(round(x))
        # Re-enforce bounds after rounding
        if event.min is not None:
            x = max(x, int(event.min))
        if event.max is not None:
            x = min(x, int(event.max))
    else:                  # Continuous event
        x = round(x, 2)    # 2 decimal places as required

    return x


# Simulate multiple days and log to CSV
def simulate_activity(events, stats, days, log_file="activity_log.csv"):
    # For consistent column order
    event_names = sorted(events.keys())

    with open(log_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Header row: day, then each event name
        writer.writerow(["day"] + event_names)

        # Simple progress feedback interval (≈ 10 updates)
        progress_step = max(1, days // 10)

        for day in range(1, days + 1):
            row = [day]
            for name in event_names:
                event = events[name]
                stat = stats[name]
                value = generate_value_for_event(event, stat)
                row.append(value)
            writer.writerow(row)

            # Progress feedback without excessive detail
            if day == 1 or day == days or day % progress_step == 0:
                print(f"Simulated day {day}/{days}")

    print(f"Finished simulation. Logged {days} days to {log_file}")

