import requests

class EvoClient:

    def __init__(
        self,
        ip,
        port="80",
        password="1234"
    ):

        self.ip = ip
        self.port = port
        self.password = password

        self.base_url = (
            f"http://{ip}:{port}/api"
        )

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