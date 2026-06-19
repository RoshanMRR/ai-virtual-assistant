"""
speech_input.py
Handles microphone capture and converts speech to text using the
SpeechRecognition library (Google Web Speech API backend by default).
"""

import speech_recognition as sr
from typing import Optional


class SpeechListener:
    """Wraps microphone capture and speech-to-text transcription."""

    def __init__(self, energy_threshold: int = 300, pause_threshold: float = 0.8):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold

    def listen(self, timeout: int = 5, phrase_time_limit: int = 8) -> Optional[str]:
        """
        Listens via the default microphone and returns the transcribed text.
        Returns None if nothing was understood or no mic is available.
        """
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
        except sr.WaitTimeoutError:
            print("No speech detected within timeout window.")
            return None
        except OSError:
            print("No microphone found. Falling back to text input mode.")
            return None

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"Heard: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            return None

    def listen_from_text(self, prompt: str = "You: ") -> str:
        """Fallback for environments without a microphone (e.g. CI, demos)."""
        return input(prompt)
