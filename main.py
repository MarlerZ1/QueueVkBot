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

request_prefix = F'[club{os.getenv("GROUP_ID")}|{os.getenv("GROUP_NAME")}]'
print(request_prefix)
chats_current_active_queue = {}


def change_active_state(queue_id, queue_name, new_state):
    RestRequest.SpecificQueue.patch(queue_id=queue_id, data={'active': new_state})
    write_msg(event.message.peer_id,
              f"Очередь #{queue_name if queue_name else queue_id} {'де' if not new_state else ''}активирована")


def choose_queue(queue_id, queue_name):
    chats_current_active_queue[event.message.peer_id] = queue_id
    write_msg(event.message.peer_id, f"Очередь #{queue_name if queue_name else queue_id} выбрана")


def print_queue(queue_id, queue_name):
    members = RestRequest.Members.get(data={"specific_queue": queue_id})
    answer = MembersAnswer.get_members_answer(members, queue_id, queue_name)
    write_msg(event.message.peer_id, answer)


def request_queue_exists_checker(request, callback, **kwargs):
    request = request.strip()
    if not request:
        write_msg(event.message.peer_id, "Вы не указали очередь")
    else:
        if request.isdigit():
            rest_object = RestRequest.SpecificQueue.get(queue_id=int(request))
            if rest_object.get('detail') != 'No SpecificQueue matches the given query.':
                callback(queue_id=int(request), queue_name=rest_object["name"], **kwargs)
            else:
                write_msg(event.message.peer_id, f"Очередь #{request} не существует\n")
        else:
            content = RestRequest.SpecificQueue.get()
            for queue in content:
                if queue["name"].strip() == request:
                    callback(queue_id=int(queue["id"]), queue_name=request, **kwargs)
                    break
            else:
                write_msg(event.message.peer_id, f"Очередь #{request} не существует\n")


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

                request_queue_exists_checker(request, change_active_state, new_state=new_state)
            else:
                write_msg(event.message.peer_id, "У вас нет прав для этого действия")
        elif request.lower()[:7] == "очередь":
            request = request[7:]

            request_queue_exists_checker(request, print_queue)

        elif request.lower()[:7] == "выбрать":
            request = request[7:]

            request_queue_exists_checker(request, choose_queue)
        elif request.lower() in ['+', 'я', 'фиксирую', '.']:
            if chats_current_active_queue.get(event.message.peer_id):
                queue = RestRequest.SpecificQueue.get(queue_id=chats_current_active_queue[event.message.peer_id])
                if queue["active"]:
                    user_data = api_vk.users.get(user_ids=event.message.from_id)[0]
                    username = user_data["first_name"] + " " + user_data["last_name"]

                    rest_user = RestRequest.Members.get(
                        data={"specific_queue": chats_current_active_queue[event.message.peer_id],
                              "name": username})
                    if rest_user:
                        write_msg(event.message.peer_id, f"Вы уже есть в этой очереди, {username}")
                    else:
                        RestRequest.Members.post(data={'name': username, 'specific_queue': chats_current_active_queue[
                            event.message.peer_id]})
                        write_msg(event.message.peer_id, f"{username} добавлен")
                else:
                    write_msg(event.message.peer_id,
                              "Очередь не активирована. Для добавления в очередь, активируйте ее или подождите активации от администратора")
            else:
                write_msg(event.message.peer_id, "Вы не выбрали очередь")
        elif request.lower() in ['pop', 'поп', '-']:
            if api_vk.users.get(user_ids=event.message.from_id, fields=["screen_name", ])[0]["screen_name"] in admins:
                if chats_current_active_queue.get(event.message.peer_id):
                    members = RestRequest.Members.get(
                        data={"specific_queue": chats_current_active_queue[event.message.peer_id]})
                    if len(members) != 0:
                        RestRequest.Members.delete(member_id=members[0]["id"])
                        write_msg(event.message.peer_id, f"{members[0]['name']} удален из очереди")
                    else:
                        write_msg(event.message.peer_id, f"Очередь пуста")
                else:
                    write_msg(event.message.peer_id, "Вы не выбрали очередь")
            else:
                write_msg(event.message.peer_id, "У вас нет прав для этого действия")
        elif request.lower() in ['команды', 'help']:
            answer = "1. Лист - посмотреть список очередей\n"
            answer += "2. Активно - посмотреть список активных очередей\n"
            answer += "3. Неактивно - посмотреть список неактивных очередей\n"
            answer += "4. Активировать/Деактивировать *номер очереди или название*- включить или выключить очередь (admins only)\n"
            answer += "5. Очередь *номер очереди или название* - вывести всех участников очереди\n"
            answer += "6. Выбрать *номер очереди или название* - выбрать очередь для записи или удаления участника (admins only)\n"
            answer += "7. '+', 'я', 'фиксирую', '.' - добавить себя в очередь. Сначала нужно выбрать очередь (6). Если вы уже есть в очереди, то вас не добавят заново \n"
            answer += "8. 'pop', 'поп', '-' - убрать первого участника очереди. Сначала нужно выбрать очередь (6) \n"

            write_msg(event.message.peer_id, answer)
        else:
            write_msg(event.message.peer_id, "Не поняла вашего ответа...")
