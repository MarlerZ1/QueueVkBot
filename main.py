import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dotenv import load_dotenv

load_dotenv()
token = os.getenv("VK_SECRET_TOCKEN")

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message})


for event in longpoll.listen():
    pass