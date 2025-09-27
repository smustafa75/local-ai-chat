#!/usr/bin/env python3
import requests
import json
import re
from typing import Dict, Any, Optional, Iterator, Callable

class OllamaAgent:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2:latest"):
        self.base_url = base_url
        self.model = model
        self.injection_patterns = [
            r'ignore\s+previous\s+instructions',
            r'forget\s+everything',
            r'system\s*:',
            r'assistant\s*:',
            r'human\s*:',
            r'<\s*system\s*>',
            r'</\s*system\s*>',
            r'prompt\s*injection',
            r'jailbreak',
            r'override\s+instructions'
        ]
    
    def _sanitize_input(self, text: str) -> str:
        """Basic prompt injection prevention"""
        for pattern in self.injection_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                raise ValueError("Potential prompt injection detected")
        
        # Remove excessive newlines and control characters
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        return text.strip()[:4000]  # Limit length
        
    def chat(self, message: str, context: Optional[str] = None) -> str:
        """Send message to Ollama and get response"""
        message = self._sanitize_input(message)
        if context:
            context = self._sanitize_input(context)
            
        url = f"{self.base_url}/api/generate"
        prompt = f"{context}\n\n{message}" if context else message
        
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    
    def stream(self, message: str, context: Optional[str] = None, callback: Optional[Callable] = None) -> str:
        """Stream response from Ollama with optional callback"""
        message = self._sanitize_input(message)
        if context:
            context = self._sanitize_input(context)
            
        url = f"{self.base_url}/api/generate"
        prompt = f"{context}\n\n{message}" if context else message
        
        payload = {"model": self.model, "prompt": prompt, "stream": True}
        
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
    
    def task(self, task_name: str, data: Dict[str, Any], callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Execute structured task"""
        task_name = self._sanitize_input(task_name)
        prompt = f"Task: {task_name}\nData: {json.dumps(data)}\nProvide JSON response with status and result."
        
        try:
            response = self.stream(prompt, callback=callback) if callback else self.chat(prompt)
            
            # Extract JSON
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                return json.loads(response[start:end])
            
            return {"status": "success", "result": response}
            
        except Exception as e:
            return {"status": "error", "result": str(e)}
