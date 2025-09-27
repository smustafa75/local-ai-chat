#!/usr/bin/env python3
import argparse
import json
from ollama_agent import OllamaAgent

def main():
    parser = argparse.ArgumentParser(description='Ollama Agent CLI')
    parser.add_argument('command', choices=['chat', 'task', 'stream'])
    parser.add_argument('input', help='Message or task name')
    parser.add_argument('--data', help='JSON data for tasks')
    parser.add_argument('--model', default='llama3.2:latest')
    
    args = parser.parse_args()
    agent = OllamaAgent(model=args.model)
    
    if args.command == 'chat':
        print(agent.chat(args.input))
        
    elif args.command == 'task':
        data = json.loads(args.data) if args.data else {}
        print(json.dumps(agent.task(args.input, data), indent=2))
        
    elif args.command == 'stream':
        data = json.loads(args.data) if args.data else {}
        agent.task(args.input, data, callback=lambda x: print(x, end='', flush=True))

if __name__ == '__main__':
    main()
