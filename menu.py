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
        keyboard.add(*[types.KeyboardButton(name) for name in ['Контакты 📞', 'Задать вопрос ❓']])
        # keyboard.add(*[types.KeyboardButton(name) for name in ['Скачать']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Выберите необходимый пункт меню', reply_markup=keyboard)

    def select_room(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Студия', '1 комната']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['2 комнаты', '3 комнаты']])
        # keyboard.add(*[types.KeyboardButton(name) for name in ['Любое количество комнат 🏢']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['4 и более', 'Далее ➡']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Выберите количество комнат и нажмите "Далее" (один или несколько вариантов)',
                         reply_markup=keyboard)

    def select_dist(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Внутри кольцевой', 'До 3 станций от кольца']])
        # keyboard.add(*[types.KeyboardButton(name) for name in []])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Внутри ТТК', 'До 5 станций от кольца']])
        # keyboard.add(*[types.KeyboardButton(name) for name in []])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Любая станция']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Выберите максимальное расстояние от центра', reply_markup=keyboard)

    def select_reg(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['СЗАО ↖', 'САО ⬆', '↗ СВАО']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['ЗАО ⬅', 'ЦАО ⏺', '➡ ВАО']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['ЮЗАО ↙', 'ЮАО ⬇', '↘ ЮВАО']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['НАО (Новомосковский)', 'Далее ➡']])  # 'Любой 🔀'
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩']])
        bot.send_chat_action(m.chat.id, action="typing")
        bot.send_message(m.chat.id, 'Выберите административный округ (один или несколько вариантов)',
                         reply_markup=keyboard)

    def select_square(m, f):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # keyboard.add(*[types.KeyboardButton(name) for name in ['Менее 50 м²', '50-100 м²']])
        # keyboard.add(*[types.KeyboardButton(name) for name in ['100-200 м²', 'Более 200 м²']])
        # keyboard.add(*[types.KeyboardButton(name) for name in ['Любая площадь 🌍']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Далее ➡']])
        bot.send_chat_action(m.chat.id, action="typing")
        if f:
            txt = 'Введите минимальную желаемую площадь в м², пример: 54'
        else:
            txt = 'Введите максимальную желаемую площадь в м², пример: 150'
        bot.send_message(m.chat.id, txt, reply_markup=keyboard)

    def select_price(m, f):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # keyboard.add(*[types.KeyboardButton(name) for name in ['<30 тыс. руб', '30-50 тыс. руб']])
        # keyboard.add(*[types.KeyboardButton(name) for name in ['50-100 тыс. руб', '>100 тыс. руб']])
        # keyboard.add(*[types.KeyboardButton(name) for name in ['Любая цена 💰']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Далее ➡']])
        bot.send_chat_action(m.chat.id, action="typing")
        if f:
            txt = 'Введите минимальную цену аренды руб./мес., пример 35000'
        else:
            txt = 'Введите максимальную цену аренды руб./мес., пример 120000'
        bot.send_message(m.chat.id, txt, reply_markup=keyboard)

    def show_menu_first(m):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #keyboard.add(*[types.KeyboardButton(name) for name in []])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Показать результат ⬆']])
        bot.send_chat_action(m.chat.id, action='typing')
        bot.send_message(m.chat.id, 'Сейчас я подготовлю для вас подходящий список недвижимости', reply_markup=keyboard)

    def show_menu(m, rcount):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # keyboard.add(*[types.KeyboardButton(name) for name in ['Показать результат ⤴']])
        # keyboard.add(*[types.KeyboardButton(name) for name in ['◀ Предыдущая', 'Выбрать ✅', 'Следующая ▶']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Новый поиск ↩', 'Следующая ▶']])
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
