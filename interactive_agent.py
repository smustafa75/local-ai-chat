#!/usr/bin/env python3
from ollama_agent import OllamaAgent

def main():
    agent = OllamaAgent()
    print("Ollama Agent ready. Type 'quit' to exit.")
    
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ['quit', 'exit']:
                break
            print(agent.chat(user_input))
        except ValueError as e:
            print(f"Input rejected: {e}")
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == '__main__':
    main()
