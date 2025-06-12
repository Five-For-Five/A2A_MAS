import random
from datetime import date, datetime, timedelta

from google.adk.agents import LlmAgent


def generate_karley_calendar() -> dict[str, list[str]]:
    """Generates available coaching slots for Karley Coaching Services for the next 7 days."""
    calendar = {}
    today = date.today()
    possible_times = [f"{h:02}:00" for h in range(8, 21)]  # 8 AM to 8 PM

    for i in range(7):
        current_date = today + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")

        # Select 8 random unique time slots to increase availability
        available_slots = sorted(random.sample(possible_times, 8))
        calendar[date_str] = available_slots

    print("Coaching availability:", calendar)

    return calendar


KARLEY_CALENDAR = generate_karley_calendar()


def get_availability(start_date: str, end_date: str) -> str:
    """
    Checks coaching session availability for a given date range.

    Args:
        start_date: The start of the date range to check, in YYYY-MM-DD format.
        end_date: The end of the date range to check, in YYYY-MM-DD format.

    Returns:
        A string listing available coaching slots for that date range.
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start > end:
            return "Invalid date range. The start date cannot be after the end date."

        results = []
        delta = end - start
        for i in range(delta.days + 1):
            day = start + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            available_slots = KARLEY_CALENDAR.get(date_str, [])
            if available_slots:
                availability = f"On {date_str}, coaching sessions are available at: {', '.join(available_slots)}."
                results.append(availability)
            else:
                results.append(f"No coaching sessions available on {date_str}.")

        return "\n".join(results)

    except ValueError:
        return (
            "Invalid date format. Please use YYYY-MM-DD for both start and end dates."
        )


def create_agent() -> LlmAgent:
    """Constructs the ADK agent for Karley Coaching Services."""
    return LlmAgent(
        model="gemini-2.5-flash-preview-04-17",
        name="Karley_Coaching_Agent",
        instruction="""
            **Role:** You are the scheduling assistant for Karley Coaching Services, a voluntary coaching organization. 
            Your sole responsibility is to manage coaching session availability and respond to inquiries 
            about booking coaching sessions.

            **Core Directives:**

            *   **Check Availability:** Use the `get_availability` tool to determine 
                    available coaching slots on a requested date or over a range of dates. 
                    The tool requires a `start_date` and `end_date`. If the user only provides 
                    a single date, use that date for both the start and end.
            *   **Professional and Helpful:** Maintain a professional tone while being helpful and accommodating.
            *   **Stick to Your Role:** Focus on scheduling coaching sessions. 
                    If asked other questions, politely state that you can only help with coaching session scheduling.
            *   **Organization Context:** Remember you represent Karley Coaching Services, not an individual.
        """,
        tools=[get_availability],
    )
