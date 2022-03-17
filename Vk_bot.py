import vk_api
import BD
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import *
from pytz import timezone
from config import TOKEN_VK_API, ID_GROUP, MY_ID
from time import time


class MyVkBotLongPoll(VkBotLongPoll):
    """Обработчик ошибок, связанных с ответом сервера - ибо вк как миннимум раз в день перезагружает сови сервера"""

    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as err:
                print('error', err)


TIME_ZONE = timezone("Asia/Krasnoyarsk")

vk_session = vk_api.VkApi(token=TOKEN_VK_API)
longpoll = MyVkBotLongPoll(vk_session, ID_GROUP)
upload = vk_api.VkUpload(vk_session)


def send_me_message(text):
    """Функция для отправки сообщения владельцу, в сязи с возможными ошибками и их устранению"""
    try:
        vk_session.method('messages.send', {'peer_id': MY_ID, 'message': text, 'random_id': int(time())})
    except Exception as err:
        print('error sending_message', err)


def send_message(id, text, photo=None, keyboard=None):
    """Отправка сообщения"""
    try:
        vk_session.method('messages.send',
                          {'peer_id': id, 'message': text, 'attachment': photo, 'random_id': int(time()),
                           'keyboard': keyboard})
    except Exception as err:
        send_me_message(f'{err} - send_message')


