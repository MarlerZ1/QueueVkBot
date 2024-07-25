import os
from answers import *
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


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if request == "Очередь":
                content = RestRequest.SpecificQueue.get()

                answer = QueuesAnswer.get_all_queues_answer(content)
                write_msg(event.user_id, answer)
            elif request == "Активно":
                content = RestRequest.SpecificQueue.get()

                answer = QueuesAnswer.get_active_queues_answer(content)
                write_msg(event.user_id, answer)
            elif request == "Неактивно":
                content = RestRequest.SpecificQueue.get()

                answer = QueuesAnswer.get_inactive_queues_answer(content)
                write_msg(event.user_id, answer)
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
