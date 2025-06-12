from datetime import date, datetime, timedelta
from typing import Dict

# Hardcoded host schedule with mock data
# Format: {date: {time: status}} where status is either "available" or a meeting name
HOST_SCHEDULE: Dict[str, Dict[str, str]] = {
    "2025-06-13": {
        "08:00": "available",
        "09:00": "Team Standup",
        "10:00": "available",
        "11:00": "Client Review",
        "12:00": "available",
        "13:00": "Lunch Break",
        "14:00": "Project Planning",
        "15:00": "available",
        "16:00": "available",
        "17:00": "1-on-1 with Sarah",
        "18:00": "available",
        "19:00": "available",
        "20:00": "available"
    },
    "2025-06-14": {
        "08:00": "available",
        "09:00": "available",
        "10:00": "Department Meeting",
        "11:00": "Department Meeting",
        "12:00": "available",
        "13:00": "Lunch Break",
        "14:00": "available",
        "15:00": "Code Review",
        "16:00": "available",
        "17:00": "available",
        "18:00": "available",
        "19:00": "available",
        "20:00": "available"
    },
    "2025-06-15": {
        "08:00": "available",
        "09:00": "available",
        "10:00": "available",
        "11:00": "available",
        "12:00": "Weekend Planning",
        "13:00": "available",
        "14:00": "available",
        "15:00": "available",
        "16:00": "Family Time",
        "17:00": "Family Time",
        "18:00": "available",
        "19:00": "available",
        "20:00": "available"
    },
    "2025-06-16": {
        "08:00": "available",
        "09:00": "available",
        "10:00": "available",
        "11:00": "Brunch with Team",
        "12:00": "Brunch with Team",
        "13:00": "available",
        "14:00": "available",
        "15:00": "available",
        "16:00": "available",
        "17:00": "available",
        "18:00": "available",
        "19:00": "available",
        "20:00": "available"
    },
    "2025-06-17": {
        "08:00": "available",
        "09:00": "Sprint Planning",
        "10:00": "Sprint Planning",
        "11:00": "available",
        "12:00": "available",
        "13:00": "Lunch Break",
        "14:00": "Technical Discussion",
        "15:00": "available",
        "16:00": "available",
        "17:00": "available",
        "18:00": "Evening Workshop",
        "19:00": "Evening Workshop",
        "20:00": "available"
    },
    "2025-06-18": {
        "08:00": "available",
        "09:00": "available",
        "10:00": "Client Call",
        "11:00": "available",
        "12:00": "available",
        "13:00": "Lunch Break",
        "14:00": "available",
        "15:00": "Performance Review",
        "16:00": "available",
        "17:00": "available",
        "18:00": "available",
        "19:00": "available",
        "20:00": "available"
    },
    "2025-06-19": {
        "08:00": "available",
        "09:00": "Daily Standup",
        "10:00": "available",
        "11:00": "available",
        "12:00": "available",
        "13:00": "Lunch Break",
        "14:00": "available",
        "15:00": "available",
        "16:00": "Team Retrospective",
        "17:00": "available",
        "18:00": "available",
        "19:00": "available",
        "20:00": "available"
    }
}

# Print the schedule when module loads (for debugging)
print("Host availability loaded:")
for date_str, slots in HOST_SCHEDULE.items():
    available_times = [time for time, status in slots.items() if status == "available"]
    print(f"{date_str}: {len(available_times)} available slots - {', '.join(available_times[:3])}...")


