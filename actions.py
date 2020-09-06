import telebot
from telebot import types
from telebot import apihelper
from telebot.types import Message

from const import TOKEN
from const import PROXY

bot = telebot.TeleBot(token=TOKEN, threaded=False)
apihelper.proxy = {'https': PROXY}


def changerooms(m: Message):
    if m.text == '1 комната':
        rooms = 1
    if m.text == '2 комнаты':
        rooms = 2
    if m.text == '3 комнаты':
        rooms = 3
    if m.text == '4 и более':
        rooms = 4
    # if m.text == 'Любое количество комнат 🏢':
    #     rooms = 4
    return rooms


def changedist(m: Message):
    if m.text == 'ЦАО ⏺':
        dist = 'ЦАО'
    if m.text == 'САО ⬆':
        dist = 'САО'
    if m.text == '↗ СВАО':
        dist = 'СВАО'
    if m.text == '➡ ВАО':
        dist = 'ВАО'
    if m.text == '↘ ЮВАО':
        dist = 'ЮВАО'
    if m.text == 'ЮАО ⬇':
        dist = 'ЮАО'
    if m.text == 'ЮЗАО ↙':
        dist = 'ЮЗАО'
    if m.text == 'ЗАО ⬅':
        dist = 'ЗАО'
    if m.text == 'СЗАО ↖':
        dist = 'СЗАО'
    if m.text == 'НАО (Новомосковский)':
        dist = 'НАО'
    if m.text == 'Любой 🔀':
        dist = 'Any'
    return dist


def changesqure(m: Message):
    if m.text == 'Менее 50 м²':
        square = 50
    if m.text == '50-100 м²':
        square = 100
    if m.text == '100-200 м²':
        square = 200
    if m.text == 'Более 200 м²':
        square = 201
    if m.text == 'Любая площадь 🌍':
        square = 202
    return square


def changeprice(m: Message):
    if m.text == '<30 тыс. руб':
        price = 30
    if m.text == '30-50 тыс. руб':
        price = 40
    if m.text == '50-100 тыс. руб':
        price = 75
    if m.text == '>100 тыс. руб':
        price = 100
    if m.text == 'Любая цена 💰':
        price = 101
    return price
