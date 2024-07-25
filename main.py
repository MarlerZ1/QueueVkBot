import os
import requests
import vk_api
from rest_requests import RestRequest
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

load_dotenv()
token = os.getenv("VK_SECRET_TOCKEN")

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': vk_api.utils.get_random_id()})


def create_queues_text_answer(content):
    answer = "Список доступных очередей: \n\n"

    for i in range(len(content)):
        if i != 0:
            answer += "\n\n"
        answer += str(i+1) + ". " + content[i]["name"] + "\n"
        answer += content[i]["description"]

    return answer

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request == "Очередь":
                content = RestRequest.SpecificQueue.get()

                answer = create_queues_text_answer(content)
                write_msg(event.user_id, answer)
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
