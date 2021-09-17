import time

import vk_api

with open('./vk.txt', 'r') as fa:
    for line in fa:
        if line:
            user_id = line
vk = vk_api.VkApi(token = '023f638e66da45ebe3c5af7ea707a125b5c3aa1527afd2e598475a2fb378f585abb31187b3d33e69ba4d2') #Авторизоваться как сообщество
def write_msg(s):
    print(user_id)
    vk.method('messages.send', {'user_id':int(user_id),'message': s,'random_id':int(time.time()*1000)})