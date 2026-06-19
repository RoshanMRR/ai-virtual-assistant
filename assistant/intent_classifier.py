"""
intent_classifier.py
Lightweight rule-based + keyword-scoring intent classifier.
Routes a transcribed utterance to a registered intent handler.

Designed to be swappable: replace `classify()` internals with an
LLM-based classifier (see llm_backend.py) without changing the
public interface used by the assistant core.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple


@dataclass
class Intent:
    name: str
    keywords: List[str]
    handler: Callable[[str], str]


class IntentClassifier:
    """Routes text input to the best-matching registered intent."""

    def __init__(self):
        self._intents: Dict[str, Intent] = {}

    def register(self, name: str, keywords: List[str], handler: Callable[[str], str]) -> None:
        self._intents[name] = Intent(name=name, keywords=keywords, handler=handler)

    def classify(self, text: str) -> Tuple[str, float]:
        """
        Scores each registered intent by keyword overlap and returns
        the best match and a confidence score between 0 and 1.
        """
        text_lower = text.lower()
        best_name, best_score = "fallback", 0.0

        for intent in self._intents.values():
            matches = sum(1 for kw in intent.keywords if kw in text_lower)
            if matches == 0:
                continue
            score = matches / len(intent.keywords)
            if score > best_score:
                best_name, best_score = intent.name, score

        return best_name, best_score

    def handle(self, text: str, fallback: Callable[[str], str]) -> str:
        """Classifies the text and dispatches to the matched handler."""
        name, score = self.classify(text)
        if name == "fallback" or score == 0.0:
            return fallback(text)
        return self._intents[name].handler(text)
