import requests


class RestRequest:
    class SpecificQueue:
        URL = "http://127.0.0.1:8000/api/specific_queues_rest"
        @staticmethod
        def get():
            rest_response = requests.get(RestRequest.SpecificQueue.URL)
            content = rest_response.json()
            return content
