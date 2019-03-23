# -*- coding: utf-8 -*-
import telebot, time
from telebot import types
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) 

bot = telebot.TeleBot('881932071:AAF7FhtTi-3Al9Ef53Mt7961JfFGNfTHQ8Y')#токен бота
photo = open('img/share.jpg', 'rb')

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
            msg = bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(msg, owner_menu)
        elif (mess == u'🚶‍ Пользователь'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row('📬 Рассказать друзьям')
            markup.row('Поиск')
            markup.row('Изменить интересы')
            markup.row('Частота рассылки')
            markup.row('🏬 Изменить аккаунт')
            msg = bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(msg, user_menu)
        else:
            raise Exception()

    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибочка(')

def owner_menu(message):
    
    try:
        mess = message.text
        if(mess == u'📬 Рассказать друзьям'):
            msg = bot.send_message(message.chat.id, f'Я бот который поможет рассказать о твоём боте или канале тем пользователям, которых это может заинтересовать. Рассылка делается на основании интересов которые заполнили пользователи, так что они будут получать только качественный и интересный контент[.]({photo})', parse_mode='Markdown')
            bot.register_next_step_handler(msg, owner_menu)
           
        elif (mess == u'Разместить бота, канал'):
            
            msg = bot.send_message(message.chat.id, '*Разместить бота, канал!*\nВыбери, что именно ты хочешь разместить. Бота или канал?', parse_mode='Markdown')
            bot.register_next_step_handler(msg, owner_menu)
        elif (mess == u'Мой счёт'):
            
            msg = bot.send_message(message.chat.id, '*Мой счёт!*\nЧтобы продвигать бота, на счету должно быть не менее 1$.\n💰  *0, 15 $*', parse_mode='Markdown') # f'{money}'
            bot.register_next_step_handler(msg, owner_menu)
        elif (mess == u'Статистика продвижения'):
            
            msg = bot.send_message(message.chat.id, '*Статистика продвижения!*\nЗдесь будет отображаться статистика продвижения твоих ботов или каналов.', parse_mode='Markdown')
            bot.register_next_step_handler(msg, owner_menu)
        elif (mess == u'🏬 Изменить аккаунт'):
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('🏬 Владелец' , '🚶‍ Пользователь')
            msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(msg, manage)
        elif (mess == u'/start'):
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('🏬 Владелец' , '🚶‍ Пользователь')
            msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(msg, manage)
        else:
            raise Exception()

    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибочка(')
        bot.register_next_step_handler(msg, owner_menu)

def user_menu(message):
    try:
        mess = message.text
        if(mess == u'📬 Рассказать друзьям'):
           
            msg = bot.send_message(message.chat.id, 'Я бот который на основе твоих интересов будет делать индивидуальную рассылку ботов и каналов. Также ты можешь искать нужный контент самостоятельно.', parse_mode='Markdown')
            bot.register_next_step_handler(msg, user_menu)
        elif (mess == u'Поиск'):
            
            msg = bot.send_message(message.chat.id, '*Поиск!*\nНиже выбери что именно ты хочешь найти. Я ищу боты и каналы по твоим интересам которые ты выбрал. Чтобы изменить результаты поиска, измени свои интересы.' , parse_mode='Markdown')
            bot.register_next_step_handler(msg, user_menu)
        elif (mess == u'Изменить интересы'):
            
            msg = bot.send_message(message.chat.id, '*Изменить интересы!*\nВыбирай какие именно интересы ты хочешь изменить.', parse_mode='Markdown')
            bot.register_next_step_handler(msg, user_menu)
        elif (mess == u'Частота рассылки'):
            
            msg = bot.send_message(message.chat.id, '*Частота рассылки!*\nКак часто ты хочешь получить россылку каналов и ботов подобранных индивидуально для тебя?', parse_mode='Markdown')
            bot.register_next_step_handler(msg, user_menu)
        elif (mess == u'🏬 Изменить аккаунт'):
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('🏬 Владелец' , '🚶‍ Пользователь')
            msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(msg, manage)
        elif (mess == u'/start'):
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('🏬 Владелец' , '🚶‍ Пользователь')
            msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(msg, manage)
        else:
            raise Exception()

    except Exception as e:
        msg = bot.send_message(message.chat.id, 'Ошибочка(')
        bot.register_next_step_handler(msg, user_menu)



if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)

