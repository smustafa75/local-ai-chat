#!/usr/bin/env python3
import argparse
from strand_ollama_agent import StrandOllamaAgent

def main():
    parser = argparse.ArgumentParser(description="Strand Ollama Agent CLI")
    parser.add_argument("command", choices=["chat", "stream"], help="Command to execute")
    parser.add_argument("message", help="Message to send")
    parser.add_argument("--model", default="llama3.2:latest", help="Model to use")
    parser.add_argument("--url", default="http://localhost:11434", help="Ollama base URL")
    
    args = parser.parse_args()
    
    agent = StrandOllamaAgent(base_url=args.url, model=args.model)
    
    if args.command == "chat":
        response = agent.chat(args.message)
        print(response)
    elif args.command == "stream":
        def print_chunk(chunk):
            print(chunk, end='', flush=True)
        agent.stream_chat(args.message, callback=print_chunk)
        print()

if __name__ == "__main__":
    main()
