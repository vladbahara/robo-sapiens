# -*- coding: utf-8 -*-
import logging
import sqlite3
import time
import re
import telebot
import random
from telebot import types
from config import token

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(token)




c1 = types.InlineKeyboardButton(text='1. Новости и СМИ', callback_data='news')
c2 = types.InlineKeyboardButton(text='2. Криптовалюты', callback_data='crypto')
c3 = types.InlineKeyboardButton(text='3. Для взрослых', callback_data='adult')
c4 = types.InlineKeyboardButton(text='4. Образование', callback_data='education')
c5 = types.InlineKeyboardButton(text='5. Искусство и фото', callback_data='art')
c6 = types.InlineKeyboardButton(text='6. Здоровье и Спорт', callback_data='health')
c7 = types.InlineKeyboardButton(text='7. Технологии', callback_data='tech')
c8 = types.InlineKeyboardButton(text='8. Путешествия', callback_data='travel')
c9 = types.InlineKeyboardButton(text='9. Продажи', callback_data='sales')
c10 = types.InlineKeyboardButton(text='10. Политика', callback_data='policy')
c11 = types.InlineKeyboardButton(text='11. Видео и фильмы', callback_data='video')
c12 = types.InlineKeyboardButton(text='12. Мода и красота', callback_data='style')
c13 = types.InlineKeyboardButton(text='13. Психология', callback_data='psychology')
c14 = types.InlineKeyboardButton(text='14. Игры и приложения', callback_data='games')
c15 = types.InlineKeyboardButton(text='15. Книги', callback_data='books')
c16 = types.InlineKeyboardButton(text='16. Маркетинг, PR, реклама', callback_data='marketing')
c17 = types.InlineKeyboardButton(text='17. Цитаты', callback_data='quotes')
c18 = types.InlineKeyboardButton(text='18. Еда и кулинария', callback_data='food')
c19 = types.InlineKeyboardButton(text='19. Авто', callback_data='auto')
c20 = types.InlineKeyboardButton(text='20. Экономика', callback_data='economy')
c21 = types.InlineKeyboardButton(text='21. Telegram', callback_data='telegram')
c22 = types.InlineKeyboardButton(text='22. Лингвистика', callback_data='lingvist')
c23 = types.InlineKeyboardButton(text='23. Дизайн', callback_data='design')
c24 = types.InlineKeyboardButton(text='24. Карьера', callback_data='career')
c25 = types.InlineKeyboardButton(text='25. Семья и дети', callback_data='family')
c26 = types.InlineKeyboardButton(text='26. Медицина', callback_data='medicine')
c27 = types.InlineKeyboardButton(text='27. Рукоделие', callback_data='handmade')
c28 = types.InlineKeyboardButton(text='28. Животные', callback_data='animals')
c29 = types.InlineKeyboardButton(text='29. Лайфхаки', callback_data='lifehacks')






@bot.message_handler(commands=[''])
def empty_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/start')
    bot.send_message(message.chat.id, 'Нажимай старт!', reply_markup=markup)
    bot.register_next_step_handler(message, start)


@bot.message_handler(commands=['start'])
def start(message):
    user = (message.from_user.id, message.from_user.username, message.from_user.first_name)
    conn = sqlite3.connect('robo_users')
    cursor = conn.cursor()
    cursor.execute(f'SELECT ID FROM users WHERE ID = {user[0]}')
    response = cursor.fetchall()

    if response == []:
        cursor.execute("INSERT INTO users (ID, UN, NAME, ACCOUNT, MONEY) VALUES (?, ?, ?, 'user', 0.0)", user)
        conn.commit()
        conn.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🏬 Владелец', '🚶‍ Пользователь')
        msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
        bot.register_next_step_handler(msg, manage)
        
        
    elif response != []:
        cursor.execute(f'SELECT ACCOUNT FROM users WHERE ID = {user[0]}')
        r = cursor.fetchall()
        if r[0][0] == 'owner':
            conn.close()
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
            markup.row('📬 Рассказать друзьям')
            markup.row('Разместить бота, канал')
            markup.row('Мой счёт')
            markup.row('Статистика продвижения')
            markup.row('🏬 Изменить аккаунт')
            bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(message, owner_menu)
            
        elif r[0][0] == 'user':
            conn.close()
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
            markup.row('📬 Рассказать друзьям')
            markup.row('Поиск')
            markup.row('Изменить интересы')
            markup.row('Частота рассылки')
            markup.row('🏬 Изменить аккаунт')
            bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(message, user_menu)

        else:
            conn.close()
            bot.send_message(message.chat.id, 'Россия хуле! 1')
        
    else:
        conn.close()
        bot.send_message(message.chat.id, 'Россия хуле! 2')


