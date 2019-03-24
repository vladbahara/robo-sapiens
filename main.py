# -*- coding: utf-8 -*-
import logging
import time

import telebot
from telebot import types

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot('707234632:AAEKTM5uVzYPwSp-62RtMj2Enu_DXDf6TN4')  # токен бота
money = 0.65

uid = 0
messageOp = ''

@bot.message_handler(commands=['start'])
def start(message):
    global uid
    uid = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🏬 Владелец', '🚶‍ Пользователь')
    msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
    bot.register_next_step_handler(msg, manage)


def manage(message):
    try:
        mess = message.text

        if(mess == u'🏬 Владелец'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
            markup.row('📬 Рассказать друзьям')
            markup.row('Разместить бота, канал')
            markup.row('Мой счёт')
            markup.row('Статистика продвижения')
            markup.row('🏬 Изменить аккаунт')
            msg = bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(msg, owner_menu)

        elif (mess == u'🚶‍ Пользователь'):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
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


def owner_menu(message):  # Владелец

    try:
        mess = message.text

        if(mess == u'📬 Рассказать друзьям'):
            markup = types.InlineKeyboardMarkup()
            forward_btn = types.InlineKeyboardButton(text='📱 Отправить', url='https://t.me/share/url?url=https://t.me/RS_Media_Bot&text= FWFdfwsdf *dasdas*')
            markup.add(forward_btn)
            msg = bot.send_message(message.chat.id, f'Я бот который поможет рассказать о твоём боте или канале тем пользователям, которых это может заинтересовать. Рассылка делается на основании интересов которые заполнили пользователи, так что они будут получать только качественный и интересный контент.<a href="https://imbt.ga/2bLbzibnr0">&#160;</a>', reply_markup=markup, parse_mode='HTML')
            bot.register_next_step_handler(msg, owner_menu)

        elif (mess == u'Разместить бота, канал'):
            global messageOp
            messageOp = message.message_id
            markup = types.InlineKeyboardMarkup()
            add_bot = types.InlineKeyboardButton(text='Разместить бота', callback_data='add_bot_command')
            add_channel = types.InlineKeyboardButton(text='Разместить канал', callback_data='add_channel_command')
            markup.row(add_bot)
            markup.row(add_channel)
            msg = bot.send_message(message.chat.id, '<b>Разместить бота, канал!</b>\nВыбери, что именно ты хочешь разместить. Бота или канал?<a href="https://imbt.ga/nwmnR4wpIZ">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(msg, owner_menu)

        elif (mess == u'Мой счёт'):
            markup = types.InlineKeyboardMarkup()
            add_money = types.InlineKeyboardButton(text='💰 Пополнить счёт', callback_data='add_money')
            markup.add(add_money)

            if money < 1.0:
                msg = bot.send_message(message.chat.id, f'<b>Мой счёт!</b>\nЧтобы продвигать бота, на счету должно быть не менее 1$.<a href="https://imbt.ga/UlmN4K1cot">&#160;</a>\n💰  <b>{money} $</b>', parse_mode='HTML', reply_markup=markup)
                bot.register_next_step_handler(msg, owner_menu)
            else:
                msg = bot.send_message(message.chat.id, f'<b>Мой счёт!</b>\nКаждый целевой переход в бота или канал стоит 2 цента.<a href="https://imbt.ga/UlmN4K1cot">&#160;</a>\n💰  <b>{money} $</b>', parse_mode='HTML', reply_markup=markup)
                bot.register_next_step_handler(msg, owner_menu)

        elif (mess == u'Статистика продвижения'):
            markup = types.InlineKeyboardMarkup()
            stat_channel_1 = types.InlineKeyboardButton(text='@some_channel', callback_data='channel_stat')
            stat_bot_1 = types.InlineKeyboardButton(text='@some_bot', callback_data='bot_stat')
            markup.row(stat_channel_1)
            markup.row(stat_bot_1)
            msg = bot.send_message(message.chat.id, '<b>Статистика продвижения!</b>\nЗдесь будет отображаться статистика продвижения твоих ботов или каналов.<a href="https://imbt.ga/9z884zDX1w">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(msg, owner_menu)

        elif (mess == u'🏬 Изменить аккаунт'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            markup.add('🏬 Владелец', '🚶‍ Пользователь')
            msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(msg, manage)

        elif (mess == u'/start'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            markup.add('🏬 Владелец', '🚶‍ Пользователь')
            msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(msg, manage)
        else:
            raise Exception()

    except Exception as e:
        msg = bot.send_message(message.chat.id, 'Ошибочка(')
        bot.register_next_step_handler(msg, owner_menu)


def user_menu(message):  # Пользователь
    try:
        mess = message.text

        if(mess == u'📬 Рассказать друзьям'):
            markup = types.InlineKeyboardMarkup()
            share_btn = types.InlineKeyboardButton(text='📱 Отправить', url='https://t.me/share/url?url=https://t.me/RS_Media_Bot')
            markup.add(share_btn)
            msg = bot.send_message(message.chat.id, 'Я бот который на основе твоих интересов будет делать индивидуальную рассылку ботов и каналов. Также ты можешь искать нужный контент самостоятельно.<a href="https://imbt.ga/2bLbzibnr0">&#160;</a>', reply_markup=markup, parse_mode='HTML')
            bot.register_next_step_handler(msg, user_menu)

        elif (mess == u'Поиск'):
            markup = types.InlineKeyboardMarkup()
            search_bots = types.InlineKeyboardButton(text='Боты', callback_data='search_bots')
            search_channel = types.InlineKeyboardButton(text='Каналы', callback_data='search_channels')
            change_pref = types.InlineKeyboardButton(text='⚙️ Изменить интересы', callback_data='change_prefs')
            markup.row(search_bots)
            markup.row(search_channel)
            markup.row(change_pref)
            msg = bot.send_message(message.chat.id, '<b>Поиск!</b>\nНиже выбери что именно ты хочешь найти. Я ищу боты и каналы по твоим интересам которые ты выбрал. Чтобы изменить результаты поиска, измени свои интересы.<a href="https://imbt.ga/9z884zDX1w">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(msg, user_menu)

        elif (mess == u'Изменить интересы'):
            markup = types.InlineKeyboardMarkup()
            change_category = types.InlineKeyboardButton(text='1. Категории', callback_data='change_category')
            change_country = types.InlineKeyboardButton(text='2. Страна', callback_data='change_country')
            change_content = types.InlineKeyboardButton(text='3. Контент', callback_data='change_content')
            change_freq = types.InlineKeyboardButton(text='4. Частота рассылки', callback_data='change_freq')
            markup.row(change_category)
            markup.row(change_country)
            markup.row(change_content)
            markup.row(change_freq)
            msg = bot.send_message(message.chat.id, '<b>Изменить интересы!</b>\nВыбирай какие именно интересы ты хочешь изменить.<a href="https://telegra.ph/file/8c2abab1d2ecfc76677d2.jpg">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(msg, user_menu)

        elif (mess == u'Частота рассылки'):
            markup = types.InlineKeyboardMarkup()
            one_per_day = types.InlineKeyboardButton(text='🕟 Раз в день', callback_data='one_per_day')
            two_per_day = types.InlineKeyboardButton(text='🕘 Два в день', callback_data='two_per_day')
            one_per_two_days = types.InlineKeyboardButton(text='🕜 Раз в 2 дня', callback_data='one_per_two_days')
            one_per_three_days = types.InlineKeyboardButton(text='🕥 Раз в 3 дня', callback_data='one_per_three_days')
            markup.row(one_per_day)
            markup.row(two_per_day)
            markup.row(one_per_two_days)
            markup.row(one_per_three_days)
            msg = bot.send_message(message.chat.id, '<b>Частота рассылки!</b>\nКак часто ты хочешь получить россылку каналов и ботов подобранных индивидуально для тебя?<a href="https://imbt.ga/UuCEyp73zo">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(msg, user_menu)

        elif (mess == u'🏬 Изменить аккаунт'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add('🏬 Владелец', '🚶‍ Пользователь')
            msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(msg, manage)

        elif (mess == u'/start'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add('🏬 Владелец', '🚶‍ Пользователь')
            msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(msg, manage)
        else:
            raise Exception()

    except Exception as e:
        msg = bot.send_message(message.chat.id, 'Ошибочка(')
        bot.register_next_step_handler(msg, user_menu)


def addBot(message):
    try:
        pass
    except Exception as e:
        msg = bot.send_message(message.chat.id, 'Ошибочка(')
        bot.register_next_step_handler(msg, owner_menu)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    command = call.data
    try:
        if(command == 'add_bot_command'):
            markup = types.InlineKeyboardMarkup()
            cat_1 = types.InlineKeyboardButton(text='1.', callback_data='saa')
            markup.row(cat_1)
            bot.edit_message_text(uid, messageOp, text="<b>Категории!</b>Выбери одну категорию, которой соответствует твой контент. Это позволит показывать твой контент только заинтересованным пользователям.<a href='https://imbt.ga/dZNsjMG61z'>&#160;</a>", reply_markup=markup, parse_mode='HTML')

        elif(command == 'add_channel_command'):
            bot.send_message(uid, 'Add Channel')

        elif(command == 'add_money'):
            bot.send_message(uid, 'Add Money')

        elif(command == 'channel_stat'):
            bot.send_message(uid, 'Channel Stat')

        elif(command == 'bot_stat'):
            bot.send_message(uid, 'Bot Stat')

        elif(command == 'search_bots'):
            bot.send_message(uid, 'Search Bots')

        elif(command == 'search_channels'):
            bot.send_message(uid, 'Search Channels')

        elif(command == 'change_prefs'):
            bot.send_message(uid, 'Change Prefs')

        elif(command == 'change_category'):
            bot.send_message(uid, 'Change Category')

        elif(command == 'change_country'):
            bot.send_message(uid, 'Change Country')

        elif(command == 'change_content'):
            bot.send_message(uid, 'Change Content')

        elif(command == 'change_freq'):
            bot.send_message(uid, 'Change Freq')

        elif(command == 'one_per_day'):
            bot.send_message(uid, 'one_per_day')

        elif(command == 'two_per_day'):
            bot.send_message(uid, 'two_per_day')

        elif(command == 'one_per_two_days'):
            bot.send_message(uid, 'one_per_two_days')

        elif(command == 'one_per_three_days'):
            bot.send_message(uid, 'one_per_three_days')
            
    except Exception as e:
        bot.send_message(uid, 'nope(')
    

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)
