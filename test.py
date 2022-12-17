import time

import vk_api

with open('./vk.txt', 'r') as fa:
    for line in fa:
        if line:
            user_id = line
vk = vk_api.VkApi(token = '**') #Авторизоваться как сообщество
def write_msg(s):
    print(user_id)
    vk.method('messages.send', {'user_id':int(user_id),'message': s,'random_id':int(time.time()*1000)})