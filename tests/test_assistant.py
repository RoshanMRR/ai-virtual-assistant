"""
test_assistant.py
Unit tests for the intent classifier and built-in command handlers.
Run with: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from assistant.intent_classifier import IntentClassifier
from assistant import commands


def test_classifier_matches_time_intent():
    classifier = IntentClassifier()
    classifier.register("time", ["time", "clock"], commands.handle_time)

    name, score = classifier.classify("what is the time right now")
    assert name == "time"
    assert score > 0


def test_classifier_returns_fallback_for_unknown_input():
    classifier = IntentClassifier()
    classifier.register("time", ["time", "clock"], commands.handle_time)

    name, score = classifier.classify("tell me a poem about the ocean")
    assert name == "fallback"
    assert score == 0.0


def test_handle_dispatches_to_correct_handler():
    classifier = IntentClassifier()
    classifier.register("greeting", ["hello", "hi"], commands.handle_greeting)

    result = classifier.handle("hi there", fallback=lambda t: "FALLBACK")
    assert "Hello" in result


def test_handle_falls_back_when_no_intent_matches():
    classifier = IntentClassifier()
    classifier.register("greeting", ["hello", "hi"], commands.handle_greeting)

    result = classifier.handle("xyz unmatched text", fallback=lambda t: "FALLBACK_USED")
    assert result == "FALLBACK_USED"


def test_handle_time_returns_string_with_time_keyword():
    response = commands.handle_time("")
    assert "time" in response.lower()


def test_handle_date_returns_today():
    response = commands.handle_date("")
    assert "Today is" in response


def test_handle_exit_message():
    response = commands.handle_exit("")
    assert "Goodbye" in response
