import json
import os
from typing import Union

import requests


class RestRequest:
    class SpecificQueue:
        @staticmethod
        def get_url():
            return f"{os.getenv('SERVER_URL')}/api/specific_queues_rest/"

        @staticmethod
        def get(queue_id: Union[int, None] = None) -> json:
            rest_response = requests.get(
                RestRequest.SpecificQueue.get_url() + (f"{str(queue_id)}" if queue_id else ""))
            content = rest_response.json()
            return content

        @staticmethod
        def patch(queue_id: int, data: dict) -> int:
            rest_response = requests.patch(RestRequest.SpecificQueue.get_url() + str(queue_id) + "/", data=data)
            return rest_response.status_code

    class Members:
        @staticmethod
        def get_url():
            return f"{os.getenv('SERVER_URL')}/api/members_rest/"

        @staticmethod
        def get(member_id: Union[int, None] = None, data: Union[dict, None] = None) -> json:
            rest_response = requests.get(
                RestRequest.Members.get_url() + (f"{str(member_id)}" if member_id else ""), params=data)
            print(rest_response.url)
            content = rest_response.json()
            return content

        @staticmethod
        def post(data: dict) -> int:
            rest_response = requests.post(RestRequest.Members.get_url(), data=data)
            return rest_response.status_code

        def delete(member_id: id) -> int:
            rest_response = requests.delete(RestRequest.Members.get_url() + str(member_id))
            return rest_response.status_code
