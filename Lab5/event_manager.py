"""Manage events, guest registrations, and seating capacity."""

import json
import secrets
from datetime import date

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """Create an event and return its details."""
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    if guests is None:
        guests = []

    events[event_name] = {
        "venue": venue,
        "capacity": capacity,
        "guests": list(guests),
    }
    return events[event_name]


def register_guest(event_name, guest):
    """Register a guest if the event has space."""
    event = events.get(event_name)
    if event is None:
        print("No such event:", event_name)
        return False

    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False

    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """Return the number of available seats."""
    if event_name not in events:
        raise KeyError(f"Unknown event: {event_name}")

    event = events[event_name]
    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """Return whether an event is upcoming or completed."""
    if event_date >= date.today():
        return "Upcoming"
    return "Completed"


def guest_report(event_name, sort_order="asc"):
    """Return guest names in the requested alphabetical order."""
    if event_name not in events:
        raise KeyError(f"Unknown event: {event_name}")
    if sort_order not in {"asc", "desc"}:
        raise ValueError("sort_order must be asc or desc")

    names = sorted(
        events[event_name]["guests"],
        reverse=sort_order == "desc",
    )
    return ", ".join(names)


def save_events(file_name="events.json"):
    """Save event data as JSON."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=2)


def load_events(file_name="events.json"):
    """Load event data from JSON."""
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Invalid event data.")
    return data


def print_badges(event_name):
    """Display the contents of an event's badge file."""
    allowed = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    )
    if not event_name or any(
        char not in allowed for char in event_name
    ):
        raise ValueError("Invalid event name.")

    badge_file = f"badges_{event_name}.txt"
    with open(badge_file, "r", encoding="utf-8") as file:
        print(file.read())


def main():
    """Demonstrate event creation and guest registration."""
    events.clear()

    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop", 2)

    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")

    print("Seats left at Tech Meetup:", seats_left("Tech Meetup"))
    print(
        "Seats left at Alumni Dinner:",
        seats_left("Alumni Dinner"),
    )
    print("Tech Meetup guests:", guest_report("Tech Meetup"))
    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print(
        "Alumni Dinner is",
        event_status(date(2020, 5, 1)),
    )

    guests = events["Tech Meetup"]["guests"]
    if guests:
        print("Lucky draw winner:", secrets.choice(guests))

    save_events()
    restored = load_events()
    print("Events restored from file:", len(restored))

    venues = [
        event["venue"]
        for event in restored.values()
    ]
    print("Venues:", venues)


if __name__ == "__main__":
    main()
