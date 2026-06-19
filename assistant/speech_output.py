"""
speech_output.py
Converts text responses to speech using pyttsx3 (fully offline TTS engine).
"""

import pyttsx3


class SpeechSpeaker:
    """Wraps offline text-to-speech synthesis."""

    def __init__(self, rate: int = 175, volume: float = 1.0, voice_index: int = 0):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

        voices = self.engine.getProperty("voices")
        if voices and voice_index < len(voices):
            self.engine.setProperty("voice", voices[voice_index].id)

    def speak(self, text: str) -> None:
        """Speaks the given text aloud and also prints it for visibility."""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
