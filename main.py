"""
main.py
Entry point for the AI Virtual Assistant. Wires together speech input,
intent classification, built-in command handlers, the LLM fallback
backend, and speech output into a single conversational loop.

Run with:
    python main.py            # voice mode (requires microphone)
    python main.py --text     # text-only mode (no microphone needed)
"""

import sys
import argparse

from assistant.speech_input import SpeechListener
from assistant.speech_output import SpeechSpeaker
from assistant.intent_classifier import IntentClassifier
from assistant.llm_backend import LLMBackend
from assistant import commands

EXIT_PHRASES = {"exit", "quit", "stop", "goodbye", "bye"}


def build_classifier() -> IntentClassifier:
    classifier = IntentClassifier()
    classifier.register("time", ["time", "clock"], commands.handle_time)
    classifier.register("date", ["date", "today's date", "what day"], commands.handle_date)
    classifier.register(
        "open_website",
        ["open", "youtube", "google", "github", "linkedin"],
        commands.handle_open_website,
    )
    classifier.register("greeting", ["hello", "hi", "hey"], commands.handle_greeting)
    classifier.register("exit", list(EXIT_PHRASES), commands.handle_exit)
    return classifier


def run(text_mode: bool) -> None:
    classifier = build_classifier()
    llm = LLMBackend()
    speaker = SpeechSpeaker()
    listener = SpeechListener()

    speaker.speak("Hello, I'm your assistant. How can I help you today?")
    history = []

    while True:
        if text_mode:
            user_text = listener.listen_from_text()
        else:
            user_text = listener.listen()

        if not user_text:
            continue

        if user_text.strip().lower() in EXIT_PHRASES:
            speaker.speak(commands.handle_exit(user_text))
            break

        response = classifier.handle(
            user_text,
            fallback=lambda t: llm.respond(t, history),
        )

        history.append({"role": "user", "content": user_text})
        history.append({"role": "assistant", "content": response})
        history = history[-10:]  # keep last 5 exchanges for context

        speaker.speak(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Virtual Assistant")
    parser.add_argument(
        "--text", action="store_true", help="Run in text-only mode (no microphone)"
    )
    args = parser.parse_args()

    try:
        run(text_mode=args.text)
    except KeyboardInterrupt:
        print("\nShutting down.")
        sys.exit(0)