def manage(message):
    try:
        mess = message.text
        user = message.from_user.id
        conn = sqlite3.connect('robo_users')
        cursor = conn.cursor()

        if(mess == u'🏬 Владелец'):
            try:
                cursor.execute(f"UPDATE users SET ACCOUNT = 'owner' WHERE ID = {user}")
                conn.commit()
                conn.close()
            except sqlite3.DatabaseError as err:       
                print("Error: ", err)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
            markup.row('📬 Рассказать друзьям')
            markup.row('Разместить бота, канал')
            markup.row('Мой счёт')
            markup.row('Статистика продвижения')
            markup.row('🏬 Изменить аккаунт')
            bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(message, owner_menu)

        elif (mess == u'🚶‍ Пользователь'):
            try:
                cursor.execute(f"UPDATE users SET ACCOUNT = 'user' WHERE ID = {user}")
                conn.commit()
                conn.close()
            except sqlite3.DatabaseError as err:       
                print("\nError: ", err, '\n')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
            markup.row('📬 Рассказать друзьям')
            markup.row('Поиск')
            markup.row('Изменить интересы')
            markup.row('Частота рассылки')
            markup.row('🏬 Изменить аккаунт')
            bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(message, user_menu)
        elif (mess == '/start'):
            conn.close()
            bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(message, start)
        else:
            conn.close()
            raise Exception()
        
    except Exception as e:
        conn.close()
        bot.register_next_step_handler(message, start)


