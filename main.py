import telebot
from telebot import apihelper
from telebot import types
from telebot.types import Message

from const import TOKEN
from const import PROXY
from menu import Keyboard
from menu import InlineKeyboard

import time
import sqlite3
import getRowOperands
import getFilterText
import actions

bot = telebot.TeleBot(token=TOKEN, threaded=False)
apihelper.proxy = {'socks5': PROXY}

# chat id 433242252

rooms = 0
square = 0
choice = 0
dist = ' '
price = 0
opernum = 0
flat = ' '
rcount = 0
a = ''
userid = 0
firstname = ''
lastname = ''
username = ''
flag = 0

# def getRow(id: int, rnum: int):
#     dbConn = sqlite3.connect("CIAN.db")
#     cursor = dbConn.cursor()
#     row = cursor.execute("SELECT * FROM Flat1 ORDER BY P2 ASC LIMIT 1 OFFSET {}".format(rnum)).fetchone()
#     if row:
#         return str(row[id])


def getRow(id: int, rnum: int, flat: int, square, dist, price):
    global rcount
    flat = getRowOperands.getflat(flat)
    square = getRowOperands.getsquare(square)
    dist = getRowOperands.getdist(dist)
    price = getRowOperands.getprice(price)
    counter = 0
    w = 'WHERE '
    a = ' AND '
    request = ''
    if square != 'Any':
        if counter == 0:
            request = w + square
        else:
            request = request + a + square
        counter += 1
    if dist != 'Any':
        if counter == 0:
            request = w + dist
        else:
            request = request + a + dist
        counter += 1
    if price != 'Any':
        if counter == 0:
            request = w + price
        else:
            request = request + a + price
        counter += 1

    connection = sqlite3.connect("CIAN.db")
    cursor = connection.cursor()
    final = "SELECT * FROM {} {} ORDER BY P2 ASC LIMIT 1 OFFSET {}".format(flat, request, rnum)
    row = cursor.execute(final).fetchone()

    cfinal = "SELECT * FROM {} {}".format(flat, request)
    crow = cursor.execute(cfinal).fetchall()
    rcount = len(crow)

    if row is None:
        return 0
    else:
        return str(row[id])


@bot.message_handler(commands=["start"])
def start(m: Message):
    global userid, firstname, lastname, username
    userid = m.from_user.id
    firstname = m.from_user.first_name
    lastname = m.from_user.last_name
    username = m.from_user.username

    Keyboard.main_menu(m)
    # print(m.chat.id)
    # print(m.from_user.id)
    # print(m.from_user.first_name)
    # print(m.from_user.last_name)
    # print(m.from_user.username)
    print("chatid: " + m.chat.id +
          " ;userid: " + m.from_user.id +
          " ;firstname: " + m.from_user.first_name +
          " ;lastname: " + m.from_user.last_name +
          " ;username: " + m.from_user.username)
    # print("=========")


# @bot.message_handler(commands=["chat"])
def inline(m: Message):
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="NumberOne", callback_data="NumberOne")
    but_2 = types.InlineKeyboardButton(text="NumberTwo", callback_data="NumberTwo")
    but_3 = types.InlineKeyboardButton(text="NumberTree", callback_data="NumberTree")
    key.add(but_1, but_2, but_3)
    bot.send_message(m.chat.id, "ВЫБЕРИТЕ КНОПКУ", reply_markup=key)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'NumberOne':
        bot.send_message(c.message.chat.id, 'Это кнопка 1')
    if c.data == 'NumberTwo':
        bot.send_message(c.message.chat.id, 'Это кнопка 2')
    if c.data == 'NumberTree':
        key = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="NumberOne", callback_data="NumberOne")
        but_2 = types.InlineKeyboardButton(text="NumberTwo", callback_data="NumberTwo")
        but_3 = types.InlineKeyboardButton(text="NumberTree", callback_data="NumberTree")
        key.add(but_1, but_2, but_3)
        bot.send_message(c.message.chat.id, 'Это кнопка 3', reply_markup=key)
    if c.data == "Контакты 📞":
        bot.send_message(c.message.chat.id, 'О нас')
    if c.data == "Select":
        selectflat(c.message)


