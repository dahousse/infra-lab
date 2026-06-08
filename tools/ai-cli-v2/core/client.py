import requests

class OllamaClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def generate(self, model, prompt):
        url = f"{self.endpoint}/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        r = requests.post(url, json=payload)
        r.raise_for_status()

        return r.json().get("response", "")
