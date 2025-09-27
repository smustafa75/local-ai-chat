# Local AI Chat Interface

Simple Python integration with Ollama for AI task execution, now with Strand Agent for enhanced chat handling. Includes built-in security guardrails for prompt injection prevention and input sanitization.

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running locally
- Internet connection for package installation

**NOTE**: Internet connection is only required for initial setup (installing dependencies and downloading models). During execution, the system runs entirely offline as both Strand Agent and Ollama operate locally.

## Setup

1. Install Ollama and pull a model:
```bash
ollama pull llama3.2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

```bash
python3 interactive_agent.py
```

### Strand Agent CLI

```bash
# Chat with Strand Agent handling
python3 strand_cli.py chat "What is machine learning?"

# Streaming with Strand Agent
python3 strand_cli.py stream "Tell me a story"
```

### Python API

#### Strand Agent Integration

```python
from strand_ollama_agent import StrandOllamaAgent

agent = StrandOllamaAgent()

# Chat handled by Strand Agent
response = agent.chat("Hello, how are you?")
print(response)

# Streaming with callback
def print_chunk(chunk):
    print(chunk, end='', flush=True)

agent.stream_chat("Tell me a story", callback=print_chunk)
```

#### Original Agent

```python
from ollama_agent import OllamaAgent

agent = OllamaAgent()

# Simple chat
response = agent.chat("Hello, how are you?")
print(response)

# Streaming chat with callback
agent.stream("Tell me a story", callback=print_chunk)

# Structured task execution
result = agent.task("analyze_data", {
    "numbers": [1, 2, 3, 4, 5],
    "operation": "calculate_statistics"
})
print(result)
```

## Configuration

- **Default URL**: `http://localhost:11434`
- **Default Model**: `llama3.2:latest`
- **Customizable**: Pass different `base_url` and `model` to constructor

## Project Structure

```
├── ollama_agent.py         # Core agent class
├── strand_ollama_agent.py  # Strand Agent integration
├── interactive_agent.py    # Interactive CLI
├── cli.py                 # Command line interface
├── strand_cli.py          # Strand Agent CLI
├── requirements.txt       # Dependencies
└── README.md             # This file
```
