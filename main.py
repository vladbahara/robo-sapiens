# -*- coding: utf-8 -*-
import telebot, time
from telebot import types
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) 

bot = telebot.TeleBot('881932071:AAF7FhtTi-3Al9Ef53Mt7961JfFGNfTHQ8Y')#токен бота

@bot.message_handler(commands=['start'])
def start(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🏬 Владелец' , '🚶‍ Пользователь')
    msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
    bot.register_next_step_handler(msg, manage)

def manage(message):
    try:
        mess = message.text
        if(mess == u'🏬 Владелец'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row('📬 Рассказать друзьям')
            markup.row('Разместить бота, канал')
            markup.row('Мой счёт')
            markup.row('Статистика продвижения')
            markup.row('🏬 Изменить аккаунт')
            msg = bot.send_message(message.chat.id, 'test', reply_markup=markup)
            bot.register_next_step_handler(msg, owner_menu)
            bot.send_message(message.chat.id, 'Работает! 1')
        elif (mess == u'🚶‍ Пользователь'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row('📬 Рассказать друзьям')
            markup.row('Поиск')
            markup.row('Изменить интересы')
            markup.row('Частота рассылки')
            markup.row('🏬 Изменить аккаунт')
            msg = bot.send_message(message.chat.id, 'test', reply_markup=markup)
            bot.register_next_step_handler(msg, user_menu)
            bot.send_message(message.chat.id, 'Работает! 2')
        else:
            raise Exception()

    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибочка(')

def owner_menu(message):
    try:
        mess = message.text
        if(mess == u'📬 Рассказать друзьям'):

            msg = bot.send_message(message.chat.id, 'Я бот который поможет рассказать о твоём боте или канале тем пользователям, которых это может заинтересовать. Рассылка делается на основании интересов которые заполнили пользователи, так что они будут получать только качественный и интересный контент.', reply_markup=keyboard)
            #bot.register_next_step_handler(msg, owner_menu)
           
        elif (mess == u'Поиск'):
            
            msg = bot.send_message(message.chat.id, 'test')
            #bot.register_next_step_handler(msg, user_menu)
        elif (mess == u'Изменить интересы'):
            
            msg = bot.send_message(message.chat.id, 'test')
            #bot.register_next_step_handler(msg, user_menu)
        elif (mess == u'Частота рассылки'):
            
            msg = bot.send_message(message.chat.id, 'test')
            #bot.register_next_step_handler(msg, user_menu)
        elif (mess == u'🏬 Изменить аккаунт'):
            
            msg = bot.send_message(message.chat.id, 'test')
            #bot.register_next_step_handler(msg, user_menu)
        else:
            raise Exception()

    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибочка(')

def user_menu(message):
    try:
        mess = message.text
        if(mess == u'🏬 Владелец'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row('📬 Рассказать друзьям')
            markup.row('Разместить бота, канал')
            markup.row('Мой счёт')
            markup.row('Статистика продвижения')
            markup.row('🏬 Изменить аккаунт')
            msg = bot.send_message(message.chat.id, 'test', reply_markup=markup)
            #bot.register_next_step_handler(msg, owner_menu)
            bot.send_message(message.chat.id, 'Работает! 1')
        elif (mess == u'🚶‍ Пользователь'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.row('📬 Рассказать друзьям')
            markup.row('Поиск')
            markup.row('Изменить интересы')
            markup.row('Частота рассылки')
            markup.row('🏬 Изменить аккаунт')
            msg = bot.send_message(message.chat.id, 'test', reply_markup=markup)
            #bot.register_next_step_handler(msg, user_menu)
            bot.send_message(message.chat.id, 'Работает! 2')
        else:
            raise Exception()

    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибочка(')



if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)

