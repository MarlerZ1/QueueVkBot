import os

import vk_api
from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from answers import *
from rest_requests import RestRequest

load_dotenv()
token = os.getenv("VK_SECRET_TOCKEN")

vk = vk_api.VkApi(token=token)
api_vk = vk.get_api()
longpoll = VkBotLongPoll(vk, os.getenv("GROUP_ID"))

admins = json.loads(os.getenv("ADMINS_SREEN_NAME_LIST"))

request_prefix = F'[club{os.getenv("GROUP_ID")}|os.getenv("GROUP_NAME")]'


def write_msg(peer_id: int, message: str) -> None:
    api_vk.messages.send(peer_id=peer_id, message=message, random_id=vk_api.utils.get_random_id())


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        request = event.object["message"]["text"].strip()

        request = request.replace(request_prefix, '').replace(',', '').replace('.', '').strip()

        if request.lower() == "лист":
            content = RestRequest.SpecificQueue.get()

            answer = QueuesAnswer.get_all_queues_answer(content)
            write_msg(event.message.peer_id, answer)
        elif request.lower() == "активно":
            content = RestRequest.SpecificQueue.get()

            answer = QueuesAnswer.get_active_queues_answer(content)
            write_msg(event.message.peer_id, answer)


        elif request.lower() == "неактивно":
            content = RestRequest.SpecificQueue.get()

            answer = QueuesAnswer.get_inactive_queues_answer(content)
            write_msg(event.message.peer_id, answer)
        elif request[:12].lower() == "активировать" or request[:14].lower() == "деактивировать":
            if api_vk.users.get(user_ids=event.message.from_id, fields=["screen_name", ])[0]["screen_name"] in admins:
                if request[:12] == "активировать":
                    new_state = True
                    request = request[12:]
                else:
                    new_state = False
                    request = request[14:]

                if not request:
                    write_msg(event.message.peer_id, "Вы не указали очередь")
                else:
                    queues_to_activate = list(map(str.strip, request.split(',')))
                    answer = QueuesAnswer.get_activity_change_attempt_answer(queues_to_activate, new_state)
                    write_msg(event.message.peer_id, answer)
            else:
                write_msg(event.message.peer_id, "У вас нет прав для этого действия")
        elif request.lower()[:7] == "очередь":
            request = request[7:].strip()
            if not request:
                write_msg(event.message.peer_id, "Вы не указали очередь")
            else:
                if request.isdigit():
                    rest_object = RestRequest.SpecificQueue.get(queue_id=int(request))
                    if rest_object.get('detail') != 'No SpecificQueue matches the given query.':
                        members = RestRequest.Members.get(data={"specific_queue": int(request)})

                        answer = MembersAnswer.get_members_answer(members)
                        write_msg(event.message.peer_id, answer)
                    else:
                        write_msg(event.message.peer_id, f"Очередь #{request} не существует\n")
                else:
                    content = RestRequest.SpecificQueue.get()
                    for queue in content:
                        if queue["name"].strip() == request:
                            members = RestRequest.Members.get(data={"specific_queue": int(request)})
                            answer = MembersAnswer.get_members_answer(members)
                            write_msg(event.message.peer_id, answer)
                            break
                    else:
                        write_msg(event.message.peer_id, f"Очередь #{request} не существует\n")
        else:
            write_msg(event.message.peer_id, "Не поняла вашего ответа...")
