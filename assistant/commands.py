"""
commands.py
Built-in handlers for common voice assistant tasks: time, date, web search,
opening applications/websites, and simple jokes. Each handler takes the
raw utterance and returns a string response to be spoken back.
"""

import datetime
import webbrowser


def handle_time(_: str) -> str:
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {now}."


def handle_date(_: str) -> str:
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {today}."


def handle_open_website(text: str) -> str:
    sites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "github": "https://github.com",
        "linkedin": "https://linkedin.com",
    }
    text_lower = text.lower()
    for name, url in sites.items():
        if name in text_lower:
            webbrowser.open(url)
            return f"Opening {name.capitalize()}."
    return "I'm not sure which site you'd like me to open."


def handle_greeting(_: str) -> str:
    return "Hello! How can I help you today?"


def handle_exit(_: str) -> str:
    return "Goodbye! Shutting down now."
