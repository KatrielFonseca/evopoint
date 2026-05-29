import requests

class EvoClient:

    def __init__(self, ip, password="1234"):
        self.ip = ip
        self.password = password
        self.base_url = f"http://{ip}/api"

    def send(self, payload):

        payload["password"] = self.password

        response = requests.post(
            self.base_url,
            json=payload,
            timeout=10
        )

        try:
            return response.json()
        except:
            return response.text