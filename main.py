import telebot, time
from telebot import types

bot = telebot.TeleBot('881932071:AAF7FhtTi-3Al9Ef53Mt7961JfFGNfTHQ8Y')#токен бота

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Владелец', 'Пользователь')
    msg = bot.send_message(message.chat.id, 'Выбирай!', reply_markup=markup)
    






if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)