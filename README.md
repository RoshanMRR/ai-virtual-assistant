# AI Virtual Assistant

A voice-enabled virtual assistant built in Python. It listens via the
microphone, transcribes speech to text, routes the request through a
rule-based intent classifier for common commands, and falls back to an
LLM (Claude) for open-ended conversation — then speaks the response
back aloud.

## Features

- **Speech-to-text** input via `SpeechRecognition` (Google Web Speech API)
- **Text-to-speech** output via `pyttsx3` (fully offline, no API needed)
- **Rule-based intent routing** for fast, deterministic handling of common
  commands (time, date, opening websites, greetings, exit)
- **LLM fallback** (Anthropic Claude) for open-ended queries that don't
  match a built-in command
- **Text-only mode** for demoing or testing without a microphone
- Modular design — swap the LLM backend, add new intents, or replace the
  speech engine without touching the rest of the codebase

## Architecture

```
main.py                      # Entry point / conversational loop
assistant/
  speech_input.py            # Microphone capture + transcription
  speech_output.py           # Text-to-speech synthesis
  intent_classifier.py       # Keyword-based intent routing
  commands.py                # Built-in command handlers
  llm_backend.py             # Claude API wrapper for fallback responses
tests/
  test_assistant.py          # Unit tests for classifier + commands
```

## Setup

```bash
git clone https://github.com/<your-username>/ai-virtual-assistant.git
cd ai-virtual-assistant
pip install -r requirements.txt
```

On Linux, PyAudio may require system dependencies first:

```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

To enable the LLM fallback for open-ended conversation, set your API key:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Without a key, the assistant still runs — it just returns a fallback
message instead of an LLM-generated response for unmatched queries.

## Usage

Voice mode (requires a working microphone):

```bash
python main.py
```

Text-only mode (no microphone needed — useful for demos or headless
environments):

```bash
python main.py --text
```

Example interaction:

```
You: what time is it
Assistant: The current time is 03:42 PM.

You: open github
Assistant: Opening Github.

You: tell me something interesting about black holes
Assistant: [Claude-generated response]

You: exit
Assistant: Goodbye! Shutting down now.
```

## Running tests

```bash
pip install pytest
pytest tests/ -v
```

## Why this design

Most beginner voice-assistant projects hardcode a single `if/elif` chain
for matching commands. This one separates concerns instead: the intent
classifier is a standalone, swappable module, the speech I/O layers are
decoupled from the logic, and the LLM fallback means the assistant isn't
limited to a fixed list of commands — it gracefully extends to
open-ended conversation. This mirrors how production conversational AI
systems are typically structured (rule-based routing for fast, cheap,
deterministic paths + LLM fallback for everything else).

## Possible extensions

- Wake-word detection (e.g. Porcupine) so it listens continuously
- Persistent conversation memory across sessions
- Additional intents (calendar, weather, smart home control)
- Swap the rule-based classifier for an LLM-based intent router

## License

MIT — see [LICENSE](LICENSE).
