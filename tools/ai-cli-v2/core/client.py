import requests

class OllamaClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint.rstrip("/")

    def generate(self, model, prompt):
        url = f"{self.endpoint}/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()

        return r.json()["response"]

    def models(self):
        url = f"{self.endpoint}/api/tags"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