def upload_photo(url):
    """Отправка фото либо картинки"""
    try:
        picture = url
        upload_image = upload.photo_messages(photos=picture)[0]
        owner_id = upload_image['owner_id']
        photo_id = upload_image['id']
        access_key = upload_image['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        return attachment
    except Exception as err:
        send_me_message(f'{err} - upload_photo')
        return None


def uppload_doc(url, id_peer):
    """Отправка документа"""
    try:
        docs = url
        upload_image = upload.document_message(doc=docs, peer_id=id_peer)['doc']
        owner_id = upload_image['owner_id']
        photo_id = upload_image['id']
        attachment = f'doc{owner_id}_{photo_id}'
        return attachment
    except Exception as err:
        send_me_message(f'{err} - upload_doc')
        return None


def isMember(id_user):
    """Проверка пользователя на то, что состоит ли он в сообществе"""
    try:
        return vk_session.method('groups.isMember',
                                 {'group_id': ID_GROUP, 'user_id': id_user})
    except Exception as err:
        send_me_message(f'{err} - IsMember')
        return False


def check_name(id):
    try:
        data = vk_session.method('users.get', {'user_ids': id})[0]
        full_name = f'{data.get("first_name")} {data.get("last_name")}'
        return full_name
    except Exception as err:
        send_me_message(f'{err} - check_name')
        return 'NoName'


def keyboard_bgc():
    keyboard = VkKeyboard()
    keyboard.add_button(label='1 корпус',
                        color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='2 корпус',
                        color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(label='3 корпус',
                        color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='4 корпус',
                        color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(label='Автоматическая отправка расписания',
                        color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(label='Расписание звонков',
                        color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()


def keyboard_auto_update_bgc():
    keyboard = VkKeyboard()
    keyboard.add_button(label='обновление 1 корпус',
                        color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(label='обновление 2 корпус',
                        color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(label='обновление 3 корпус',
                        color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(label='обновление 4 корпус',
                        color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(label='Удалить подписку на обновление',
                        color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(label='Назад',
                        color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def message_processing():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.obj['message']['text'].lower()
            if event.from_chat:  # обработка событий для сообщений в беседу
                id = event.chat_id
                if msg == '/расписание1':
                    send_message(id + 2000000000, 'Расписание 1 корпус', upload_photo('pictures/download_zamena1k.png'))
                elif msg == '/расписание2':
                    send_message(id + 2000000000, 'Расписание 2 корпус', upload_photo('pictures/download_zamena2k.png'))
                elif msg == '/расписание3':
                    send_message(id + 2000000000, 'Расписание 3 корпус',
                                 upload_photo('pictures/download_zamena3k.png'))
                elif msg == '/расписание4':
                    send_message(id + 2000000000, 'Расписание 4 корпус', upload_photo('pictures/download_zamena4k.png'))

                elif msg == '/обновление 1 корпус':
                    BD.user_add(id + 2000000000, 'group', '1 корпус')
                    send_message(id + 2000000000, 'Вы успешно подписались на обновление')
                elif msg == '/обновление 2 корпус':
                    BD.user_add(id + 2000000000, 'group', '2 корпус')
                    send_message(id + 2000000000, 'Вы успешно подписались на обновление')
                elif msg == '/обновление 3 корпус':
                    BD.user_add(id + 2000000000, 'group', '3 корпус')
                    send_message(id + 2000000000, 'Вы успешно подписались на обновление')
                elif msg == '/обновление 4 корпус':
                    BD.user_add(id + 2000000000, 'group', '4 корпус')
                    send_message(id + 2000000000, 'Вы успешно подписались на обновление')
                elif msg == '/удалить подписку на обновление':
                    BD.user_delete(id + 2000000000)
                    send_message(id + 2000000000, 'Вы успешно удалили подписку на обновление')
                elif msg == '/расписание звонков':
                    send_message(id + 2000000000, 'Расписание звонков',
                                 upload_photo('pictures/звонки.png'))

            if event.from_user:  # обработка событий для сообщений в лс
                id = event.obj['message']['peer_id']
                # Возвращает 0 или 1, если человек имеется в группе... В зависимости от этого, выполняется код
                if isMember(id):
                    if msg == '1 корпус':
                        send_message(id, 'Расписание 1 корпус', upload_photo('pictures/download_zamena1k.png'),
                                     keyboard_bgc())
                    elif msg == '2 корпус':
                        send_message(id, 'Расписание 2 корпус', upload_photo('pictures/download_zamena2k.png'),
                                     keyboard_bgc())
                    elif msg == '3 корпус':
                        send_message(id, 'Расписание 3 корпус', upload_photo('pictures/download_zamena3k.png'),
                                     keyboard_bgc())
                    elif msg == '4 корпус':
                        send_message(id, 'Расписание 4 корпус', upload_photo('pictures/download_zamena4k.png'),
                                     keyboard_bgc())
                    elif msg == 'автоматическая отправка расписания':
                        send_message(id, 'Переход в меню редактирования автообновлений',
                                     keyboard=keyboard_auto_update_bgc())
                    elif msg == 'обновление 1 корпус':
                        BD.user_add(id, check_name(id), '1 корпус')
                        send_message(id, 'Вы успешно подписались на обновление')
                    elif msg == 'обновление 2 корпус':
                        BD.user_add(id, check_name(id), '2 корпус')
                        send_message(id, 'Вы успешно подписались на обновление')
                    elif msg == 'обновление 3 корпус':
                        BD.user_add(id, check_name(id), '3 корпус')
                        send_message(id, 'Вы успешно подписались на обновление')
                    elif msg == 'обновление 4 корпус':
                        BD.user_add(id, check_name(id), '4 корпус')
                        send_message(id, 'Вы успешно подписались на обновление')
                    elif msg == 'удалить подписку на обновление':
                        BD.user_delete(id)
                        send_message(id, 'Вы успешно удалили подписку на обновление')
                    elif msg == 'расписание звонков':
                        send_message(id, 'Расписание звонков', upload_photo('pictures/звонки.png'))
                    elif msg == 'назад':
                        send_message(id, 'Возвращаем вас в меню', None, keyboard_bgc())
                    elif msg == 'начать':
                        send_message(id, 'Привет, рад вас видеть', None, keyboard_bgc())
                    else:
                        send_message(id, 'Ошибка, данная команда не найдена', None, keyboard_bgc())
                else:
                    send_message(id, 'Для использования бота необходимо вступить в группу данного бота ВК', None,
                                 keyboard_bgc())
