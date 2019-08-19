from typing import Callable
import random

# from aiogram.types import ReplyKeyboardRemove, \
# ReplyKeyboardMarkup, KeyboardButton, \
# InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import pandas as pd
from pandas import DataFrame
import os
import numpy as np
import pprint

token = '933498089:AAHf5NQGnL53mckLs4uCSyF7A-Rso55eMKE'
telebot.apihelper.proxy = {'https': 'socks5://geek:socks@t.geekclass.ru:7777'}
bot = telebot.TeleBot(token=token)
# ========================================================================

Rooms = {'hunter_house': ['m'],
                 'korostel': ['0'],
                 '10': ['0'],
                 '11': ['0'],
                 '12': ['0'],
                 '1_bath_house': ['0'],
                 '2_bath_house': ['0'],
         }

Players = {
    'user_id': [0],
    # 827267152
    'user_name': ['Great_Admin'],
    'gps': ['0'],
    'was_in korostel': [0],
    'was_in 10': [0],
    'was_in 11': [0],
    'was_in 12': [0],
    'was_in 1_bath_house': [0],
    'was_in 2_bath_house': [0],
    'money': [0],
    'power': [3],
    'exp': [0]
}

rooms = DataFrame(Rooms, columns=['hunter_house', 'korostel', '10', '11', '12', '1_bath_house', '2_bath_house'])
players = DataFrame(Players,
                    columns=['user_id', 'user_name', 'gps', 'was_in korostel', 'was_in 10', 'was_in 11', 'was_in 12',
                             'was_in 1_bath_house', 'was_in 2_bath_house', 'money', 'power', 'exp'])
with open('rules', mode='r', encoding='utf-8') as f:
    rulestxt = f.read()

bosses = {'easy': 10, 'normal': 20, 'hard': 30}
all_bosses = ['easy', 'normal', 'hard']


# пошли классы локаций:


class BossLocation:
    def __init__(self, ids, power):  # ids это массив с id
        global all_bosses
        global bosses
        self.bosshp = bosses[all_bosses[random.randrange(0, 2)]]
        self.money_prize = self.bosshp * 0.5
        self.power_prize = self.bosshp * 0.5
        self.xp_prize = self.bosshp * 0.5
        self.id = ids
        self.power = power

    def fighting(self):
        global players
        if self.power >= self.bosshp:
            ntf = np.array([random.randrange(1, 6) for i in range(self.power)])
            nums = len(ntf[ntf > 3])
            if nums >= self.bosshp:
                for i in self.id:
                    players['power'][user_search[i]] += self.power_prize
                    players['exp'][user_search[i]] += self.xp_prize
                    players['money'][user_search[i]] += self.money_prize
                return [2, self.money_prize, self.power_prize, self.xp_prize]
            return [1]
        return [0]


class ShopLocation:
    def __init__(self, id, power):
        self.id = id
        self.power = power

    def buy_power(self):
        global players
        if self.power * 50 <= players['money'][user_search[self.id]]:
            players['money'][user_search[self.id]] -= self.power * 50
            players['power'][user_search[self.id]] += self.power
            return [1, players]
        else:
            return [0, players]


multi_people = 0
powers = []
ids = []


class MultiLocation:
    def __init__(self, id, power):
        self.id = id
        self.power = power

    def threetowin(self):
        global powers
        global ids
        global multi_people
        multi_people += 1
        powers.append(self.power)
        ids.append(self.id)
        if multi_people == 3:
            BossLocation(1, 2)  # читывая то, что у нас складываются силы
        ids1, ids = ids, []
        powers = []
        multi_people = 0
        return players


def smivka(chislo):  # на вход поступает число от 1 до 3
    if chislo == random.choice([1, 2, 3]):
        return True  # смылись
    else:
        return False  # не смылись


@bot.message_handler(commands=['start', 'rules'])
def start(message):
    global players
    user = message.chat.id
    if message.text == '/start':
        if user not in set(players.user_id):
            bot.send_message(user, "Введите ник:")
            players = players.append({
                'user_id': user,
                'user_name': '0',
                'gps': '0',
                'was_in korostel': 0,
                'was_in 10': 0,
                'was_in 11': 0,
                'was_in 12': 0,
                'was_in 1_bath_house': 0,
                'was_in 2_bath_house': 0,
                'money': 0,
                'power': 90,
                'exp': 0
            }, ignore_index=True)


ind = 0
user_search = {}
qr_places = {}
with open('codes/codes.txt', 'r') as f:
    c = f.read().split('\n')
    qr_places[c[0]] = 'hunter_house'
    qr_places[c[1]] = 'karastel'
    qr_places[c[2]] = '10'
    qr_places[c[3]] = '11'
    qr_places[c[4]] = '12'
    qr_places[c[5]] = '1_bath_house'
    qr_places[c[6]] = '2_bath_house'
print(qr_places)


@bot.message_handler(content_types=['text'])
def welcome(message):
    global ind
    global players
    ind += 1
    userid = message.chat.id
    user_search[userid] = ind
    bot.send_message(userid, rulestxt)
    userindex = players.user_id[players.user_id == userid].index[0]
    if (players[players.user_id == userid].user_name == '0')[userindex]:
        bot.send_message(userid, ('Твой ник: ' + message.text))
        user = bot.send_message(userid, 'Ты готов приступить к игре, введи ключ')
        players.loc[userindex, 'user_name'] = message.text
        print(players)
        bot.register_next_step_handler(user, process_qr_step)


def process_qr_step(message):
    global qr_places
    chat_id = message.chat.id
    qr = message.text
    #    user = user_dict[chat_id]
    bot.send_message(chat_id, 'Welcome to ' + qr_places[qr] + ', here is a ' + rooms[qr_places[qr]])
    place = qr_places[qr]
    if rooms[place][0] == 'm':
        bot.send_message(chat_id, 'Now you have to fight, i believe, that you have read the rules.')
        ans = BossLocation([chat_id], players['power'][user_search[chat_id]])
        ans = ans.fighting()
        if ans[0] == 2:
            bot.send_message(chat_id, "VICTORY! Stats have been updated")
        elif ans[0] == 1:
            bot.send_message(chat_id, "You've lost. Money and power points were reduced by half")
            players['power'][user_search[chat_id]] /= 2
            players['exp'][user_search[chat_id]] /= 2
            players['money'][user_search[chat_id]] /= 2
        elif ans[0] == 0:
            bot.send_message(chat_id, "You've lost. Try to run out - enter a number from 1 to 3")
            if smivka(random.randint(1, 3)):
                bot.send_message(chat_id, "Смылся")
            else:
                bot.send_message(chat_id, 'Не смылся')
                players['power'][user_search[chat_id]] /= 2
                players['exp'][user_search[chat_id]] /= 2
                players['money'][user_search[chat_id]] /= 2


bot.polling(none_stop=True)
