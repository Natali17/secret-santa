# -------------------------------------------------------
# Secret Santa
# python3
# encoding: utf8
# (C) 2021 Natasha Kropivnitskaya, Dolgoprudny, Russia
# Moscow Institute of Physics and Technologies (MIPT)
# Released under GNU Public License (GPL)
# email kropivnitskaya@phystech.edu
# --------------------------------------------------------
import openpyxl
import random
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import pandas as pd
import asyncio
import time
import csv

token = "xxx"
user_token = 'xxx'

users = [343115381, 235876424]


def pair(users_list, user):
    '''
	Функция для нахождения пары для данного пользователя. Из списка всех пользователей выбирается следующий.
	Если на вход подается последний, то функция возвращает первого пользователя.
	'''
    index = users_list.index(user) + 1
    if index > len(users_list) - 1:
        index = 0
    try:
        return users_list[index]
    except ValueError:
        return 'Такой пользователь не найден'


session = requests.Session()
vk_session = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def test():
    '''
	Функция для определения людей, которые не включили сообщения группы.
	Список всех выводится в терминал и таблицу в excel
	'''
    list_of_faggots = [[], []]
    print("Testing is running")

    vk = vk_session
    for user in users:
        try:
            vk.messages.send(user_id=user, message="", random_id=random.randint(-2147483648, +2147483648))
        except:
            userdata = vk.method("users.get", {"user_ids": user})
            print(userdata[0]['first_name'] + ' ' + userdata[0]['last_name'] + ' (' + str(
                user) + ')' + 'не подтвердил сообщение')
            list_of_faggots[0].append(userdata[0]['first_name'] + ' ' + userdata[0]['last_name'])
            list_of_faggots[1].append('https://vk.com/id' + str(user))

        with open("list_of_faggots.csv", "w") as file:
            writer = csv.writer(file)
            for x in list_of_faggots[0]:
                writer.writerow(x)


def main():
    '''
	Основная функция. Если пользователь пишет в группу, то Тайный Санта находит его пару функцией pair и отсылает ему сообщение пользователя и выводится сообщение об отправке.
	В терминале отображается история сообщений
	'''

    print("Spam machine launched")
    from vk_api.longpoll import VkLongPoll, VkEventType
    vk = vk_session.get_api()
    vk_for_getting_names = vk_session
	for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.text != '':  # Если написали заданную фразу
                if event.from_user:  # Если написали в ЛС
                    addressee = pair(users, event.user_id)
                    userdata = vk_for_getting_names.method("users.get", {"user_ids": addressee})
                    addressee_name = userdata[0]['first_name'] + ' ' + userdata[0]['last_name']
                    userdata = vk_for_getting_names.method("users.get", {"user_ids": event.user_id})
                    addresser_name = userdata[0]['first_name'] + ' ' + userdata[0]['last_name']
                    vk.messages.send(user_id=addressee,
                                     message="Вам сообщение от Вашего Тайного Санты!\n" + event.text + "\n\nЧтобы ответить, напишите что-нибудь в ответ!",
                                     random_id=random.randint(-2147483648, +2147483648))
                    vk.messages.send(user_id=event.user_id, message='Я передал сообщение',
                                     random_id=random.randint(-2147483648, +2147483648))
                    print(addresser_name + ' (' + str(event.user_id) + ')' + " написал \"" + str(
                        event.text) + "\" " + addressee_name + ' (' + str(addressee) + ')')


key = input('Введите main или test: ')
if key == 'main':
    while True:
        try:
            main()
        except requests.exceptions.ReadTimeout:
            print('Время ответа вышло')
        except requests.exceptions.ConnectionError:
            print('Потеряно соединение с сервером')
elif key == 'test':
    test()
