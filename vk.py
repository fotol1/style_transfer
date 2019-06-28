from model import StyleTransferModel
from vk_api import VkUpload
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import urllib.request
from trans import *
import requests
model = StyleTransferModel()


def main():
    #token for group
    #token=''
   # login= ''
   # passw = ''


#    api_group = vk.get_api()
    session = requests.Session()
    vk = vk_api.VkApi(login,passw,token='another_token')

   
    vk_session = vk_api.VkApi(token=token)
    upload = VkUpload(vk)

    api = vk.get_api()   
    api_group = vk_session.get_api()   
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            random_id = np.random.randint(0,20000000)
            
            user = event.user_id
            attach = event.attachments
            try:
                photo = attach['attach1']
            except:
                message = 'ЧТо-то не так'

            # let's create new folder if it doesn't exist
            path = photo.split('_')[0]
            # name of folder is id in vk

            try:  
                os.mkdir(path)
            except OSError:  
                print ("Creation of the directory %s failed" % path)
        
            # receiving some info about photo
            real_photo = api.photos.getById(photos=photo)

            # get url
            url_photo = real_photo[0]['sizes'][-1]['url']

            
            # here we have to define the filename
            # idea is very primitive
            # we will look through the folder and name the file by the next number

            # getting list of files
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            new_number = len(onlyfiles)

            # let's save the photo into directory
            urllib.request.urlretrieve(url_photo, path+'/{}.jpg'.format(new_number+1))

            # if number % 2 == 0 then it will be the source of the style
            # and it will be a picture to be transformed otherwise


            # so now our goal is to return the result
            # firstly, let's get two numpy arrays of photos

            f1 = onlyfiles[0]
            f2 = onlyfiles[1]
            print(f1,f2)

#            from trans import *
            get_output(f1,f2,path)




            image_url = 'http://localhost:8888/view/style_transer/22147487/output.png'


            image = session.get(image_url, stream=True)



            # I can't upload photo :(
            photo = upload.photo_messages(photos=image.raw)[0]
            attachments.append(
                'photo{}_{}'.format(photo['owner_id'], photo['id'])
            )
            vk.messages.send(
                user_id=event.user_id,
                attachment=','.join(attachments),
                message='Ваш текст'
            )
            continue

            #real_photo = api.photos.getByID(photos=photo)
            message = str(url_photo)

            if event.from_user:
                api_group.messages.send(
                    user_id=event.user_id,
                    message=message,
                    random_id=random_id
		)
        
if __name__ == '__main__':
    main()

