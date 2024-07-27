import json
import os
from answers import *
import vk_api
from rest_requests import RestRequest
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

load_dotenv()
token = os.getenv("VK_SECRET_TOCKEN")

vk = vk_api.VkApi(token=token)
api_vk = vk.get_api()
longpoll = VkLongPoll(vk)

admins = json.loads(os.getenv("ADMINS_SREEN_NAME_LIST"))
print(admins)
def write_msg(user_id: int, message: str) -> None:
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': vk_api.utils.get_random_id()})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.strip()
            if request.lower() == "очередь":
                content = RestRequest.SpecificQueue.get()

                answer = QueuesAnswer.get_all_queues_answer(content)
                write_msg(event.user_id, answer)
            elif request.lower() == "активно":
                content = RestRequest.SpecificQueue.get()

                answer = QueuesAnswer.get_active_queues_answer(content)
                write_msg(event.user_id, answer)


            elif request.lower() == "неактивно":
                content = RestRequest.SpecificQueue.get()

                answer = QueuesAnswer.get_inactive_queues_answer(content)
                write_msg(event.user_id, answer)
            elif request[:12].lower() == "активировать" or request[:14].lower() == "деактивировать":
                if api_vk.users.get(user_ids=event.user_id, fields=["screen_name", ])[0]["screen_name"] in admins:
                    if request[:12] == "активировать":
                        new_state = True
                        request = request[12:]
                    else:
                        new_state = False
                        request = request[14:]
                        
                    if not request:
                        write_msg(event.user_id, "Вы не указали очередь")
                    else:
                        queues_to_activate = list(map(str.strip, request.split(',')))
                        answer = QueuesAnswer.get_activity_change_attempt_answer(queues_to_activate, new_state)
                        write_msg(event.user_id, answer)
                else:
                    write_msg(event.user_id, "У вас нет прав для этого действия")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
