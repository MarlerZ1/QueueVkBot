import json
import os
from typing import Union

import requests


class RestRequest:
    class SpecificQueue:
        @staticmethod
        def get_url():
            return f"{os.getenv('SERVER_URL')}/api/specific_queues_rest"

        @staticmethod
        def get(queue_id: Union[int, None] = None) -> json:
            rest_response = requests.get(RestRequest.SpecificQueue.get_url() + (f"/{str(queue_id)}" if queue_id else ""))
            content = rest_response.json()
            return content

        @staticmethod
        def patch(queue_id: int, data: dict) -> json:
            rest_response = requests.patch(RestRequest.SpecificQueue.get_url() + "/" + str(queue_id) + "/", data=data)
            print(rest_response.status_code)
            return rest_response.status_code