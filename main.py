# -*- coding: utf-8 -*-
import telebot
from telebot import apihelper
from telebot import types
from telebot.types import Message, CallbackQuery

from const import *
from menu import Keyboard
from menu import InlineKeyboard

from datetime import datetime
from threading import Thread
import time
import sqlite3
import getRowOperands
import getFilterText
import actions

bot = telebot.TeleBot(token=TOKEN, threaded=True)
apihelper.proxy = {'socks5': PROXY}


def init_user(ui, f, l, un):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    row = tuple([ui if i == 0 else
                 str(f) if i == 1 else
                 str(l) if i == 2 else
                 str(un) if i == 3 else
                 0 for i in range(0, 29)])
    cursor.execute("INSERT OR REPLACE INTO users VALUES {}".format(row))
    connection.commit()
    connection.close()


def update_db(ui, properties, values):
    req = ''
    for i, j in enumerate(properties):
        req += "%s = '%s'" % (properties[i], values[i])
        if i + 1 < len(properties):
            req += ", "
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    ex = "UPDATE users SET {} WHERE user_id = {}".format(req, ui)
    cursor.execute(ex)
    connection.commit()
    connection.close()


def update_messages(message_id, flat_id, user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    ex = "INSERT INTO messages VALUES ({}, {}, {})".format(message_id, flat_id, user_id)
    cursor.execute(ex)
    connection.commit()
    connection.close()


def get_message(message_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    ex = "SELECT * FROM messages WHERE message_id = {}".format(message_id)
    rows = cursor.execute(ex).fetchone()
    connection.close()
    return rows


def get_last_message(userid):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    ex = "SELECT * FROM messages WHERE user_id = {} ORDER BY message_id DESC LIMIT 1".format(userid)
    row = cursor.execute(ex).fetchone()
    connection.close()
    return row[0]


def slog(type='info', txt=''):
    txt = type + datetime.now().strftime(" %d.%m.%Y %H:%M:%S.%f ") + str(txt) + '\n'
    # print(txt.replace('\n', ''))
    f = open('bot.log', 'a', encoding='utf-8')
    f.write(txt)
    f.close()


def getRow(flat, square, dist, reg, price, offset):
    global rcount
    rooms = getRowOperands.getflat(flat)
    dist = getRowOperands.getdist(dist)
    reg = getRowOperands.getreg(reg)
    square = getRowOperands.getsquare(square)
    price = getRowOperands.getprice(price)
    counter = 0
    w = 'WHERE'
    a = 'AND'
    request = ''
    if rooms != 'Any':
        if counter == 0:
            request = '%s (%s)' % (w, rooms)
        else:
            request = '%s %s (%s)' % (request, a, rooms)
        counter += 1
    if dist != 'Any':
        if counter == 0:
            request = '%s (%s)' % (w, dist)
        else:
            request = '%s %s (%s)' % (request, a, dist)
        counter += 1
    if reg != 'Any':
        if counter == 0:
            request = '%s %s' % (w, reg)
        else:
            request = '%s %s (%s)' % (request, a, reg)
        counter += 1
    if square != 'Any':
        if counter == 0:
            request = '%s %s' % (w, square)
        else:
            request = '%s %s (%s)' % (request, a, square)
        counter += 1
    if price != 'Any':
        if counter == 0:
            request = '%s %s' % (w, price)
        else:
            request = '%s %s (%s)' % (request, a, price)
        counter += 1
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    exe = "SELECT * FROM flats {}".format(request)
    rare_rows = cursor.execute(exe).fetchall()
    rows = []
    for row in rare_rows:
        rows.append([i for i in row])
    # random.shuffle(rows)
    connection.close()
    if len(rows) > 0:
        return rows[offset], len(rows)
    else:
        return [None for i in range(0, 8)], len(rows)


def get_flat(flat_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    exe = "SELECT * FROM flats WHERE Id = {}".format(flat_id)
    rare_rows = cursor.execute(exe).fetchall()
    rows = []
    for row in rare_rows:
        rows.append([i for i in row])
    connection.close()
    return rows[0]


@bot.message_handler(commands=["start"])
def start(m: Message):
    global stage, userid, firstname, lastname, username
    userid = m.from_user.id
    firstname = m.from_user.first_name
    lastname = m.from_user.last_name
    username = m.from_user.username
    stage = 'main'
    init_user(userid, firstname, lastname, username)
    update_db(userid, ['stage'], ['main'])
    Keyboard.main_menu(m)
    log = 'User %s @%s %s %s started work' % (userid, username, firstname, lastname)
    slog('info', log)


@bot.callback_query_handler(func=lambda c: True)
def inline(c: CallbackQuery):
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    ans = [j for i in cur.execute('SELECT * FROM users WHERE user_id = {}'.format(c.from_user.id)) for j in i]
    con.close()
    userid = ans[0]
    firstname = ans[1]
    lastname = ans[2]
    username = ans[3]
    r1, r2, r3, r4 = ans[5], ans[6], ans[7], ans[8]
    vco, tco, ttk, ztk = ans[9], ans[10], ans[11], ans[12]
    cao, sao, svao, vao, uvao, uao, uzao, zao, szao, nao = ans[13], ans[14], ans[15], ans[16], ans[17], ans[18], ans[
        19], ans[20], ans[21], ans[22]
    minsq, maxsq, minp, maxp, choice = ans[23], ans[24], ans[25], ans[26], ans[27]
    rooms = actions.changerooms(r1, r2, r3, r4)
    dist = actions.changedist(vco, tco, ttk, ztk)
    reg = actions.changereg(cao, sao, svao, vao, uvao, uao, uzao, zao, szao, nao)
    square = (minsq, maxsq)
    price = (minp, maxp)
    flat, rcount = getRow(rooms, square, dist, reg, price, choice)
    if c.data == "Контакты 📞":
        bot.send_message(c.message.chat.id, 'О нас')
    if rcount > 0:
        if c.data == "Select":
            flat_id = get_message(c.message.message_id)[1]
            selectflat(c.message, get_flat(flat_id), ans[0], ans[1], ans[2], ans[3])
        if c.data == "pdf":
            send_pdf(c.message, flat)
    if c.data == 'New':
        key = types.InlineKeyboardMarkup()
        select_but = types.InlineKeyboardButton(text='Выбрать ✅', callback_data='Select')
        key.add(select_but)
        bot.edit_message_reply_markup(chat_id=userid, message_id=c.message.message_id, reply_markup=key)
        log = 'User %s @%s %s %s back to menu via inline' % (userid, username, firstname, lastname)
        slog('info', log)
        init_user(userid, firstname, lastname, username)
        update_db(userid, ['stage'], ['main'])
        Keyboard.main_menu(c.message)

    if c.data == 'More':
        # key = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Выбрать ✅', callback_data='Select'))
        choice += 1
        update_db(userid, ['offset'], [choice])
        flat, rcount = getRow(rooms, square, dist, reg, price, choice)
        log = 'User %s @%s %s %s pressed "next" via inline' % (userid, username, firstname, lastname)
        slog('info', log)
        showflat(c.message, flat, choice, rcount)
        key = types.InlineKeyboardMarkup()
        select_but = types.InlineKeyboardButton(text='Выбрать ✅', callback_data='Select')
        key.add(select_but)
        bot.edit_message_reply_markup(chat_id=userid, message_id=c.message.message_id, reply_markup=key)


@bot.message_handler(content_types=['text'])
def message(m: Message):
    chatid = m.chat.id
    userid = m.from_user.id
    firstname = m.from_user.first_name
    lastname = m.from_user.last_name
    username = m.from_user.username
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    ans = [j for i in cur.execute('SELECT * FROM users WHERE user_id = {}'.format(userid)) for j in i]
    con.close()
    if len(ans) == 0:
        init_user(userid, firstname, lastname, username)
    stage = ans[4]
    r1, r2, r3, r4 = ans[5], ans[6], ans[7], ans[8]
    vco, tco, ttk, ztk = ans[9], ans[10], ans[11], ans[12]
    cao, sao, svao, vao, uvao, uao, uzao, zao, szao, nao = ans[13], ans[14], ans[15], ans[16], ans[17], ans[18], ans[
        19], ans[20], ans[21], ans[22]
    minsq, maxsq, minp, maxp, choice = ans[23], ans[24], ans[25], ans[26], ans[27]
    if m.text == 'Найти недвижимость 🔎':
        log = 'User %s @%s %s %s started searching' % (userid, username, firstname, lastname)
        slog('info', log)
        init_user(userid, firstname, lastname, username)
        update_db(userid, properties=['stage', 'offset'], values=['room', 0])
        Keyboard.select_room(m)

    elif m.text == 'Скачать':
        f = open(r'X:\pdfs\403276986.pdf', "rb")
        bot.send_chat_action(m.chat.id, action='upload_document')
        bot.send_document(m.chat.id, f)
        # bot.send_location(m.chat.id, latitude=55.791410, longitude=37.624480)

    elif m.text == 'Вернутся в меню ↩' or m.text == 'Новый поиск ↩' or m.text == '↩':
        log = 'User %s @%s %s %s back to menu' % (userid, username, firstname, lastname)
        slog('info', log)
        init_user(userid, firstname, lastname, username)
        update_db(userid, ['stage'], ['main'])
        Keyboard.main_menu(m)

    elif stage == 'room':
        if m.text == 'Студия':
            update_db(userid, ['r1'], [-1])
        elif m.text == '1 комната':
            update_db(userid, ['r1'], [1])
        elif m.text == '2 комнаты':
            update_db(userid, ['r2'], [1])
        elif m.text == '3 комнаты':
            update_db(userid, ['r3'], [1])
        elif m.text == '4 и более':
            update_db(userid, ['r4'], [1])
        elif m.text == 'Далее ➡':
            txt = 'Вы выбрали: ' + getFilterText.roomtext(r1, r2, r3, r4)
            log = 'User %s @%s %s %s selected room: %s %s %s %s' % (userid, username, firstname, lastname,
                                                                    r1, r2, r3, r4)
            slog('info', log)
            # bot.send_chat_action(m.chat.id, action="typing")
            # bot.send_message(m.chat.id, txt)
            update_db(userid, properties=['stage'], values=['dist'])
            Keyboard.select_dist(m)
        else:
            bot.send_chat_action(m.chat.id, action="typing")
            txt = 'Пожалуйста, выберите один из пунктов меню и нажмите <b>Далее</b>'
            bot.send_message(m.chat.id, txt, parse_mode='HTML')

    elif stage == 'dist':
        if m.text == 'Внутри кольцевой':
            update_db(userid, ['vco'], [1])
            vco = 1
        elif m.text == 'До 3 станций от кольца':
            update_db(userid, ['tco'], [1])
            tco = 1
        elif m.text == 'Внутри ТТК':
            update_db(userid, ['ttk'], [1])
            ttk = 1
        elif m.text == 'До 5 станций от кольца':
            update_db(userid, ['ztk'], [1])
            ztk = 1
        update_db(userid, properties=['stage'], values=['reg'])
        dist = getFilterText.getdist(vco, tco, ttk, ztk)
        log = 'User %s @%s %s %s selected dist: %s %s %s %s' % (userid, username, firstname, lastname,
                                                                vco,
                                                                tco,
                                                                ttk,
                                                                ztk)
        slog('info', log)
        # txt = 'Вы выбрали: ' + dist
        # bot.send_message(m.chat.id, txt)
        Keyboard.select_reg(m)

    elif stage == 'reg':
        if m.text == 'ЦАО ⏺':
            update_db(userid, ['cao'], [1])
        elif m.text == 'САО ⬆':
            update_db(userid, ['sao'], [1])
        elif m.text == '↗ СВАО':
            update_db(userid, ['svao'], [1])
        elif m.text == '➡ ВАО':
            update_db(userid, ['vao'], [1])
        elif m.text == '↘ ЮВАО':
            update_db(userid, ['uvao'], [1])
        elif m.text == 'ЮАО ⬇':
            update_db(userid, ['uao'], [1])
        elif m.text == 'ЮЗАО ↙':
            update_db(userid, ['uzao'], [1])
        elif m.text == 'ЗАО ⬅':
            update_db(userid, ['zao'], [1])
        elif m.text == 'СЗАО ↖':
            update_db(userid, ['szao'], [1])
        elif m.text == 'НАО (Новомоск.)':
            update_db(userid, ['nao'], [1])
        elif m.text == 'Далее ➡':
            update_db(userid, properties=['stage'], values=['square'])
            # txt = 'Вы выбрали: ' + getFilterText.regtext(cao, sao, svao, vao, uvao, uao, uzao, zao, szao, nao)
            log = 'User %s @%s %s %s selected reg: %s %s %s %s %s %s %s %s %s %s' % (
                userid,
                username,
                firstname,
                lastname,
                cao, sao,
                svao, vao,
                uvao, uao,
                uzao, zao,
                szao, nao)
            slog('info', log)
            # bot.send_chat_action(m.chat.id, action="typing")
            # bot.send_message(m.chat.id, txt)
            Keyboard.select_square(m, True)
        else:
            bot.send_chat_action(m.chat.id, action="typing")
            txt = 'Пожалуйста, выберите один из пунктов меню и нажмите <b>Далее</b>'
            bot.send_message(m.chat.id, txt, parse_mode='HTML')

    elif stage == 'square':
        if m.text != 'Далее ➡':
            if minsq == 0:
                try:
                    sq = int(m.text)
                    if sq < 0:
                        raise ValueError
                    if sq > 1000:
                        raise ValueError
                except Exception as e:
                    txt = 'Некорректно задана площадь, введите только число в м². Пример: 54'
                    log = 'User %s @%s %s %s entered incorrect square, %s' % (userid,
                                                                              username,
                                                                              firstname,
                                                                              lastname, e)
                    slog('erro', log)
                    bot.send_message(m.chat.id, txt)
                    Keyboard.select_square(m, True)
                else:
                    if sq == 0:
                        sq = -1
                    update_db(userid, ['minsq', 'stage'], [sq, 'price'])
                    # txt = 'Вы выбрали: ' + getFilterText.sqtext(sq)
                    log = 'User %s @%s %s %s selected square: %s' % (userid,
                                                                     username,
                                                                     firstname,
                                                                     lastname, sq)
                    slog('info', log)
                    # bot.send_chat_action(m.chat.id, action="typing")
                    # bot.send_message(m.chat.id, txt)
                    Keyboard.select_price(m, True)
        else:
            update_db(userid, properties=['stage'], values=['price'])
            # txt = 'Вы выбрали: ' + getFilterText.sqtext(0)
            log = 'User %s @%s %s %s selected any square' % (userid, username,
                                                             firstname,
                                                             lastname)
            slog('info', log)
            # bot.send_chat_action(m.chat.id, action="typing")
            # bot.send_message(m.chat.id, txt)
            Keyboard.select_price(m, True)

    elif stage == 'price':
        if m.text != 'Далее ➡':  # or minp != -1 or maxp != -1:
            if minp == 0:
                # print('minp=0')
                try:
                    pr = int(m.text)
                    if pr < 0:
                        raise ValueError
                except Exception as e:
                    txt = 'Некорректно задана цена, введите только число в рублях. Пример: 35000'
                    log = 'User %s @%s %s %s entered incorrect min price, %s' % (userid,
                                                                                 username,
                                                                                 firstname,
                                                                                 lastname, e)
                    slog('erro', log)
                    bot.send_message(m.chat.id, txt)
                    Keyboard.select_price(m, True)
                else:
                    # print('minp else')
                    if pr == 0:
                        pr = -1
                    update_db(userid, ['minp'], [pr])
                    Keyboard.select_price(m, False)
            elif maxp == 0:
                # print('maxp=0')
                try:
                    pr = int(m.text)
                    if pr < 0:
                        raise ValueError
                except Exception as e:
                    txt = 'Некорректно задана цена, введите только число в рублях. Пример: 35000'
                    log = 'User %s @%s %s %s entered incorrect max price, %s' % (userid,
                                                                                 username,
                                                                                 firstname,
                                                                                 lastname, e)
                    slog('erro', log)
                    bot.send_message(m.chat.id, txt)
                    Keyboard.select_price(m, False)
                else:
                    # print('maxp else')
                    if pr == 0:
                        pr = -1
                    if minp < pr:
                        '''text = getFilterText.ffilter(r1, r2, r3, r4,
                                                     vco, tco, ttk, ztk,
                                                     cao, sao, svao, vao, uvao, uao, uzao, zao, szao, nao,
                                                     minsq, pr)'''
                        log = 'User %s @%s %s %s selected price: %s' % (
                            userid,
                            username,
                            firstname,
                            lastname, pr)
                        slog('info', log)
                        # bot.send_chat_action(m.chat.id, action="typing")
                        # bot.send_message(m.chat.id, text)
                        update_db(userid, ['maxp', 'stage'], [pr, 'first_show'])
                        Keyboard.show_menu_first(m)
                    else:
                        update_db(userid, ['minp', 'maxp'], [0, 0])
                        txt = 'Некорректно заданы пределы, повторите ввод'
                        bot.send_message(m.chat.id, txt)
                        Keyboard.select_price(m, True)
        else:
            update_db(userid, properties=['stage'], values=['first_show'])
            log = 'User %s @%s %s %s selected any price' % (userid,
                                                            username,
                                                            firstname,
                                                            lastname)
            slog('info', log)
            # bot.send_chat_action(m.chat.id, action="typing")
            # bot.send_message(m.chat.id, text)
            Keyboard.show_menu_first(m)

    elif stage == 'first_show':
        rooms = actions.changerooms(r1, r2, r3, r4)
        dist = actions.changedist(vco, tco, ttk, ztk)
        reg = actions.changereg(cao, sao, svao, vao, uvao, uao, uzao, zao, szao, nao)
        square = (minsq, maxsq)
        price = (minp, maxp)

        flat, rcount = getRow(rooms, square, dist, reg, price, choice)
        Keyboard.show_menu(m, rcount)
        log = 'User %s @%s %s %s pressed "first show"' % (userid, username, firstname, lastname)
        slog('info', log)
        if rcount > 0:
            showflat(m, flat, choice, rcount)
            update_db(userid, properties=['stage'], values=['show'])
        else:
            Keyboard.norows(m)
            init_user(userid, firstname, lastname, username)
            update_db(userid, properties=['stage'], values=['room'])

    elif stage == 'show':
        rooms = actions.changerooms(r1, r2, r3, r4)
        dist = actions.changedist(vco, tco, ttk, ztk)
        reg = actions.changereg(cao, sao, svao, vao, uvao, uao, uzao, zao, szao, nao)
        square = (minsq, maxsq)
        price = (minp, maxp)
        flat, rcount = getRow(rooms, square, dist, reg, price, choice)
        if m.text == 'Выбрать ✅':
            selectflat(m, flat, userid, firstname, lastname, username)
            log = 'User %s @%s %s %s pressed "show"' % (userid, username, firstname, lastname)
            slog('info', log)
        else:
            if m.text == '◀ Предыдущая':
                if choice > 0:
                    choice -= 1
                else:
                    choice = 0
            if m.text == 'Ещё ▶':
                if choice < rcount - 1:
                    choice += 1
                    update_db(userid, properties=['offset'], values=[choice])
                    flat, rcount = getRow(rooms, square, dist, reg, price, choice)
                    log = 'User %s @%s %s %s pressed "next" %s' % (userid, username, firstname, lastname, choice)
                    slog('info', log)
                    try:
                        key = types.InlineKeyboardMarkup()
                        select_but = types.InlineKeyboardButton(text='Выбрать ✅', callback_data='Select')
                        key.add(select_but)
                        bot.edit_message_reply_markup(chat_id=userid, message_id=get_last_message(userid),
                                                  reply_markup=key)
                    except: pass
                    showflat(m, flat, choice, rcount)
                else:
                    text = 'Закончились квартиры в выбранном фильтре, нажмите "Новый поиск" для составления нового фильтра'
                    bot.send_chat_action(m.chat.id, action="typing")
                    bot.send_message(m.chat.id, text)

    elif m.text == 'Задать вопрос ❓':
        update_db(userid, properties=['stage'], values=['question'])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Какой у вас вопрос?')
        log = 'User %s @%s %s %s pressed "question"' % (userid, username, firstname, lastname)
        slog('info', log)

    elif m.text == 'О нас 📝':
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Скоро здесь появится информация')
        log = 'User %s @%s %s %s pressed "about"' % (userid, username, firstname, lastname)
        slog('info', log)

    elif m.text == 'Контакты 📞':
        log = 'User %s @%s %s %s pressed "contacts"' % (userid, username, firstname, lastname)
        slog('info', log)
        InlineKeyboard.box(m)

    elif stage == 'question':
        update_db(userid, properties=['stage'], values=['main'])
        out = ('Пользователь ' +
               str(firstname) + ' ' +
               str(lastname) + ' @' +
               str(username) + " задал вопрос:\n%s" % m.text)
        log = 'User %s @%s %s %s asked question: %s' % (userid, username, firstname, lastname, m.text)
        slog('info', log)
        bot.send_message(433242252, out)  # я
        bot.send_message(318453750, out)  # median
        bot.send_chat_action(m.chat.id, action='typing')
        bot.send_message(m.chat.id,
                         'Ваш вопрос записан и уже рассматривается, можете продолжить пользоватся остальными услугами')

    elif 'хуй' in m.text.lower() or 'пизда' in m.text.lower() or 'бля' in m.text.lower():
        log = 'User %s @%s %s %s ahyel v krai' % (userid, username, firstname, lastname)
        slog('info', log)
        bot.send_message(m.chat.id, '👁')

    else:
        if m.reply_to_message is None:
            bot.send_chat_action(m.chat.id, action='typing')
            bot.send_message(m.chat.id,
                             'Ошибка. Команда не найдена')

    if m.reply_to_message is not None:
        rep_message = get_message(m.reply_to_message.message_id)
        if rep_message is not None:
            selectflat(m, get_flat(rep_message[1]), userid, firstname, lastname, username)


def showflat(m: Message, flat, choice, rcount):
    art = str(flat[0])
    r = str(flat[2])
    s = str(flat[1])
    d = str(flat[4]).replace('\r', '').replace('|', ', ')
    p = str(flat[3])
    a = ("Вариант <b>" + str(choice + 1) + " из " + str(rcount) + '</b>\nID квартиры <b>' + art + '</b>')  # + '\n' +
    key = types.InlineKeyboardMarkup()
    select_but = types.InlineKeyboardButton(text='Выбрать ✅', callback_data='Select')
    # pdf_but = types.InlineKeyboardButton(text='Презентация', callback_data='pdf')
    # new_but = types.InlineKeyboardButton(text='Новый поиск', callback_data='New')
    more_but = types.InlineKeyboardButton(text='Ещё ▶', callback_data='More')
    key.add(select_but, more_but)  # , pdf_but)
    # bot.send_chat_action(m.chat.id, action='typing')
    # bot.send_message(m.chat.id, a, reply_markup=key)
    send_pdf(m, flat, a, key)


def selectflat(m: Message, flat, userid, firstname, lastname, username):
    if firstname is None:
        firstname = ' '
    if lastname is None:
        lastname = ' '
    if username is None:
        username = ' '
    art = str(flat[0])
    r = str(flat[2])
    s = str(flat[1])
    d = str(flat[4]).replace('\r', '').replace('|', ', ')
    p = str(flat[3])
    a = (r + " комнатная квартира, площадью " + s + " м², по адресу " +
         d + "\nЦена: " + p + " тыс. руб/месяц, артикул " + art)
    out = ('Пользователь ' +
           str(firstname) + ' ' +
           str(lastname) + ' @' +
           str(username) + " выбрал квартиру:\n" + a)
    log = 'User %s @%s %s %s selected flat id %s, r %s, s %s, d %s, p %s' % (userid, username, firstname, lastname,
                                                                             art, r, s, d, p)
    slog('info', log)
    bot.send_message(433242252, out)  # я
    bot.send_message(318453750, out)  # median admin
    out = ("Вы выбрали:\n"
           + a +
           "\n\nСвяжитесь с нашим риелтором @medianadmin для продолжения работы, он уже оповещен о вашем выборе")
    bot.send_chat_action(m.chat.id, action='typing')
    bot.send_message(m.chat.id, out)


def send_action(id, ac):
    return bot.send_chat_action(id, action=ac)


def send_doc(id, f, mar, cap):
    return bot.send_document(id, f, reply_markup=mar, caption=cap, parse_mode='HTML')


def send_pdf(m: Message, flat, a, key):
    flat_id = flat[0]
    lat = str(flat[5])[:-2]
    lat = float(lat[:2] + '.' + lat[2:])
    lon = str(flat[6])[:-2]
    lon = float(lon[:2] + '.' + lon[2:])
    f = open(PDF_PATH + '/%s.pdf' % flat_id, "rb")
    # bot.send_chat_action(m.chat.id, action='upload_document')
    # bot.send_document(m.chat.id, f, reply_markup=key, caption=a)  # , caption='Презентация %s' % flat_id)
    Thread(target=send_action, args=(m.chat.id, 'upload_document')).start()
    # Thread(target=send_doc, args=(m.chat.id, f, key, a)).start()
    message_info = send_doc(m.chat.id, f, key, a)
    update_messages(message_info.message_id, flat[0], m.chat.id)


while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=20)
    except Exception as E:
        slog('cri', E)
        time.sleep(2)
