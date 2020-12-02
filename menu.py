import telebot
from telebot import types
from telebot import apihelper

from const import TOKEN
from const import PROXY

bot = telebot.TeleBot(token=TOKEN, threaded=False)
apihelper.proxy = {'https': PROXY}


class Keyboard:
    def main_menu(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Найти недвижимость 🔎']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Контакты 📞', 'Задать вопрос ❓']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Выберите необходимый пункт меню', reply_markup=keyboard)

    def select_room(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Студия', '1 комната']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['2 комнаты', '3 комнаты', '4 и более']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Далее ➡']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Выберите количество комнат или нажмите <b>Далее</b>\n<i>(один или несколько вариантов)</i>',
                         reply_markup=keyboard, parse_mode='HTML')

    def select_dist(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Внутри кольцевой', 'До 3 станций от кольца']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Внутри ТТК', 'До 5 станций от кольца']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Любая станция ➡']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Выберите максимальное расстояние от центра <i>(один вариант)</i>', reply_markup=keyboard, parse_mode='HTML')

    def select_reg(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['СЗАО ↖', 'САО ⬆', '↗ СВАО']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['ЗАО ⬅', 'ЦАО ⏺', '➡ ВАО']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['ЮЗАО ↙', 'ЮАО ⬇', '↘ ЮВАО']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['↩', 'НАО (Новомоск.)', 'Далее ➡']])  # 'Любой 🔀'
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Выберите административный округ или нажмите <b>Далее</b>\n<i>(один или несколько вариантов)</i>',
                         reply_markup=keyboard, parse_mode='HTML')

    def select_square(m, f):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Далее ➡']])
        bot.send_chat_action(m.chat.id, action="typing")
        if f:
            txt = 'Введите минимальную желаемую площадь в м² или нажмите <b>Далее</b>\n<i>(пример: 54)</i>'
        else:
            txt = 'Введите максимальную желаемую площадь в м² или нажмите <b>Далее</b>\n<i>(пример: 150)</i>'
        bot.send_message(m.chat.id, txt, reply_markup=keyboard, parse_mode='HTML')

    def select_price(m, f):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Далее ➡']])
        bot.send_chat_action(m.chat.id, action="typing")
        if f:
            txt = 'Введите минимальную цену аренды руб./мес. или нажмите <b>Далее</b>\n<i>(пример: 35000)</i>'
        else:
            txt = 'Введите максимальную цену аренды руб./мес. или нажмите <b>Далее</b>\n<i>(пример: 120000)</i>'
        bot.send_message(m.chat.id, txt, reply_markup=keyboard, parse_mode='HTML')

    def show_menu_first(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Показать результат ⬆']])
        bot.send_chat_action(m.chat.id, action='typing')
        bot.send_message(m.chat.id, 'Сейчас я подготовлю для вас подходящий список недвижимости', reply_markup=keyboard)

    def show_menu(m, rcount):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Ещё ▶']])
        bot.send_chat_action(m.chat.id, action='typing')
        text = "По вашему запросу найдено: <b>" + str(rcount) + " вариантов</b>\n\n" \
                                                             "<i>Для выбора квартиры, ответье на нужное сообщение с <b>любым</b> текстом</i>"
        bot.send_message(m.chat.id, text, reply_markup=keyboard, parse_mode='HTML')

    def send_photo(m, media, choice, flag):
        bot.send_chat_action(m.chat.id, action="upload_photo")
        bot.send_media_group(m.chat.id, media=media)

    def norows(m):
        bot.send_message(m.chat.id, '<b>Попробуйте изменить фильтр</b>', parse_mode='HTML')
        Keyboard.select_room(m)


class InlineKeyboard:
    def box(m):
        key = types.InlineKeyboardMarkup()
        rieltor = types.InlineKeyboardButton(
            text='Риелтор',
            url='t.me/medianadmin'
        )
        tg = types.InlineKeyboardButton(
            text='Техподдержка',
            url='t.me/royalgoose'
        )
        key.add(rieltor, tg)
        bot.send_chat_action(m.chat.id, action='typing')
        bot.send_message(m.chat.id, '📞 Наши контакты:', reply_markup=key)