def owner_menu(message):  # Владелец
    conn = sqlite3.connect('robo_users')
    cursor = conn.cursor()
    try:
        mess = message.text

        if(mess == u'📬 Рассказать друзьям'):
            markup = types.InlineKeyboardMarkup()
            forward_btn = types.InlineKeyboardButton(text='📱 Отправить', url='https://t.me/share/url?url=https://t.me/RS_Media_Bot')
            markup.add(forward_btn)
            bot.send_message(message.chat.id, 'Я бот который поможет рассказать о твоём боте или канале тем пользователям, которых это может заинтересовать. Рассылка делается на основании интересов которые заполнили пользователи, так что они будут получать только качественный и интересный контент.<a href="https://imbt.ga/2bLbzibnr0">&#160;</a>', reply_markup=markup, parse_mode='HTML')
            bot.register_next_step_handler(message, owner_menu)

        elif (mess == u'Разместить бота, канал'):
            
            markup = types.InlineKeyboardMarkup()
            add_bot = types.InlineKeyboardButton(text='Разместить бота', callback_data='add_bot_command')
            add_channel = types.InlineKeyboardButton(text='Разместить канал', callback_data='add_channel_command')
            markup.row(add_bot)
            markup.row(add_channel)
            bot.send_message(message.chat.id, '<b>Разместить бота, канал!</b>\nВыбери, что именно ты хочешь разместить. Бота или канал?<a href="https://imbt.ga/nwmnR4wpIZ">&#160;</a>', parse_mode='HTML', reply_markup=markup)

        elif (mess == u'Мой счёт'):
            cursor.execute(f'SELECT MONEY FROM users WHERE ID = {message.from_user.id}')
            money = cursor.fetchall()
            markup = types.InlineKeyboardMarkup()
            add_money = types.InlineKeyboardButton(text='💰 Пополнить счёт', callback_data='add_money')
            markup.add(add_money)
            conn.close()
            if money[0][0] < 1.0:
                bot.send_message(message.chat.id, text=f'<b>Мой счёт!</b>\nЧтобы продвигать бота, на счету должно быть не менее 1$.<a href="https://imbt.ga/UlmN4K1cot">&#160;</a>\n💰  <b>{money[0][0]} $</b>', parse_mode='HTML', reply_markup=markup)
                bot.register_next_step_handler(message, owner_menu)
            else:
                bot.send_message(message.chat.id, text=f'<b>Мой счёт!</b>\nКаждый целевой переход в бота или канал стоит 2 цента.<a href="https://imbt.ga/UlmN4K1cot">&#160;</a>\n💰  <b>{money[0][0]} $</b>', parse_mode='HTML', reply_markup=markup)
                bot.register_next_step_handler(message, owner_menu)

        elif (mess == u'Статистика продвижения'):
            markup = types.InlineKeyboardMarkup()
            cursor.execute(f'SELECT * FROM BAC_DB WHERE ID_OF_OWNER = {user}')
            res = cursor.fetchall()
            conn.close()
            for i in range(len(res)):
                print(res[i][2])
                stat_channel_1 = types.InlineKeyboardButton(text='@some_channel', callback_data='statistic')
            markup.row(stat_channel_1)
            markup.row(stat_bot_1)
            bot.send_message(message.chat.id, '<b>Статистика продвижения!</b>\nЗдесь будет отображаться статистика продвижения твоих ботов или каналов.<a href="https://imbt.ga/9z884zDX1w">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(message, owner_menu)

        elif (mess == u'🏬 Изменить аккаунт'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            markup.add('🏬 Владелец', '🚶‍ Пользователь')
            bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(message, manage)

        elif (mess == u'/start'):
            bot.register_next_step_handler(message, start)
        else:
            conn.close()
            raise Exception()

    except Exception as e:
        bot.send_message(message.chat.id, 'Выберите один из пунктов!')
        bot.register_next_step_handler(message, owner_menu)


def user_menu(message):  # Пользователь
    try:
        mess = message.text

        if(mess == u'📬 Рассказать друзьям'):
            markup = types.InlineKeyboardMarkup()
            share_btn = types.InlineKeyboardButton(text='📱 Отправить', url='https://t.me/share/url?url=https://t.me/RS_Media_Bot&text= Это бот который на основе твоих интересов будет делать индивидуальную рассылку ботов и каналов. Также ты можешь искать нужный контент самостоятельно.')
            markup.add(share_btn)
            bot.send_message(message.chat.id, 'Я бот который на основе твоих интересов будет делать индивидуальную рассылку ботов и каналов. Также ты можешь искать нужный контент самостоятельно.<a href="https://imbt.ga/2bLbzibnr0">&#160;</a>', reply_markup=markup, parse_mode='HTML')
            bot.register_next_step_handler(message, user_menu)

        elif (mess == u'Поиск'):
            markup = types.InlineKeyboardMarkup()
            search_bots = types.InlineKeyboardButton(text='Боты', callback_data='search_bots')
            search_channel = types.InlineKeyboardButton(text='Каналы', callback_data='search_channels')
            change_pref = types.InlineKeyboardButton(text='⚙️ Изменить интересы', callback_data='change_prefs')
            markup.row(search_bots)
            markup.row(search_channel)
            markup.row(change_pref)
            bot.send_message(message.chat.id, '<b>Поиск!</b>\nНиже выбери что именно ты хочешь найти. Я ищу боты и каналы по твоим интересам которые ты выбрал. Чтобы изменить результаты поиска, измени свои интересы.<a href="https://imbt.ga/9z884zDX1w">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(message, user_menu)

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
            bot.send_message(message.chat.id, '<b>Изменить интересы!</b>\nВыбирай какие именно интересы ты хочешь изменить.<a href="https://telegra.ph/file/8c2abab1d2ecfc76677d2.jpg">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(message, user_menu)

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
            bot.send_message(message.chat.id, '<b>Частота рассылки!</b>\nКак часто ты хочешь получить россылку каналов и ботов подобранных индивидуально для тебя?<a href="https://imbt.ga/UuCEyp73zo">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(message, user_menu)

        elif (mess == u'🏬 Изменить аккаунт'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add('🏬 Владелец', '🚶‍ Пользователь')
            bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(message, manage)

        elif (mess == u'/start'):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add('🏬 Владелец', '🚶‍ Пользователь')
            bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть!', reply_markup=markup)
            bot.register_next_step_handler(message, manage)
        else:
            raise Exception()

    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибочка( 3')
        bot.register_next_step_handler(message, user_menu)




@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('robo_users')
    cursor = conn.cursor()
    command = call.data
    user = call.message.chat.id
    global c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26, c27, c28, c29
    try:
        if(command == 'add_bot_command'):
            
            markup = types.InlineKeyboardMarkup()
            '''
            def ca():
                try:
                    for item in arr:
                        yield item
                except:
                    print('\nerr 1 \n')
            f = ca()
            def ce():
                for i in arr:
                    try:
                       ...
                    except StopIteration:
                        pass
            '''
            
            

            markup.row(c1)
            markup.row(c2)
            markup.row(c3)
            markup.row(c4)
            markup.row(c5)
            markup.row(c6)
            markup.row(c7)
            markup.row(c8)
            markup.row(c9)
            markup.row(c10)
            markup.row(c11)
            markup.row(c12)
            markup.row(c13)
            markup.row(c14)
            markup.row(c15)
            markup.row(c16)
            markup.row(c17)
            markup.row(c18)
            markup.row(c19)
            markup.row(c20)
            markup.row(c21)
            markup.row(c22)
            markup.row(c23)
            markup.row(c24)
            markup.row(c25)
            markup.row(c26)
            markup.row(c27)
            markup.row(c28)
            markup.row(c29)
            
        
            
            bot.send_message(call.message.chat.id, reply_markup=markup, text="<b>Категории!</b>\nВыбери одну категорию, которой соответствует твой контент. Это позволит показывать твой контент только заинтересованным пользователям.<a href='https://imbt.ga/dZNsjMG61z'>&#160;</a>",  parse_mode='HTML')


            
                        
        

        elif(command == 'add_channel_command'):
            markup = types.InlineKeyboardMarkup()
            

            markup.row(c1)
            markup.row(c2)
            markup.row(c3)
            markup.row(c4)
            markup.row(c5)
            markup.row(c6)
            markup.row(c7)
            markup.row(c8)
            markup.row(c9)
            markup.row(c10)
            markup.row(c11)
            markup.row(c12)
            markup.row(c13)
            markup.row(c14)
            markup.row(c15)
            markup.row(c16)
            markup.row(c17)
            markup.row(c18)
            markup.row(c19)
            markup.row(c20)
            markup.row(c21)
            markup.row(c22)
            markup.row(c23)
            markup.row(c24)
            markup.row(c25)
            markup.row(c26)
            markup.row(c27)
            markup.row(c28)
            markup.row(c29)
           
            bot.send_message(call.message.chat.id, reply_markup=markup, text="<b>Категории!</b>\nВыбери одну категорию, которой соответствует твой контент. Это позволит показывать твой контент только заинтересованным пользователям.<a href='https://imbt.ga/dZNsjMG61z'>&#160;</a>",  parse_mode='HTML')
            

        elif(command == 'add_money'):
            cursor.execute(f"UPDATE users SET MONEY = (25.2) WHERE ID = {user}")
            conn.commit()
            conn.close()
            bot.send_message(call.message.chat.id, 'Add Some Demo Money')

        elif(command == 'channel_stat'):
            cursor.execute('SELECT ')
            bot.send_message(call.message.chat.id, '<b>Бот:</b> @ome33\nПереходов: 567 (2 цента за переход)\n💰 <b>11, 34$</b><a href="https://telegra.ph/file/954afb76178f388d7d4f6.jpg">&#160;</a>', parse_mode='HTML')
                    
        elif(command == 'bot_stat'):
            bot.send_message(call.message.chat.id, '<b>Канал:</b> @omfewfe3a3\nПереходов: 957 (2 цента за переход)\n💰 <b>19, 84$</b><a href="https://telegra.ph/file/8cde82c7e8f5f1c8ddf50.jpg">&#160;</a>', )

        elif(command == 'search_bots'):
            bot.send_message(call.message.chat.id, 'gbfgb')
            @bot.inline_handler(lambda query: query.query == 'search_bots')
            def query_text(inline_query):
                try:
                    r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
                    r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
                    bot.answer_inline_query(inline_query.id, [r, r2])
                except Exception as e:
                    print(e)

        elif(command == 'search_channels'):
            bot.send_message(call.message.chat.id, 'Search Channels')

        elif(command == 'change_prefs'):
            markup = types.InlineKeyboardMarkup()
            change_category = types.InlineKeyboardButton(text='1. Категории', callback_data='change_category')
            change_country = types.InlineKeyboardButton(text='2. Страна', callback_data='change_country')
            change_content = types.InlineKeyboardButton(text='3. Контент', callback_data='change_content')
            change_freq = types.InlineKeyboardButton(text='4. Частота рассылки', callback_data='change_freq')
            markup.row(change_category)
            markup.row(change_country)
            markup.row(change_content)
            markup.row(change_freq)
            bot.send_message(call.message.chat.id, '<b>Изменить интересы!</b>\nВыбирай какие именно интересы ты хочешь изменить.<a href="https://telegra.ph/file/8c2abab1d2ecfc76677d2.jpg">&#160;</a>', parse_mode='HTML', reply_markup=markup)

            @bot.callback_query_handler(func=lambda call: True)
            def callback(call):
                bot.send_message(call.message.chat.id, 'adasdasdasdasdasd')

        elif(command == 'change_category'):
            bot.send_message(call.message.chat.id, 'Change Category')

        elif(command == 'change_country'):
            bot.send_message(call.message.chat.id, 'Change Country')

        elif(command == 'change_content'):
            bot.send_message(call.message.chat.id, 'Change Content')

        elif(command == 'change_freq'):
            markup = types.InlineKeyboardMarkup()
            one_per_day = types.InlineKeyboardButton(text='🕟 Раз в день', callback_data='one_per_day')
            two_per_day = types.InlineKeyboardButton(text='🕘 Два в день', callback_data='two_per_day')
            one_per_two_days = types.InlineKeyboardButton(text='🕜 Раз в 2 дня', callback_data='one_per_two_days')
            one_per_three_days = types.InlineKeyboardButton(text='🕥 Раз в 3 дня', callback_data='one_per_three_days')
            markup.row(one_per_day)
            markup.row(two_per_day)
            markup.row(one_per_two_days)
            markup.row(one_per_three_days)
            bot.send_message(message.chat.id, '<b>Частота рассылки!</b>\nКак часто ты хочешь получить россылку каналов и ботов подобранных индивидуально для тебя?<a href="https://imbt.ga/UuCEyp73zo">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(message, user_menu)

        elif(command == 'one_per_day'):
            cursor.execute(f"UPDATE users SET FREQ = 'one_per_day' WHERE ID = {user}")
            conn.commit()
            conn.close()
            bot.send_message(call.message.chat.id, '🕟 <b>Раз в день</b>\nОтлично, теперь я буду присылать раз в день интересного бота, или канал. Рассылка зависит от выбранных вами интересов.<a href="https://telegra.ph/file/06d026ea7f832d1c3c757.jpg">&#160;</a>', parse_mode="HTML")

        elif(command == 'two_per_day'):
            cursor.execute(f"UPDATE users SET FREQ = 'two_per_day' WHERE ID = {user}")
            conn.commit()
            conn.close()
            bot.send_message(call.message.chat.id, '🕜 <b>Два в день</b>\nОтлично, теперь я буду присылать два раза в день интересного бота, или канал. Рассылка зависит от выбранных вами интересов.<a href="https://telegra.ph/file/06d026ea7f832d1c3c757.jpg">&#160;</a>', parse_mode="HTML")

        elif(command == 'one_per_two_days'):
            cursor.execute(f"UPDATE users SET FREQ = 'one_per_two_days' WHERE ID = {user}")
            conn.commit()
            conn.close()
            bot.send_message(call.message.chat.id, '🕘 <b>Раз в 2 дня</b>\nОтлично, теперь я буду присылать раз в 2 дня интересного бота, или канал. Рассылка зависит от выбранных вами интересов.<a href="https://telegra.ph/file/06d026ea7f832d1c3c757.jpg">&#160;</a>', parse_mode="HTML")

        elif(command == 'one_per_three_days'):
            cursor.execute(f"UPDATE users SET FREQ = 'one_per_three_days' WHERE ID = {user}")
            conn.commit()
            conn.close()
            bot.send_message(call.message.chat.id, '🕥 <b>Раз в 3 дня</b>\nОтлично, теперь я буду присылать раз в 3 дня интересного бота, или канал. Рассылка зависит от выбранных вами интересов.<a href="https://telegra.ph/file/06d026ea7f832d1c3c757.jpg">&#160;</a>', parse_mode="HTML")
        elif(command == 'saa'):
            markup = types.InlineKeyboardMarkup()
            c1 = types.InlineKeyboardButton(text='Россия', callback_data='bot_ru')
            c2 = types.InlineKeyboardButton(text='Украина', callback_data='bot_ua')
            c3 = types.InlineKeyboardButton(text='Белоруссия', callback_data='bot_by')
            c4 = types.InlineKeyboardButton(text='Казахстан', callback_data='bot_kz')
            c5 = types.InlineKeyboardButton(text='Узбекистан', callback_data='bot_uz')
            c6 = types.InlineKeyboardButton(text='Грузия', callback_data='bot_ge')
            c7 = types.InlineKeyboardButton(text='Молдавия', callback_data='bot_md')
            c8 = types.InlineKeyboardButton(text='Литва', callback_data='bot_lt')
            c9 = types.InlineKeyboardButton(text='Латвия', callback_data='bot_lv')
            c10 = types.InlineKeyboardButton(text='Эстония', callback_data='bot_ee')
            c11 = types.InlineKeyboardButton(text='Армения', callback_data='bot_am')
            c12 = types.InlineKeyboardButton(text='Таджикистан', callback_data='bot_tj')
            c13 = types.InlineKeyboardButton(text='Азербайджан', callback_data='bot_az')
            c14 = types.InlineKeyboardButton(text='Киргизия', callback_data='bot_kg')
            c15 = types.InlineKeyboardButton(text='Туркменистан', callback_data='bot_tm')
            c16 = types.InlineKeyboardButton(text='🗺️ Все страны', callback_data='bot_all')
            

            markup.row(c1)
            markup.row(c2)
            markup.row(c3)
            markup.row(c4)
            markup.row(c5)
            markup.row(c6)
            markup.row(c7)
            markup.row(c8)
            markup.row(c9)
            markup.row(c10)
            markup.row(c11)
            markup.row(c12)
            markup.row(c13)
            markup.row(c14)
            markup.row(c15)
            markup.row(c16)
            
           
            bot.send_message(call.message.chat.id, reply_markup=markup, parse_mode='HTML', text='<b>Страна!</b>\nЕсли твой бот локализован под определенную страну или группу стран, тогда выбери страну с целевыми пользователями. Если хочешь чтобы бот продвигался не зависимо от страны проживания пользователей, нажми - "Все страны".<a href="https://imbt.ga/rbJntgXEla">&#160;</a>')
        elif command == '!news':
            try:
                button_text = getattr(c1, 'text')
                if button_text == '1. Новости и СМИ':
                    setattr(c1, 'text', '✔️ 1. Новости и СМИ')
                elif button_text == '✔️ 1. Новости и СМИ':
                    setattr(c1, 'text', '1. Новости и СМИ')
                markup = types.InlineKeyboardMarkup()

                markup.row(c1)
                markup.row(c2)
                markup.row(c3)
                markup.row(c4)
                markup.row(c5)
                markup.row(c6)
                markup.row(c7)
                markup.row(c8)
                markup.row(c9)
                markup.row(c10)
                markup.row(c11)
                markup.row(c12)
                markup.row(c13)
                markup.row(c14)
                markup.row(c15)
                markup.row(c16)
                markup.row(c17)
                markup.row(c18)
                markup.row(c19)
                markup.row(c20)
                markup.row(c21)
                markup.row(c22)
                markup.row(c23)
                markup.row(c24)
                markup.row(c25)
                markup.row(c26)
                markup.row(c27)
                markup.row(c28)
                markup.row(c29)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
            except:
                print('\nsdasdas\n')
        elif command == 'crypto':
            try:
                markup = types.InlineKeyboardMarkup()
                
                c1 = types.InlineKeyboardButton(text='1. Новости и СМИ', callback_data='news')
                c2 = types.InlineKeyboardButton(text='check 2. Криптовалюты', callback_data='crypto')
                c3 = types.InlineKeyboardButton(text='3. Для взрослых', callback_data='adult')
                c4 = types.InlineKeyboardButton(text='4. Образование', callback_data='education')
                c5 = types.InlineKeyboardButton(text='5. Искусство и фото', callback_data='art')
                c6 = types.InlineKeyboardButton(text='6. Здоровье и Спорт', callback_data='health')
                c7 = types.InlineKeyboardButton(text='7. Технологии', callback_data='tech')
                c8 = types.InlineKeyboardButton(text='8. Путешествия', callback_data='travel')
                c9 = types.InlineKeyboardButton(text='9. Продажи', callback_data='sales')
                c10 = types.InlineKeyboardButton(text='10. Политика', callback_data='policy')
                c11 = types.InlineKeyboardButton(text='11. Видео и фильмы', callback_data='video')
                c12 = types.InlineKeyboardButton(text='12. Мода и красота', callback_data='style')
                c13 = types.InlineKeyboardButton(text='13. Психология', callback_data='psychology')
                c14 = types.InlineKeyboardButton(text='14. Игры и приложения', callback_data='games')
                c15 = types.InlineKeyboardButton(text='15. Книги', callback_data='books')
                c16 = types.InlineKeyboardButton(text='16. Маркетинг, PR, реклама', callback_data='marketing')
                c17 = types.InlineKeyboardButton(text='17. Цитаты', callback_data='quotes')
                c18 = types.InlineKeyboardButton(text='18. Еда и кулинария', callback_data='food')
                c19 = types.InlineKeyboardButton(text='19. Авто', callback_data='auto')
                c20 = types.InlineKeyboardButton(text='20. Экономика', callback_data='economy')
                c21 = types.InlineKeyboardButton(text='21. Telegram', callback_data='telegram')
                c22 = types.InlineKeyboardButton(text='22. Лингвистика', callback_data='lingvist')
                c23 = types.InlineKeyboardButton(text='23. Дизайн', callback_data='design')
                c24 = types.InlineKeyboardButton(text='24. Карьера', callback_data='career')
                c25 = types.InlineKeyboardButton(text='25. Семья и дети', callback_data='family')
                c26 = types.InlineKeyboardButton(text='26. Медицина', callback_data='medicine')
                c27 = types.InlineKeyboardButton(text='27. Рукоделие', callback_data='handmade')
                c28 = types.InlineKeyboardButton(text='28. Животные', callback_data='animals')
                c29 = types.InlineKeyboardButton(text='29. Лайфхаки', callback_data='lifehacks')

                markup.row(c1)
                markup.row(c2)
                markup.row(c3)
                markup.row(c4)
                markup.row(c5)
                markup.row(c6)
                markup.row(c7)
                markup.row(c8)
                markup.row(c9)
                markup.row(c10)
                markup.row(c11)
                markup.row(c12)
                markup.row(c13)
                markup.row(c14)
                markup.row(c15)
                markup.row(c16)
                markup.row(c17)
                markup.row(c18)
                markup.row(c19)
                markup.row(c20)
                markup.row(c21)
                markup.row(c22)
                markup.row(c23)
                markup.row(c24)
                markup.row(c25)
                markup.row(c26)
                markup.row(c27)
                markup.row(c28)
                markup.row(c29)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
            except:
                print('\nsdasdas\n')
        elif(command == 'sc'):

            bot.send_message(call.message.chat.id, parse_mode="HTML", text='Теперь пришли мне юзер или ссылку на твоего бота или канал.<a href="https://telegra.ph/file/7b0e662039812d457bc62.jpg">&#160;</a>')
            
            
            @bot.message_handler(content_types=['text'])
            def botid(message):
                conn = sqlite3.connect('robo_users')
                cursor = conn.cursor()
                mess = message.text
                rnd = random.randint(0, 9999999)
                user = (rnd, message.from_user.id, mess, 'bot')
                x = list(mess)
                if x[0] == '@':
                    try:
                        cursor.execute('INSERT INTO BAC_DB (ID, ID_OF_OWNER, UN, B_OR_C) VALUES (?, ?, ?, ?)', user)
                        conn.commit()
                        conn.close()
                    except sqlite3.DatabaseError as err:       
                        print("Error: ", err)
                    bot.send_message(message.chat.id, text='<b>Модерация!</b>\nИдёт модерация. После прохождения модерации я сообщу тебе о следующих этапах.<a href="https://telegra.ph/file/ff35a013de4c89a43f02c.jpg">&#160;</a>', parse_mode='HTML')
                    bot.register_next_step_handler(message, owner_menu)
                else:
                    bot.send_message(message.chat.id, text='<b>Укажите корректное название канала или бота!</b>', parse_mode='HTML')
                    bot.register_next_step_handler(message, botid)
                    conn.close()

    except Exception as e:
        bot.send_message(call.message.chat.id, 'nope(')
        

@bot.callback_query_handler(func=lambda call: call.data == re.search('^news$'))
def gercall(call):
    if call.data == 'news':
        print(f'\n{call.data}\n')

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)
