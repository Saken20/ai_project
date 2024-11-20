# ai_app/ollama_client.py

import requests
import json

class OllamaClient:
    def __init__(self, base_url='http://localhost:11434'):  # Убедитесь, что порт правильный
        self.base_url = base_url

    def generate_response(self, prompt, model='default-model', temperature=0.7, max_tokens=256):
        endpoint = f"{self.base_url}/api/generate"
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'model': model,
            'prompt': prompt,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
