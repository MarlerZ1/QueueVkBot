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
            elif request[:12].lower() == "активировать":
                answer = ""

                request = request[12:]

                queue_names = []

                has_digits, has_strings = False, False

                queues_to_activate = request.split(',')
                queues_to_activate = map(str.strip, queues_to_activate)
                for queue in queues_to_activate:
                    if queue.isdigit():
                        has_digits = True
                        object = RestRequest.SpecificQueue.get(queue_id=int(queue))
                        if object.get('detail') != 'No SpecificQueue matches the given query.':

                            RestRequest.SpecificQueue.patch(queue_id=int(queue), data={'active': True})
                            answer += f"Очередь '{object['name']}' #{object['id']} активирована\n"
                        else:
                            answer += f"Очередь #{queue} не существует\n"
                    else:
                        has_strings = True
                        queue_names.append(queue)

                if has_strings:
                    content = RestRequest.SpecificQueue.get()

                    for queue in content:
                        if queue["name"].strip() in queue_names:
                            RestRequest.SpecificQueue.patch(queue_id=int(queue["id"]), data={'active': True})
                            queue_names.remove(queue["name"])
                            answer += f"Очередь '{queue['name']}' #{queue['id']} активирована\n"
                    for queue_name in queue_names:
                        answer += f"Очередь #{queue_name} не существует\n"

                if not (has_strings or has_digits):
                    write_msg(event.user_id, "Вы не указали очередь")
                else:
                    write_msg(event.user_id, answer)
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
