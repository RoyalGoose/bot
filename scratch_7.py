import telebot
import requests
from bs4 import BeautifulSoup
import time
bot = telebot.TeleBot('1170743793:AAF3xFYt54gkJ3rlY_Xr0ZSnleTrzjCmOx8')
times = []
def get_info():
    txid_info = []

    response = requests.get('https://www.blockchain.com/btc/tx/418184684622d23804edc38a771af814a66530195617ca462467d04efffea5f0')

    soup = BeautifulSoup(response.content)
    status = soup.find("span", {"class": "sc-1ryi78w-0 gCzMgE sc-16b9dsl-1 kUAhZx sc-45ldg2-0 khjuXC"})
    date_time = soup.find("div", {"class": "kad8ah-0 kKDjc"})
    comission = soup.find("div", {"class": "kad8ah-1 giMhWw"})
    #ammount = soup.find("div", {"class": "kad8ah-0 gsjnEH"})
    block = soup.find_all("a", {"class": "sc-1r996ns-0 gzrtQD sc-1tbyx6t-1 kXxRxe iklhnl-0 kVizQZ"})
    txid_info.append(status.text + '\n'+ date_time.text + '\n' + comission.text + '\n'  + block[4].text)


    return(txid_info)


@bot.message_handler(commands=['text'])
def start_message(message):
    bot.send_message(message.chat.id, 'Started')



@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Привет':
        start = time.time()
        bot.send_message(message.chat.id, get_info())
        stop = time.time()
        result = (stop - start)
        result = str(result)
        bot.send_message(message.chat.id, result)
        start = time.time()
        bot.send_message(message.chat.id, get_info())
        stop = time.time()
        result = (stop - start)
        result = str(result)
        bot.send_message(message.chat.id, result)
        start = time.time()
        bot.send_message(message.chat.id, get_info())
        stop = time.time()
        result = (stop - start)
        result = str(result)
        bot.send_message(message.chat.id, result)

    elif message.text == 'Пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')

bot.polling(none_stop=True)
