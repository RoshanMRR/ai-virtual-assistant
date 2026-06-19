"""
llm_backend.py
Wraps a call to an LLM API (Anthropic Claude by default) for open-ended
queries that don't match a registered rule-based intent.

The API key is read from the ANTHROPIC_API_KEY environment variable.
If no key is set, falls back to a canned response so the assistant
remains demoable without credentials.
"""

import os
from typing import List, Dict


class LLMBackend:
    """Thin wrapper around the Anthropic Messages API for free-form chat."""

    def __init__(self, model: str = "claude-sonnet-4-6", max_tokens: int = 300):
        self.model = model
        self.max_tokens = max_tokens
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self._client = None

        if self.api_key:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                print("anthropic package not installed; run `pip install anthropic`.")

    def respond(self, user_text: str, history: List[Dict[str, str]] = None) -> str:
        """
        Sends the user's text (plus optional conversation history) to the
        LLM and returns the text response. Falls back to a canned message
        if no API key/client is configured.
        """
        if not self._client:
            return (
                "I'd love to help with that, but my language model backend "
                "isn't configured yet. Set ANTHROPIC_API_KEY to enable "
                "full conversational responses."
            )

        messages = (history or []) + [{"role": "user", "content": user_text}]

        response = self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages,
        )
        return response.content[0].text
