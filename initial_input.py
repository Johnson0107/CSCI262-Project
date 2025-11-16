from dataclasses import dataclass

# Class to store event definition from Events.txt
@dataclass
class Event:
    name: str
    type: str
    min: float
    max: float
    weight: int

# Class to store statistical data from Stats.txt
@dataclass
class EventStats:
    mean: float
    std_dev: float

# Function to parse Events.txt and return a dictionary of Event objects
def parse_events_file(filepath):
    events = {}
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        num_events = int(lines[0])
        # Process each line to extract event details
        for line in lines[1:]:
            parts = line.split(':')
            name = parts[0]
            event_type = parts[1]
            min_val = float(parts[2]) if parts[2] else 0
            max_val = float(parts[3]) if parts[3] else None
            weight = int(parts[4]) if parts[4] else 1
            events[name] = Event(name, event_type, min_val, max_val, weight)
        # Check if actual number of events matches declared number
        if len(events) != num_events:
            raise ValueError(f"Event count mismatch: declared {num_events}, found {len(events)}")

    return events

# Function to parse Stats.txt and return a dictionary of EventStats
def parse_stats_file(filepath):
    stats = {}
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        num_events = int(lines[0])
        # Process each line to extract statistical data
        for line in lines[1:]:
            parts = line.split(':')
            name = parts[0]
            mean = float(parts[1])
            std_dev = float(parts[2])
            stats[name] = EventStats(mean, std_dev)
        # Check if actual number of stats matches declared number
        if len(stats) != num_events:
            raise ValueError(f"Stats count mismatch: declared {num_events}, found {len(stats)}")

    return stats
# Function to check consistency between Events.txt and Stats.txt
def check_consistency(events, stats):
    errors = []
    for name in events:
        if name not in stats:
            errors.append(f"{name} is in Events.txt but not in Stats.txt")
        elif events[name].type == 'D' and not stats[name].mean.is_integer():
            errors.append(f"Discrete event {name} has non-integer mean: {stats[name].mean}")
    for name in stats:
        if name not in events:
            errors.append(f"[{name} is in Stats.txt but not in Events.txt")
    return errors
