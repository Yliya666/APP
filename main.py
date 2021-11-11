import telebot
from telebot import types
import COVID19Py

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot('2050964866:AAHXDCAu3YK-rdyYvo4auZ71BUGUr3Ski3w')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Во всём мире')
    btn2 = types.KeyboardButton('Украина')
    btn3 = types.KeyboardButton('Россия')
    btn4 = types.KeyboardButton('Беларусь')
    markup.add(btn1, btn2, btn3, btn4)
    msg = bot.send_message(message.chat.id, 'Сделайте свой выбор', reply_markup=markup)
    bot.register_next_step_handler(msg, mess)


@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    get_message_bot = message.text.strip().lower()
    if get_message_bot == 'украина':
        location = covid19.getLocationByCountryCode("UA")
    elif get_message_bot == 'россия':
        location = covid19.getLocationByCountryCode("RU")
    elif get_message_bot == 'беларусь':
        location = covid19.getLocationByCountryCode("BY")
    else:
        location = covid19.getLatest()
        final_message = f"<u>Данные по всему миру:</u>\n<b>Заболевших: </b>{location['confirmed']:,}\n<b>Сметрей: </b>{location['deaths']:,}"

    if final_message == "":
        date = location[0]['last_updated'].split("T")
        time = date[1].split(".")
        final_message = f"Данные по стране: \nНаселение: {location[0]['country_population']:,}\n" \
                        f"Последнее обновление: {date[0]} {time[0]}\nПоследние данные:\n" \
                        f"Заболевших: {location[0]['latest']['confirmed']:,}\nСметрей: " \
                        f"{location[0]['latest']['deaths']:,}"
    bot.send_message(message.chat.id, final_message)




bot.polling()