def list_host_availability(date: str) -> dict:
    """
    Lists the available and booked time slots for the host on a given date.

    Args:
        date: The date to check, in YYYY-MM-DD format.

    Returns:
        A dictionary with the status and the detailed schedule for the day.
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid date format. Please use YYYY-MM-DD.",
        }

    daily_schedule = HOST_SCHEDULE.get(date)
    if not daily_schedule:
        return {
            "status": "success",
            "message": f"The host is not available on {date}.",
            "schedule": {},
        }

    available_slots = [
        time for time, status in daily_schedule.items() if status == "available"
    ]
    booked_slots = {
        time: meeting for time, meeting in daily_schedule.items() if meeting != "available"
    }

    return {
        "status": "success",
        "message": f"Host availability for {date}.",
        "available_slots": available_slots,
        "booked_slots": booked_slots,
    }


def book_host_meeting(
    date: str, start_time: str, end_time: str, meeting_name: str
) -> dict:
    """
    Books a meeting with the host for a given date and time range.

    Args:
        date: The date of the meeting, in YYYY-MM-DD format.
        start_time: The start time of the meeting, in HH:MM format.
        end_time: The end time of the meeting, in HH:MM format.
        meeting_name: The name/description for the meeting.

    Returns:
        A dictionary confirming the booking or providing an error.
    """
    try:
        start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid date or time format. Please use YYYY-MM-DD and HH:MM.",
        }

    if start_dt >= end_dt:
        return {"status": "error", "message": "Start time must be before end time."}

    if date not in HOST_SCHEDULE:
        return {"status": "error", "message": f"The host is not available on {date}."}

    if not meeting_name:
        return {
            "status": "error",
            "message": "Cannot book a meeting without a meeting name.",
        }

    required_slots = []
    current_time = start_dt
    while current_time < end_dt:
        required_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(hours=1)

    daily_schedule = HOST_SCHEDULE.get(date, {})
    for slot in required_slots:
        if daily_schedule.get(slot, "booked") != "available":
            existing_meeting = daily_schedule.get(slot)
            return {
                "status": "error",
                "message": f"The time slot {slot} on {date} is already booked for {existing_meeting}.",
            }

    for slot in required_slots:
        HOST_SCHEDULE[date][slot] = meeting_name

    return {
        "status": "success",
        "message": f"Success! The meeting '{meeting_name}' has been booked from {start_time} to {end_time} on {date}.",
    }


def manage_host_availability(
    date: str, time_slots: Dict[str, str], action: str = "update"
) -> dict:
    """
    Manages the host's availability by updating or adding time slots.

    Args:
        date: The date to manage, in YYYY-MM-DD format.
        time_slots: Dictionary of time slots to manage, format: {"HH:MM": "available" or "meeting name"}
        action: Either "update" (default) to modify existing slots, or "add" to add a new date

    Returns:
        A dictionary with the status and a confirmation message.

    Examples:
        # Make slots available
        manage_host_availability("2025-06-13", {"10:00": "available", "14:00": "available"})
        
        # Block slots with meetings
        manage_host_availability("2025-06-13", {"10:00": "Team Meeting", "14:00": "Client Call"})
        
        # Add a new date with availability
        manage_host_availability("2025-06-20", {
            "09:00": "available", "10:00": "available", "11:00": "Meeting",
            "14:00": "available", "15:00": "available"
        }, action="add")
    """
    try:
        # Validate date format
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid date format. Please use YYYY-MM-DD.",
        }

    # Validate time slots format
    for time_str in time_slots.keys():
        try:
            datetime.strptime(time_str, "%H:%M")
        except ValueError:
            return {
                "status": "error",
                "message": f"Invalid time format '{time_str}'. Please use HH:MM.",
            }

    if action == "add":
        # Add a new date to the schedule
        if date in HOST_SCHEDULE:
            return {
                "status": "error",
                "message": f"Date {date} already exists in the schedule. Use action='update' to modify existing dates.",
            }
        HOST_SCHEDULE[date] = time_slots.copy()
        return {
            "status": "success",
            "message": f"Successfully added {date} to the schedule with {len(time_slots)} time slots.",
        }
    
    elif action == "update":
        # Update existing date
        if date not in HOST_SCHEDULE:
            return {
                "status": "error",
                "message": f"Date {date} not found in schedule. Use action='add' to create new dates.",
            }
        
        # Update the specified time slots
        updated_count = 0
        for time_slot, status in time_slots.items():
            if time_slot in HOST_SCHEDULE[date]:
                HOST_SCHEDULE[date][time_slot] = status
                updated_count += 1
            else:
                # Add new time slot if it doesn't exist
                HOST_SCHEDULE[date][time_slot] = status
                updated_count += 1
        
        return {
            "status": "success",
            "message": f"Successfully updated {updated_count} time slots for {date}.",
        }
    
    else:
        return {
            "status": "error",
            "message": f"Invalid action '{action}'. Use 'update' or 'add'.",
        }