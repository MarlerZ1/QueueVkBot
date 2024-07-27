from rest_requests import RestRequest
from typing import *
import json


class QueuesAnswer:
    @staticmethod
    def get_all_queues_answer(content: json) -> str:
        answer = "Список доступных очередей: \n\n"

        for i in range(len(content)):
            if i != 0:
                answer += "\n\n"
            answer += str(content[i]["id"]) + ". " + content[i]["name"] + "\n"
            answer += content[i]["description"] + "\n"
            answer += "Активно: " + ("Да" if content[i]["active"] else "Нет")

        return answer

    @staticmethod
    def get_active_queues_answer(content: json) -> str:
        answer = "Список активных очередей: \n\n"

        for i in range(len(content)):
            if content[i]["active"]:
                if i != 0:
                    answer += "\n\n"
                answer += str(content[i]["id"]) + ". " + content[i]["name"] + "\n"
                answer += content[i]["description"] + "\n"
        answer += "\n\n"
        answer += "Чтобы активировать очередь, напишите: Активировать *название очереди или ее номер*\n"
        answer += "Чтобы деактивировать очередь, напишите: Деактивировать *название очереди или ее номер*\n"
        return answer

    @staticmethod
    def get_inactive_queues_answer(content: json):
        answer = "Список неактивных очередей: \n\n"

        for i in range(len(content)):
            if not content[i]["active"]:
                if i != 0:
                    answer += "\n\n"
                answer += str(content[i]["id"]) + ". " + content[i]["name"] + "\n"
                answer += content[i]["description"] + "\n"

        return answer

    @staticmethod
    def get_activity_change_attempt_answer(queues_to_activate: List[str], new_state: bool) -> str:
        answer = ""
        queue_names = []
        has_strings = False

        for queue in queues_to_activate:
            if queue.isdigit():
                rest_object = RestRequest.SpecificQueue.get(queue_id=int(queue))
                if rest_object.get('detail') != 'No SpecificQueue matches the given query.':

                    RestRequest.SpecificQueue.patch(queue_id=int(queue), data={'active': new_state})
                    answer += f"Очередь '{rest_object['name']}' #{rest_object['id']} {'де' if not new_state else ''}активирована\n"
                else:
                    answer += f"Очередь #{queue} не существует\n"
            else:
                has_strings = True
                queue_names.append(queue)

        if has_strings:
            content = RestRequest.SpecificQueue.get()

            for queue in content:
                if queue["name"].strip() in queue_names:
                    RestRequest.SpecificQueue.patch(queue_id=int(queue["id"]), data={'active': new_state})
                    queue_names.remove(queue["name"])
                    answer += f"Очередь '{queue['name']}' #{queue['id']} {'де' if not new_state else ''}активирована\n"
            for queue_name in queue_names:
                answer += f"Очередь #{queue_name} не существует\n"

        return answer
