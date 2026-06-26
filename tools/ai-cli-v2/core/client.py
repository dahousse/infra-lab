import requests


class OllamaClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint.rstrip("/")

    def generate(self, model, prompt, timeout=60):
        """Chat completion via /api/chat (Ollama v0.30.x)."""
        url = f"{self.endpoint}/api/chat"

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }

        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()

        data = r.json()
        return data["message"]["content"]

    def models(self):
        url = f"{self.endpoint}/api/tags"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
