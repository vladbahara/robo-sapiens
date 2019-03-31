# -*- coding: utf-8 -*-
import logging
import sqlite3
import time
import telebot
from telebot import types
from config import token



logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(token)




@bot.message_handler(commands=[''])
def empty_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/start')
    msg = bot.send_message(message.chat.id, 'Нажимай старт!', reply_markup=markup)
    bot.register_next_step_handler(msg, start)


@bot.message_handler(commands=['start'])
def start(message):
    user = (message.from_user.id, message.from_user.username, message.from_user.first_name)
    conn = sqlite3.connect('robo_users')
    cursor = conn.cursor()
    cursor.execute(f'SELECT ID FROM users WHERE ID = {user[0]}')
    res = cursor.fetchall()

    if res == []:
        cursor.execute("INSERT INTO users (ID, UN, NAME, ACCOUNT, MONEY) VALUES (?, ?, ?, 'user', 0.0)", user)
        conn.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🏬 Владелец', '🚶‍ Пользователь')
        msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть 1!', reply_markup=markup)
        bot.register_next_step_handler(msg, manage)
        conn.close()
        
    elif res != []:
        cursor.execute(f'SELECT ACCOUNT FROM users WHERE ID = {user[0]}')
        r = cursor.fetchall()
        print(r)
        if r[0][0] == 'owner':
            conn.close()
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
            markup.row('📬 Рассказать друзьям')
            markup.row('Разместить бота, канал')
            markup.row('Мой счёт')
            markup.row('Статистика продвижения')
            markup.row('🏬 Изменить аккаунт')
            msg = bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(msg, owner_menu)
            
        elif r[0][0] == 'user':
            conn.close()
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
            markup.row('📬 Рассказать друзьям')
            markup.row('Поиск')
            markup.row('Изменить интересы')
            markup.row('Частота рассылки')
            markup.row('🏬 Изменить аккаунт')
            msg = bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(msg, user_menu)
        else:
            bot.send_message(message.chat.id, 'Россия хуле! 1')
            conn.close()
        
    else:
        bot.send_message(message.chat.id, 'Россия хуле! 2')
        conn.close()


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
            msg = bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(msg, owner_menu)

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
            msg = bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            bot.register_next_step_handler(msg, user_menu)
        elif (mess == '/start'):
            msg = bot.send_message(message.chat.id, 'Меню', reply_markup=markup)
            start(msg)
        else:
            conn.close()
            raise Exception()
        

    except Exception as e:
        conn.close()
        start(message)



def owner_menu(message):  # Владелец
    conn = sqlite3.connect('robo_users')
    cursor = conn.cursor()
    try:
        mess = message.text

        if(mess == u'📬 Рассказать друзьям'):
            markup = types.InlineKeyboardMarkup()
            forward_btn = types.InlineKeyboardButton(text='📱 Отправить', url='https://t.me/share/url?url=https://t.me/RS_Media_Bot')
            markup.add(forward_btn)
            msg = bot.send_message(message.chat.id, 'Я бот который поможет рассказать о твоём боте или канале тем пользователям, которых это может заинтересовать. Рассылка делается на основании интересов которые заполнили пользователи, так что они будут получать только качественный и интересный контент.<a href="https://imbt.ga/2bLbzibnr0">&#160;</a>', reply_markup=markup, parse_mode='HTML')
            bot.register_next_step_handler(msg, owner_menu)

        elif (mess == u'Разместить бота, канал'):
            
            markup = types.InlineKeyboardMarkup()
            add_bot = types.InlineKeyboardButton(text='Разместить бота', callback_data='add_bot_command')
            add_channel = types.InlineKeyboardButton(text='Разместить канал', callback_data='add_channel_command')
            markup.row(add_bot)
            markup.row(add_channel)
            msg = bot.send_message(message.chat.id, '<b>Разместить бота, канал!</b>\nВыбери, что именно ты хочешь разместить. Бота или канал?<a href="https://imbt.ga/nwmnR4wpIZ">&#160;</a>', parse_mode='HTML', reply_markup=markup)
                
            


        elif (mess == u'Мой счёт'):
            cursor.execute(f'SELECT MONEY FROM users WHERE ID = {message.from_user.id}')
            money = cursor.fetchall()
            markup = types.InlineKeyboardMarkup()
            add_money = types.InlineKeyboardButton(text='💰 Пополнить счёт', callback_data='add_money')
            markup.add(add_money)
            conn.close()
            if money[0][0] < 1.0:
                msg = bot.send_message(message.chat.id, text=f'<b>Мой счёт!</b>\nЧтобы продвигать бота, на счету должно быть не менее 1$.<a href="https://imbt.ga/UlmN4K1cot">&#160;</a>\n💰  <b>{money[0][0]} $</b>', parse_mode='HTML', reply_markup=markup)
                bot.register_next_step_handler(msg, owner_menu)
            else:
                msg = bot.send_message(message.chat.id, text=f'<b>Мой счёт!</b>\nКаждый целевой переход в бота или канал стоит 2 цента.<a href="https://imbt.ga/UlmN4K1cot">&#160;</a>\n💰  <b>{money[0][0]} $</b>', parse_mode='HTML', reply_markup=markup)
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
            msg = bot.send_message(message.chat.id, 'Выбери аккаунт, кем хочешь быть! 3', reply_markup=markup)
            bot.register_next_step_handler(msg, manage)

        elif (mess == u'/start'):
            start(message)
        else:
            conn.close()
            raise Exception()

    except Exception as e:
        msg = bot.send_message(message.chat.id, 'Выберите один из пунктов!')
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
        msg = bot.send_message(message.chat.id, 'Ошибочка( 3')
        bot.register_next_step_handler(msg, user_menu)




