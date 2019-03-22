import telebot
import time
from telebot import types

bot = telebot.TeleBot('868691804:AAG2PfX33L7Y-OPvuCclxeFKgIoqghwadnk')#токен бота

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    owner = markup.add('Владелец')
    user = markup.add('Пользователь')
    markup.row(owner,)
    markup.row(user,)
    msg = bot.send_message(message, 'Выбирай!', reply_markup=markup)
    bot.register_next_step_handler(msg, process_name_step)
    






if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)