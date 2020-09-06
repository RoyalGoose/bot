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
        # keyboard.add(*[types.KeyboardButton(name) for name in ['Найти недвижимость 🔎', 'Задать вопрос ❓']])
        # keyboard.add(*[types.KeyboardButton(name) for name in ['О нас 📝', 'Контакты 📞']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Найти недвижимость 🔎']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Контакты 📞']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Выберите необходимый пункт меню', reply_markup=keyboard)

    def select_dist(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['СЗАО ↖', 'САО ⬆', '↗ СВАО']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['ЗАО ⬅', 'ЦАО ⏺', '➡ ВАО']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['ЮЗАО ↙', 'ЮАО ⬇', '↘ ЮВАО']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['НАО (Новомосковский)', 'Любой 🔀']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Вернутся в меню ↩']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Выберите административный округ', reply_markup=keyboard)

    def select_price(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['<30 тыс. руб', '30-50 тыс. руб']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['50-100 тыс. руб', '>100 тыс. руб']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Любая цена 💰']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Вернутся в меню ↩']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Желаемая цена аренды в месяц', reply_markup=keyboard)

    def select_room(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['1 комната', '2 комнаты']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['3 комнаты', '4 и более']])
        # keyboard.add(*[types.KeyboardButton(name) for name in ['Любое количество комнат 🏢']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Вернутся в меню ↩']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Какое количество комнат', reply_markup=keyboard)

    def select_square(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Менее 50 м²', '50-100 м²']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['100-200 м²', 'Более 200 м²']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Любая площадь 🌍']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Вернутся в меню ↩']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Желаемая площадь', reply_markup=keyboard)

    def show_menu_first(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Показать результат ⬆']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Вернутся в меню ↩']])
        bot.send_chat_action(m.chat.id, action='typing')
        bot.send_message(m.chat.id, 'Сейчас я подготовлю для вас подходящий список недвижимости', reply_markup=keyboard)

    def show_menu(m, rcount):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Показать результат ⤴']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['◀ Предыдущая', 'Выбрать ✅', 'Следующая ▶']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Вернутся в меню ↩']])
        bot.send_chat_action(m.chat.id, action='typing')
        text = "По вашему запросу найдено: " + str(rcount) + " вариантов"
        bot.send_message(m.chat.id, text, reply_markup=keyboard)

    def send_photo(m, media, choice, flag):
        # if choice == 0:
        #     bot.send_chat_action(m.chat.id, action='typing')
        #     bot.send_message(m.chat.id, 'По вашему запросу найдено:')
        bot.send_chat_action(m.chat.id, action="upload_photo")
        bot.send_media_group(m.chat.id, media=media)

    def norows(m):
        bot.send_message(m.chat.id, 'Попробуйте изменить фильтр')
        Keyboard.select_room(m)


class InlineKeyboard:
    def box(m):
        key = types.InlineKeyboardMarkup()
        rieltor = types.InlineKeyboardButton(
            text='Риелтор',
            url='t.me/Azbuka19'
        )
        tg = types.InlineKeyboardButton(
            text='Техподдержка',
            url='t.me/royalgoose'
        )
        key.add(rieltor, tg)
        bot.send_chat_action(m.chat.id, action='typing')
        bot.send_message(m.chat.id, '📞 Наши контакты:', reply_markup=key)