@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('robo_users')
    cursor = conn.cursor()
    command = call.data
    user = call.message.chat.id
    try:
        if(command == 'add_bot_command'):
            markup = types.InlineKeyboardMarkup()
            c1 = types.InlineKeyboardButton(text='1. Новости и СМИ', callback_data='saa')
            c2 = types.InlineKeyboardButton(text='2. Криптовалюты', callback_data='saa')
            c3 = types.InlineKeyboardButton(text='3. Для взрослых', callback_data='saa')
            c4 = types.InlineKeyboardButton(text='4. Образование', callback_data='saa')
            c5 = types.InlineKeyboardButton(text='5. Искусство и фото', callback_data='saa')
            c6 = types.InlineKeyboardButton(text='6. Здоровье и Спорт', callback_data='saa')
            c7 = types.InlineKeyboardButton(text='7. Технологии', callback_data='saa')
            c8 = types.InlineKeyboardButton(text='8. Путешествия', callback_data='saa')
            c9 = types.InlineKeyboardButton(text='9. Продажи', callback_data='saa')
            c10 = types.InlineKeyboardButton(text='10. Политика', callback_data='saa')
            c11 = types.InlineKeyboardButton(text='11. Видео и фильмы', callback_data='saa')
            c12 = types.InlineKeyboardButton(text='12. Мода и красота', callback_data='saa')
            c13 = types.InlineKeyboardButton(text='13. Психология', callback_data='saa')
            c14 = types.InlineKeyboardButton(text='14. Игры и приложения', callback_data='saa')
            c15 = types.InlineKeyboardButton(text='15. Книги', callback_data='saa')
            c16 = types.InlineKeyboardButton(text='16. Маркетинг, PR, реклама', callback_data='saa')
            c17 = types.InlineKeyboardButton(text='17. Цитаты', callback_data='saa')
            c18 = types.InlineKeyboardButton(text='18. Еда и кулинария', callback_data='saa')
            c19 = types.InlineKeyboardButton(text='19. Авто', callback_data='saa')
            c20 = types.InlineKeyboardButton(text='20. Экономика', callback_data='saa')
            c21 = types.InlineKeyboardButton(text='21. Telegram', callback_data='saa')
            c22 = types.InlineKeyboardButton(text='22. Лингвистика', callback_data='saa')
            c23 = types.InlineKeyboardButton(text='23. Дизайн', callback_data='saa')
            c24 = types.InlineKeyboardButton(text='24. Карьера', callback_data='saa')
            c25 = types.InlineKeyboardButton(text='25. Семья и дети', callback_data='saa')
            c26 = types.InlineKeyboardButton(text='26. Медицина', callback_data='saa')
            c27 = types.InlineKeyboardButton(text='27. Рукоделие', callback_data='saa')
            c28 = types.InlineKeyboardButton(text='28. Животные', callback_data='saa')
            c29 = types.InlineKeyboardButton(text='29. Лайфхаки', callback_data='saa')

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
            bot.send_message(call.message.chat.id, 'Add Channel')

        elif(command == 'add_money'):
            cursor.execute(f"UPDATE users SET MONEY = (25.2) WHERE ID = {user}")
            conn.commit()
            conn.close()
            bot.send_message(call.message.chat.id, 'Add Some Demo Money')

        elif(command == 'channel_stat'):
            msg = bot.send_message(call.message.chat.id, '<b>Бот:</b> @ome33\nПереходов: 567 (2 цента за переход)\n💰 <b>11, 34$</b><a href="https://telegra.ph/file/954afb76178f388d7d4f6.jpg">&#160;</a>', parse_mode='HTML')
                    
        elif(command == 'bot_stat'):
            bot.send_message(call.message.chat.id, '<b>Канал:</b> @omfewfe3a3\nПереходов: 957 (2 цента за переход)\n💰 <b>19, 84$</b><a href="https://telegra.ph/file/8cde82c7e8f5f1c8ddf50.jpg">&#160;</a>', )

        elif(command == 'search_bots'):
            bot.send_message(call.message.chat.id, 'Search Bots')

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
            msg = bot.send_message(call.message.chat.id, '<b>Изменить интересы!</b>\nВыбирай какие именно интересы ты хочешь изменить.<a href="https://telegra.ph/file/8c2abab1d2ecfc76677d2.jpg">&#160;</a>', parse_mode='HTML', reply_markup=markup)

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
            msg = bot.send_message(message.chat.id, '<b>Частота рассылки!</b>\nКак часто ты хочешь получить россылку каналов и ботов подобранных индивидуально для тебя?<a href="https://imbt.ga/UuCEyp73zo">&#160;</a>', parse_mode='HTML', reply_markup=markup)
            bot.register_next_step_handler(msg, user_menu)

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
            c1 = types.InlineKeyboardButton(text='Россия', callback_data='sc')
            c2 = types.InlineKeyboardButton(text='Украина', callback_data='sc')
            c3 = types.InlineKeyboardButton(text='Белоруссия', callback_data='sc')
            c4 = types.InlineKeyboardButton(text='Казахстан', callback_data='sc')
            c5 = types.InlineKeyboardButton(text='Узбекистан', callback_data='sc')
            c6 = types.InlineKeyboardButton(text='Грузия', callback_data='sc')
            c7 = types.InlineKeyboardButton(text='Молдавия', callback_data='sc')
            c8 = types.InlineKeyboardButton(text='Литва', callback_data='sc')
            c9 = types.InlineKeyboardButton(text='Латвия', callback_data='sc')
            c10 = types.InlineKeyboardButton(text='Эстония', callback_data='sc')
            c11 = types.InlineKeyboardButton(text='Армения', callback_data='sc')
            c12 = types.InlineKeyboardButton(text='Таджикистан', callback_data='sc')
            c13 = types.InlineKeyboardButton(text='Азербайджан', callback_data='sc')
            c14 = types.InlineKeyboardButton(text='Киргизия', callback_data='sc')
            c15 = types.InlineKeyboardButton(text='Туркменистан', callback_data='sc')
            c16 = types.InlineKeyboardButton(text='🗺️ Все страны', callback_data='sc')
            

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
        elif(command == 'sc'):
            bot.send_message(call.message.chat.id, parse_mode="HTML", text='Теперь пришли мне юзер или ссылку на твоего бота или канал.<a href="https://telegra.ph/file/7b0e662039812d457bc62.jpg">&#160;</a>')
            
            
            @bot.message_handler(content_types=['text'])
            def botid(message):
                mess = message.text
                x = list(mess)
                if x[0] == '@':
                    msg = bot.send_message(message.chat.id, text='<b>Модерация!</b>\nИдёт модерация. После прохождения модерации я сообщу тебе о следующих этапах.<a href="https://telegra.ph/file/ff35a013de4c89a43f02c.jpg">&#160;</a>', parse_mode='HTML')
                    bot.register_next_step_handler(msg, owner_menu)
                else:
                    msg = bot.send_message(message.chat.id, text='<b>Укажите корректное название канала или бота!</b>', parse_mode='HTML')
                    bot.register_next_step_handler(msg, botid)

    except Exception as e:
        bot.send_message(call.message.chat.id, 'nope(')
        
    



if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(10)