@bot.message_handler(content_types=['text'])
def message(m: Message):
    global rooms, square, choice, flat, dist, price, a, rcount, userid, firstname, lastname, username, flag
    userid = m.from_user.id
    firstname = m.from_user.first_name
    lastname = m.from_user.last_name
    username = m.from_user.username
    if m.text == 'Найти недвижимость 🔎':
        choice = 0
        Keyboard.select_room(m)

    elif m.text == 'Вернутся в меню ↩':
        Keyboard.main_menu(m)

    elif (m.text == '1 комната') | (m.text == '2 комнаты') | (m.text == '3 комнаты') | (m.text == '4 и более'):
        rooms = actions.changerooms(m)
        Keyboard.select_dist(m)

    elif m.text == 'ЦАО ⏺' or m.text == 'САО ⬆' or m.text == '↗ СВАО' or m.text == '➡ ВАО' or m.text == '↘ ЮВАО' or m.text == 'ЮАО ⬇' or m.text == 'ЮЗАО ↙' or m.text == 'ЗАО ⬅' or m.text == 'СЗАО ↖' or m.text == 'НАО (Новомосковский)' or m.text == 'Любой 🔀':
        dist = actions.changedist(m)
        Keyboard.select_square(m)

    elif m.text == 'Менее 50 м²' or m.text == '50-100 м²' or m.text == '100-200 м²' or m.text == 'Более 200 м²' or m.text == 'Любая площадь 🌍':
        square = actions.changesqure(m)
        Keyboard.select_price(m)

    elif m.text == '<30 тыс. руб' or m.text == '30-50 тыс. руб' or m.text == '50-100 тыс. руб' or m.text == '>100 тыс. руб' or m.text == 'Любая цена 💰':
        price = actions.changeprice(m)
        text = ("Ваш фильтр: " +
                getFilterText.getflat(rooms) + " комнатная квартира в " +
                getFilterText.getdist(dist) +
                getFilterText.getsquare(square) +
                getFilterText.getprice(price))
        bot.send_message(m.chat.id, text)
        Keyboard.show_menu_first(m)

    elif m.text == 'Показать результат ⬆':
        getRow(0, choice, rooms, square, dist, price)
        flag = 0
        Keyboard.show_menu(m, rcount)
        if getRow(0, choice, rooms, square, dist, price) == 0:
            Keyboard.norows(m)
        else:
            showflat(m)

    elif m.text == 'Показать результат ⤴' or m.text == '◀ Предыдущая' or m.text == 'Следующая ▶' or m.text == 'Выбрать ✅':
        flag = 1
        if getRow(0, choice, rooms, square, dist, price) == 0:
            Keyboard.norows(m)
        else:
            if m.text == 'Выбрать ✅':
                selectflat(m)
            else:
                if m.text == '◀ Предыдущая':
                    if choice > 0:
                        choice -= 1
                    else:
                        choice = 0
                if m.text == 'Следующая ▶':
                    if choice < rcount - 1:
                        choice += 1
                showflat(m)

    elif m.text == 'Задать вопрос ❓':
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Какой у вас вопрос?')

    elif m.text == 'О нас 📝':
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Скоро здесь появится информация')

    elif m.text == 'Контакты 📞':
        # key = types.InlineKeyboardMarkup()
        # but_1 = types.InlineKeyboardButton(text="NumberOne", callback_data="NumberOne")
        # but_2 = types.InlineKeyboardButton(text="NumberTwo", callback_data="NumberTwo")
        # but_3 = types.InlineKeyboardButton(text="NumberTree", callback_data="NumberTree")
        # key.add(but_1, but_2, but_3)
        # bot.send_chat_action(m.chat.id, action="typing")
        # bot.send_message(m.chat.id, 'Тут контакты', reply_markup=key)
        InlineKeyboard.box(m)

    elif m.text == 'Назад':
        kek = 1
    else:
        bot.send_chat_action(m.chat.id, action='typing')
        bot.send_message(m.chat.id,
                         'Ваш вопрос записан и уже рассматривается, можете продолжить пользоватся остальными услугами')


def showflat(m: Message):
    global rooms, square, choice, flat, dist, price, a, rcount, userid, firstname, lastname, username, flag
    text = ("Вариант " + str(choice + 1) + " из " + str(rcount))
    a = (str(getRow(0, choice, rooms, square, dist, price)) +
         " комнатная квартира, площадью " +
         str(getRow(1, choice, rooms, square, dist, price))
         + "м², в " +
         str(getRow(5, choice, rooms, square, dist, price)) +
         "\nЦена: " +
         str(getRow(10, choice, rooms, square, dist, price)) +
         " тыс. руб/месяц")
    b = ' '
    media = []
    for i in range(3):
        if i == 0:
            media.append(types.InputMediaPhoto(getRow(i + 6, choice, rooms, square, dist, price), text))
        else:
            media.append(types.InputMediaPhoto(getRow(i + 6, choice, rooms, square, dist, price), b))
    flat = getRow(4, choice, rooms, square, dist, price)
    Keyboard.send_photo(m, media, choice, flag)
    key = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Выбрать ✅', callback_data='Select')
    key.add(button)
    bot.send_message(m.chat.id, a, reply_markup=key)


def selectflat(m: Message):
    global firstname, lastname, username
    if firstname is None:
        firstname = ' '
    if lastname is None:
        lastname = ' '
    if username is None:
        username = ' '
    data = (getRow(0, choice, rooms, square, dist, price) +
            ' комната, ' +
            getRow(1, choice, rooms, square, dist, price) +
            'м²,' + ' в ' +
            getRow(5, choice, rooms, square, dist, price) +
            ', по цене ' +
            getRow(10, choice, rooms, square, dist, price) +
            ' тыс. руб ' +
            getRow(4, choice, rooms, square, dist, price))
    out = ('Пользователь ' +
           str(firstname) + ' ' +
           str(lastname) + ' @' +
           str(username) +
           " выбрал квартиру: \n" +
           str(data))
    bot.send_message(433242252, out)
    bot.send_message(318453750, out)
    # bot.send_message(318453750, out) ne robit
    out = ("Вы выбрали:\n"
           + a +
           "\n\nСвяжитесь с нашим риелтором @Azbuka19 для продолжения работы. Он уже оповещен о вашем выборе и готов помочь сию же секунду")
    bot.send_message(userid, out)


while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=20)
    except Exception as E:
        print(E.args)
        time.sleep(2)
