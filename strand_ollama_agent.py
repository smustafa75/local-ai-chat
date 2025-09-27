#!/usr/bin/env python3
import requests
import json
from typing import Dict, Any, Optional
from strand_agent import StrandAgent, Message

class StrandOllamaAgent:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2:latest"):
        self.base_url = base_url
        self.model = model
        self.strand_agent = StrandAgent()
        
    def chat(self, message: str) -> str:
        """Handle chat via Strand Agent with Ollama backend"""
        # Create message for Strand Agent
        user_message = Message(content=message, role="user")
        
        # Process through Strand Agent
        strand_response = self.strand_agent.process(user_message)
        
        # Send to Ollama backend
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model, 
            "prompt": strand_response.content, 
            "stream": False
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    
    def stream_chat(self, message: str, callback=None) -> str:
        """Stream chat via Strand Agent"""
        user_message = Message(content=message, role="user")
        strand_response = self.strand_agent.process(user_message)
        
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model, 
            "prompt": strand_response.content, 
            "stream": True
        }
        
        full_response = ""
        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        chunk = data["response"]
                        full_response += chunk
                        if callback:
                            callback(chunk)
                    if data.get("done", False):
                        break
        return full_response
