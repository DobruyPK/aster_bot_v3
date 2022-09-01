import datetime
import os
import threading
import time
from threading import Thread

import requests
import telebot
from dotenv import load_dotenv
from telebot import types

import core
import data_store
import enums
import parse
import sql_methods
from core import curent_time_now
from parse import data_fortness

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
bot = telebot.TeleBot(os.environ.get('TOKEN'))
bos_tupe = ['Simple boss!', 'Drake apic boss', 'Apic boss']
tupe_subs = ["not_1h", "not_30m", "not_15m", "not_5m"]
list_3b_loa = ['Drake Leader', 'Dragon Beast', 'Begemoth Leader']
time_notif = data_store.TimerNotific()


def server_info(server: str, chat_id):
    inline_btn_boss = types.InlineKeyboardButton(
        'Боссы',
        callback_data=f'Boss,{server}')
    inline_btn_castles = types.InlineKeyboardButton(
        'Замки',
        callback_data=f'Castles,{server}')
    inline_btn_fortness = types.InlineKeyboardButton(
        'Форты ',
        callback_data=f'fortness,{server}')
    inline_btn_therd_rb = types.InlineKeyboardButton(  # 3рб стакато
        '3РБ - ЛОА',
        callback_data=f'3rbLOA,{server}'
    )
    inline_btm_server_status = types.InlineKeyboardButton(
        'Состояние сервера',
        callback_data=f'server,{server}'
    )
    keyboard = types.InlineKeyboardMarkup().add(inline_btn_boss)
    keyboard.row(inline_btn_castles, inline_btn_fortness)
    keyboard.row(inline_btn_therd_rb, inline_btm_server_status)
    bot.send_message(chat_id=chat_id,
                     text="Выбирай тип инфы!", reply_markup=keyboard)


@bot.message_handler(commands=enums.ParseURL.servers())
def slect_by_comand(message):
    server = message.text.replace('/', '')
    server_info(server, message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def select_func(callback_query: types.CallbackQuery):
    list_data = callback_query.data.split(',')
    if len(list_data) == 1:
        if list_data[0] in enums.ParseURL.servers():
            select_type_info(callback_query)
    if len(list_data) == 2:
        if list_data[0] == 'statusserver' and list_data[1] in enums.ParseURL.servers():
            subs_to_server_status(callback_query)
        if list_data[0] == 'server' and list_data[1] in enums.ParseURL.servers():
            server_status_message(callback_query)
        if list_data[0] in list_3b_loa and list_data[1] in enums.ParseURL.servers():
            create_message_3rb(callback_query)
        if list_data[0] == '3rbLOA' and list_data[1] in enums.ParseURL.servers():
            third_rb_loa_registration(callback_query)
        if list_data[1] in enums.ParseURL.servers() and list_data[
            0] in parse.DatasaverFortnesCastleBoss.get_castle_dict(
            data_fortness,
            list_data[1]):
            subskribe_castle_message(callback_query)
        if list_data[0] == 'fortness' and list_data[1] in enums.ParseURL.servers():
            list_fortnes(callback_query)
        if list_data[0] == 'Castles' and list_data[1] in enums.ParseURL.servers():
            list_castles(callback_query)
        if list_data[0] == 'Boss' and list_data[1] in enums.ParseURL.servers():
            select_boss_type(callback_query)
        if list_data[0] in bos_tupe and list_data[1] in enums.ParseURL.servers():
            type_boss(callback_query)
        if list_data[1] in enums.ParseURL.servers() and list_data[0] in parse.DatasaverFortnesCastleBoss.get_bosslist(
                data_fortness,
                list_data[1]):
            resp_time(callback_query)
    if len(list_data) == 3:
        if list_data[0] == '3rbLOA' and list_data[1] == 'no' and list_data[2] in enums.ParseURL.servers():
            third_rb_loa_boss_was_dead(callback_query)
        if list_data[0] == '3rbLOA' and list_data[1] == 'yes' and list_data[2] in enums.ParseURL.servers():
            third_rb_load_reg_ok(callback_query)
        if list_data[0] == 'subscribe' and list_data[2] in enums.ParseURL.servers() and list_data[
            1] in parse.DatasaverFortnesCastleBoss.get_bosslist(data_fortness,
                                                                list_data[2]):
            subs(callback_query)
    if len(list_data) == 4:
        if list_data[0] == 'sub' and list_data[1] in tupe_subs and list_data[3] in enums.ParseURL.servers() and \
                list_data[2] in parse.DatasaverFortnesCastleBoss.get_bosslist(data_fortness,
                                                                              list_data[3]):
            notidications(callback_query)
            # TODO: КАК ЗАПИХАТЬ УСЛОВИЕ ЭТО ПО ПЕП8
        if list_data[0] == '3rbLOA' and list_data[1] == 'subscribe' and list_data[3] in enums.ParseURL.servers() and \
                list_data[2] in list_3b_loa:
            create_notif_3rb_sub(callback_query)
        if list_data[0] == 'sub' and list_data[1] in tupe_subs and list_data[3] in enums.ParseURL.servers() and \
                list_data[2] in list_3b_loa:
            notific_3rb(callback_query)


def server_status_message(callback_query):
    chatid = callback_query.message.chat.id
    list_data = callback_query.data.split(',')
    server = list_data[1]
    servers_status = time_notif.get_server_status()
    tg_id = callback_query.from_user.id
    user = sql_methods.get_user(tg_id)
    username = callback_query.from_user.username
    keyboard = types.InlineKeyboardMarkup()
    subskribe = sql_methods.get_subsckribe_server_status(tg_id, server)
    if user is None and subskribe is None:
        sql_methods.create_user(tg_id, username)
        inline_btn_sub_server_status = types.InlineKeyboardButton(
            'Подписаться!❌',
            callback_data=f'statusserver,{server}'
        )
        keyboard.add(inline_btn_sub_server_status)
    elif subskribe is None:
        inline_btn_sub_server_status = types.InlineKeyboardButton(
            'Подписаться!❌',
            callback_data=f'statusserver,{server}'
        )
        keyboard.add(inline_btn_sub_server_status)
    else:
        inline_btn_server_status_sub = types.InlineKeyboardButton(
            'Подписаться ✅',
            callback_data=f'statusserver,{server}'
        )
        keyboard.add(inline_btn_server_status_sub)
    if type(servers_status[server]) != 'offline':
        bot.send_message(chat_id=chatid,
                         text=f'''сервак работает онлайн примерно {int(servers_status[server])}''',
                         reply_markup=keyboard)
    else:
        bot.send_message(chat_id=chatid,
                         text=f'''сервак лежит((''',
                         reply_markup=keyboard)


def subs_to_server_status(callback_query):
    list_data = callback_query.data.split(',')
    server = list_data[1]
    chatid = callback_query.message.chat.id
    tg_id = callback_query.from_user.id
    # username = callback_query.from_user.username
    # user = sql_methods.get_user(tg_id)
    keyboard = types.InlineKeyboardMarkup()
    mesageid = callback_query.message.id
    subskribe = sql_methods.get_subsckribe_server_status(tg_id, server)
    if subskribe is None:
        sql_methods.create_subsckribe_server_status(tg_id, server)
        inline_btn_server_status_sub = types.InlineKeyboardButton(
            'Подписаться ✅',
            callback_data=f'statusserver,{server}')
    else:
        sql_methods.delete_subsckribe_server_status(tg_id, server)
        inline_btn_server_status_sub = types.InlineKeyboardButton(
            'Подписаться!❌',
            callback_data=f'statusserver,{server}'
        )
    keyboard.add(inline_btn_server_status_sub)
    bot.edit_message_text(message_id=mesageid, chat_id=chatid,
                          text=callback_query.message.text, reply_markup=keyboard)


# def change_sub_status_server(callback_query):
#     list_data = callback_query.data.split(',')
#     server = list_data[1]
#     chatid = callback_query.message.chat.id
#     tg_id = callback_query.from_user.id
#     username = callback_query.from_user.username
#     user = sql_methods.get_user(tg_id)
#     keyboard = types.InlineKeyboardMarkup()
#     mesageid = callback_query.message.id
#     if user is None:
#         sql_methods.create_user(tg_id, username)
#     subskribe = sql_methods.get_subsckribe_server_status(tg_id, server)
#     if subskribe is None:
#         sql_methods.create_subsckribe_server_status(tg_id, server)
#         inline_btn_server_status_sub = types.InlineKeyboardButton(
#             'Получать уведление если что то изменится ✅',
#             callback_data=f'statusserversub,{server}')
#     else:
#         sql_methods.delete_subsckribe_server_status(tg_id, server)
#         inline_btn_server_status_sub = types.InlineKeyboardButton(
#             'Получать уведление если что то изменится ❌',
#             callback_data=f'statusserversub,{server}'
#         )
#     keyboard.add(inline_btn_server_status_sub)
#     bot.edit_message_text(message_id=mesageid, chat_id=chatid,
#                           text=callback_query.message.text, reply_markup=keyboard)


def third_rb_loa_registration(callback_query):
    list_data = callback_query.data.split(',')
    server = list_data[1]
    inline_btn_therd_rb_yes = types.InlineKeyboardButton(
        'Да',
        callback_data=f'3rbLOA,yes,{server}'
    )
    inline_btn_therd_rb_no = types.InlineKeyboardButton(
        'Нет',
        callback_data=f'3rbLOA,no,{server}'
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard = keyboard.row(inline_btn_therd_rb_yes, inline_btn_therd_rb_no)
    bot.send_message(chat_id=callback_query.message.chat.id,
                     text="Вы убил какого босса из 3х?", reply_markup=keyboard)


def third_rb_loa_boss_was_dead(callback_query):
    bot.send_message(chat_id=callback_query.message.chat.id,
                     text="Возвращайтесь как убьете босса!")


def third_rb_load_reg_ok(callback_query):
    chatid = callback_query.message.chat.id
    mesageid = callback_query.message.id
    list_data = callback_query.data.split(',')
    server = list_data[2]
    buttom_drake_leader = types.InlineKeyboardButton(
        'Drake Leader',
        callback_data=f'Drake Leader,{server}'
    )
    buttom_dragon_beast = types.InlineKeyboardButton(
        'Dragon Beast',
        callback_data=f'Dragon Beast,{server}'
    )
    buttom_begemoth_leader = types.InlineKeyboardButton(
        'Begemoth Leader',
        callback_data=f'Begemoth Leader,{server}'
    )
    keyboard = types.InlineKeyboardMarkup().add(buttom_drake_leader)
    keyboard.add(buttom_dragon_beast)
    keyboard.add(buttom_begemoth_leader)
    bot.edit_message_text(message_id=mesageid, chat_id=chatid,
                          text='какого РБ убил?', reply_markup=keyboard)


def create_message_3rb(callback_query):
    data_list = callback_query.data.split(',')
    bossname = data_list[0]
    server = data_list[1]
    boss_resp = types.InlineKeyboardButton(
        f'Подписаться на {bossname}',
        callback_data=f'3rbLOA,subscribe,{bossname},{server}')
    keyboard = types.InlineKeyboardMarkup().add(boss_resp)
    bot.send_message(chat_id=callback_query.message.chat.id,
                     text=f'''ГЦ! \n'''
                          f'''Бос {bossname} появится через 4 часа''',
                     reply_markup=keyboard)


def create_notif_3rb_sub(callback_query):
    data_list = callback_query.data.split(',')
    bossname = data_list[2]
    server = data_list[3]
    tg_id = callback_query.from_user.id
    username = callback_query.from_user.username
    user = sql_methods.get_user(tg_id)
    if user is None:
        sql_methods.create_user(tg_id, username)
    subscribe = sql_methods.get_subscribe_3rb(tg_id, bossname, server)
    if subscribe is None:
        keyboard = generate_keyboard(None, None, None, None, bossname, server)
    else:
        keyboard = generate_keyboard(subscribe[4], subscribe[5], subscribe[6], subscribe[7], bossname, server)
    bot.send_message(chat_id=callback_query.message.chat.id,
                     text='Выберите врмея напоминания',
                     reply_markup=keyboard)


def notific_3rb(callback_query):
    data_list = callback_query.data.split(',')
    chatid = callback_query.message.chat.id
    messageid = callback_query.message.id
    tg_id = callback_query.from_user.id
    server = data_list[3]
    bossname = data_list[2]
    tybenotificattion = data_list[1]
    update_key = subscribes_3rb(tybenotificattion, tg_id, bossname, server)

    if update_key is True:
        subscribe = sql_methods.get_subscribe_3rb(tg_id, bossname, server)
        keyboard = generate_keyboard(subscribe[4], subscribe[5], subscribe[6], subscribe[7], bossname, server)
        bot.edit_message_text(message_id=messageid, chat_id=chatid,
                              text='Выберите врмея напоминания', reply_markup=keyboard)
    sql_methods.deleteNotactivesubsckribe_3rb()
    update_cash()


def subscribes_3rb(tybenotificattion: str, tg_id: int, bossname: str, server: str):
    subskribe = sql_methods.get_subscribe_3rb(tg_id, bossname, server)
    t_d_1h = datetime.timedelta(hours=1)
    t_d_30m = datetime.timedelta(minutes=30)
    t_d_15m = datetime.timedelta(minutes=15)
    t_d_5m = datetime.timedelta(minutes=5)
    t_d_resp = datetime.timedelta(hours=4)
    if subskribe is None:
        time_kill = curent_time_now()
        time_resp = time_kill + t_d_resp
        not_time = ''
        if tybenotificattion == 'not_1h':
            not_time = time_resp - t_d_1h
        elif tybenotificattion == 'not_30m':
            not_time = time_resp - t_d_30m
        elif tybenotificattion == 'not_15m':
            not_time = time_resp - t_d_15m
        elif tybenotificattion == 'not_5m':
            not_time = time_resp - t_d_5m
        sql_methods.create_subscribe_3rb(tg_id, bossname, tybenotificattion, not_time, server, time_kill)
        update_cash()
    else:
        time_kill = datetime.datetime.strptime(subskribe[2].replace('.0000000', ''), "%Y-%m-%d %H:%M:%S")
        time_resp = time_kill + t_d_resp
        not_time = ''
        if tybenotificattion == 'not_1h':
            not_time = time_resp - t_d_1h
        elif tybenotificattion == 'not_30m':
            not_time = time_resp - t_d_30m
        elif tybenotificattion == 'not_15m':
            not_time = time_resp - t_d_15m
        elif tybenotificattion == 'not_5m':
            not_time = time_resp - t_d_5m
        dict_subskribe = {"not_1h": subskribe[4],
                          "not_30m": subskribe[5],
                          "not_15m": subskribe[6],
                          "not_5m": subskribe[7]}
        for type_subs, valuse_subs in dict_subskribe.items():
            if type_subs == tybenotificattion:
                if valuse_subs == '3000-01-01 00:00:00.0000000':
                    sql_methods.update_subscribe_3rb(tg_id, bossname, tybenotificattion, not_time, server)
                    update_cash()
                else:
                    not_time = '3000-01-01'
                    sql_methods.update_subscribe_3rb(tg_id, bossname, tybenotificattion, not_time, server)
                    update_cash()
    return True


def list_castles(callback_query):
    list_data = callback_query.data.split(',')
    server = list_data[1]
    castle_name_list = sql_methods.get_all_castle_name_by_server(server)
    keyboard = types.InlineKeyboardMarkup()
    for castle_name in castle_name_list:
        inline_castle = types.InlineKeyboardButton(
            castle_name,
            callback_data=f'{castle_name},{server}')
        keyboard.add(inline_castle)
    bot.send_message(chat_id=callback_query.message.chat.id,
                     text="Выбирай замок!", reply_markup=keyboard)


def subskribe_castle_message(callback_query):
    vl_current_time = curent_time_now()
    list_castle_server_callback = callback_query.data.split(',')
    castlename = list_castle_server_callback[0]
    server = list_castle_server_callback[1]
    castle_info = sql_methods.select_castles(castlename, server)
    castlename = castle_info[0]
    castle_siege_time = datetime.datetime.strptime(
        castle_info[1].replace('.0000000', ''),
        "%Y-%m-%d %H:%M:%S",
    )
    message = core.create_message_castle(castle_info, server)
    if castle_siege_time > vl_current_time:
        bot.send_message(chat_id=callback_query.message.chat.id,
                         text=message)
    else:
        inline_subsk = types.InlineKeyboardButton(
            f'Подписаться  на осаду замка {castlename}!',
            callback_data=f'subscribe,{castlename},{server}')
        keyboard = types.InlineKeyboardMarkup().add(inline_subsk)
        bot.send_message(chat_id=callback_query.message.chat.id,
                         text=message,
                         reply_markup=keyboard)


def list_fortnes(callback_query):
    list_data = callback_query.data.split(',')
    server = list_data[1]
    castle_name_list = sql_methods.get_all_fort_name_by_server(server)
    keyboard = types.InlineKeyboardMarkup()
    for castle_name in castle_name_list:
        inline_castle = types.InlineKeyboardButton(
            castle_name,
            callback_data=f'None_active_bottom')
        # TODO: вот это можено списком убирай кнопки в теории при нажатии можно скрин карты с фортом
        keyboard.add(inline_castle)
    bot.send_message(chat_id=callback_query.message.chat.id,
                     text="Форты доступные для захвата:", reply_markup=keyboard)


def select_type_info(callback_query: types.CallbackQuery):
    server = callback_query.data
    server_info(server, callback_query.message.chat.id)


@bot.message_handler(commands=['start'])  # вот сюда вставить новый сервер
def start(message):
    inline_btn_s_server_1 = types.InlineKeyboardButton(
        'Prime X1',
        callback_data='prime_x1')
    inline_btn_a_server_2 = types.InlineKeyboardButton(
        'Asterios X5',
        callback_data='asterios_x5')
    inline_btn_a_server_3 = types.InlineKeyboardButton(
        'Hunter x55',
        callback_data='hunter_x55')
    inline_btn_a_server_4 = types.InlineKeyboardButton(
        'Medea x3',
        callback_data='media_x3')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(inline_btn_s_server_1, inline_btn_a_server_2)
    keyboard.row(inline_btn_a_server_3, inline_btn_a_server_4)
    bot.send_message(chat_id=message.chat.id, text="Выбирай сервер", reply_markup=keyboard)


def select_boss_type(callback_query: types.CallbackQuery):
    server = callback_query.data.split(',')[1]
    inline_btn_s_boss = types.InlineKeyboardButton(
        'Обычный босс',
        callback_data=f'Simple boss!,{server}')
    inline_btn_a_boss = types.InlineKeyboardButton(
        'Эпики',
        callback_data=f'Apic boss,{server}')
    inline_btn_drake_apik = types.InlineKeyboardButton(
        'ХайЭпики',
        callback_data=f'Drake apic boss,{server}')
    keyboard = types.InlineKeyboardMarkup().add(inline_btn_s_boss)
    keyboard.row(inline_btn_a_boss, inline_btn_drake_apik)
    bot.send_message(chat_id=callback_query.message.chat.id,
                     text="Выбирай тип босса!", reply_markup=keyboard)


def type_boss(callback_query: types.CallbackQuery):
    server_aster = callback_query.data.split(',')[1]
    keyboard = types.InlineKeyboardMarkup()
    if 'Apic boss' in callback_query.data:
        list_boss_by_type = sql_methods.select_boss_type(1, server_aster)
        for boss in list_boss_by_type:
            boss = boss[0]
            inline_btn_apik = types.InlineKeyboardButton(
                boss,
                callback_data=f'{boss},{server_aster}')
            keyboard.add(inline_btn_apik)

    if 'Drake apic boss' in callback_query.data:
        list_boss_by_type = sql_methods.select_boss_type(2, server_aster)
        for boss in list_boss_by_type:
            boss = boss[0]
            inline_btn_apik = types.InlineKeyboardButton(
                boss,
                callback_data=f'{boss},{server_aster}')
            keyboard.add(inline_btn_apik)

    if 'Simple boss!' in callback_query.data:
        list_boss_by_type = sql_methods.select_boss_type(0, server_aster)
        for boss in list_boss_by_type:
            boss = boss[0]
            inline_btn_apik = types.InlineKeyboardButton(
                boss,
                callback_data=f'{boss},{server_aster}')
            keyboard.add(inline_btn_apik)
    bot.send_message(chat_id=callback_query.message.chat.id,
                     text="Выбирай босса!",
                     reply_markup=keyboard)


def resp_time(callback_query: types.CallbackQuery):
    vl_current_time = curent_time_now()
    list_boss_server_callback = callback_query.data.split(',')
    bossname = list_boss_server_callback[0]
    server = list_boss_server_callback[1]
    boss_info = sql_methods.select_boss(bossname, server)
    boss = boss_info[0]
    start_resp = datetime.datetime.strptime(
        boss_info[2].replace('.0000000', ''),
        "%Y-%m-%d %H:%M:%S",
    )
    message = core.create_message(boss, server)
    if start_resp < vl_current_time:
        bot.send_message(chat_id=callback_query.message.chat.id,
                         text=message)
    else:
        inline_subsk = types.InlineKeyboardButton(
            f'Подписаться {boss}!',
            callback_data=f'subscribe,{boss},{server}')
        keyboard = types.InlineKeyboardMarkup().add(inline_subsk)
        bot.send_message(chat_id=callback_query.message.chat.id,
                         text=message,
                         reply_markup=keyboard)


def generate_bottom(staus, bossname, typesubs, server):
    msg_dict = {"not_1h": '1 час',
                "not_30m": 'полчаса',
                "not_15m": '15 минут',
                "not_5m": '5 минут'}
    smail_unsub = '❌'
    sime_sub = '✅'
    if staus == 0:
        current_smile = smail_unsub
    else:
        current_smile = sime_sub
    msg_text = msg_dict[typesubs]
    buttom = types.InlineKeyboardButton(
        f'напомнить за {msg_text} {current_smile}',
        callback_data=f'sub,{typesubs},{bossname},{server}', )
    return buttom


def generate_keyboard(not_1h, not_30m, not_15m, not_5m, bossname, server):
    keyboard = types.InlineKeyboardMarkup()
    if not_1h == '3000-01-01 00:00:00.0000000' or not_1h is None:
        butom = generate_bottom(staus=0, bossname=bossname, typesubs='not_1h', server=server)
        keyboard.add(butom)
    else:
        butom = generate_bottom(staus=1, bossname=bossname, typesubs='not_1h', server=server)
        keyboard.add(butom)

    if not_30m == '3000-01-01 00:00:00.0000000' or not_30m is None:
        butom = generate_bottom(staus=0, bossname=bossname, typesubs='not_30m', server=server)
        keyboard.add(butom)
    else:
        butom = generate_bottom(staus=1, bossname=bossname, typesubs='not_30m', server=server)
        keyboard.add(butom)

    if not_15m == '3000-01-01 00:00:00.0000000' or not_15m is None:
        butom = generate_bottom(staus=0, bossname=bossname, typesubs='not_15m', server=server)
        keyboard.add(butom)
    else:
        butom = generate_bottom(staus=1, bossname=bossname, typesubs='not_15m', server=server)
        keyboard.add(butom)

    if not_5m == '3000-01-01 00:00:00.0000000' or not_5m is None:
        butom = generate_bottom(staus=0, bossname=bossname, typesubs='not_5m', server=server)
        keyboard.add(butom)
    else:
        butom = generate_bottom(staus=1, bossname=bossname, typesubs='not_5m', server=server)
        keyboard.add(butom)
    return keyboard


def subs(callback_query: types.CallbackQuery):
    data_list = callback_query.data.split(',')
    bossname = data_list[1]
    server = data_list[2]
    tg_id = callback_query.from_user.id
    username = callback_query.from_user.username
    parse.DatasaverFortnesCastleBoss.set_selctboss(data_fortness, bossname, server)
    user = sql_methods.get_user(tg_id)
    if user is None:
        sql_methods.create_user(tg_id, username)
    subscribe = sql_methods.get_subscribe(tg_id, bossname, server)
    if subscribe is None:
        keyboard = generate_keyboard(None, None, None, None, bossname, server)
    else:
        keyboard = generate_keyboard(subscribe[3], subscribe[4], subscribe[5], subscribe[6], bossname, server)
    bot.send_message(chat_id=callback_query.message.chat.id,
                     text='Выберите врмея напоминания',
                     reply_markup=keyboard)


def notidications(callback_query: types.CallbackQuery):
    chatid = callback_query.message.chat.id
    mesageid = callback_query.message.id
    tg_id = callback_query.from_user.id
    server = callback_query.data.split(',')[3]
    bossname = ''
    update_key = bool()
    for var_bossname in data_fortness.get_bosslist(server):
        if var_bossname in callback_query.data.split(','):
            bossname = var_bossname
            tybenotificattion = callback_query.data.split(',')[1]
            update_key = subscribes(tybenotificattion, tg_id, bossname, server)
    if update_key is True:
        subscribe = sql_methods.get_subscribe(tg_id, bossname, server)
        keyboard = generate_keyboard(subscribe[3], subscribe[4], subscribe[5], subscribe[6], bossname, server)
        bot.edit_message_text(message_id=mesageid, chat_id=chatid,
                              text='Выберите врмея напоминания', reply_markup=keyboard)
    sql_methods.deleteNotactivesubsckribe()
    update_cash()


def subscribes(tybenotificattion: str, tg_id: int, bossname: str, server: str):
    subskribe = sql_methods.get_subscribe(tg_id, bossname, server)
    strt_resp = datetime.datetime.strptime(
        sql_methods.select_boss(bossname, server)[2].replace('.0000000', ''),
        "%Y-%m-%d %H:%M:%S",
    )
    t_d_1h = datetime.timedelta(hours=1)
    t_d_30m = datetime.timedelta(minutes=30)
    t_d_15m = datetime.timedelta(minutes=15)
    t_d_5m = datetime.timedelta(minutes=5)
    not_time = ''
    if tybenotificattion == 'not_1h':
        not_time = strt_resp - t_d_1h
    elif tybenotificattion == 'not_30m':
        not_time = strt_resp - t_d_30m
    elif tybenotificattion == 'not_15m':
        not_time = strt_resp - t_d_15m
    elif tybenotificattion == 'not_5m':
        not_time = strt_resp - t_d_5m
    if subskribe is None:
        sql_methods.create_subscribe(tg_id, bossname, tybenotificattion, not_time, server)
        update_cash()
    else:
        dict_subskribe = {"not_1h": subskribe[3],
                          "not_30m": subskribe[4],
                          "not_15m": subskribe[5],
                          "not_5m": subskribe[6]}
        for type_subs, valuse_subs in dict_subskribe.items():
            if type_subs == tybenotificattion:
                if valuse_subs == '3000-01-01 00:00:00.0000000':
                    sql_methods.update_subscribe(tg_id, bossname, tybenotificattion, not_time, server)
                    update_cash()
                else:
                    not_time = '3000-01-01'
                    sql_methods.update_subscribe(tg_id, bossname, tybenotificattion, not_time, server)
                    update_cash()
    return True


def update_cash():
    timerinfo = sql_methods.getnearestsub()
    data_store.TimerNotific.set_data_notifc(time_notif,
                                            core.find_min_time_for_timer_notification(timerinfo))
    timerinfo_3rb = sql_methods.GetNearestSub_3rb()
    data_store.TimerNotific.update_data_3rb(time_notif,
                                            core.find_min_time_for_timer_notification_3rb(timerinfo_3rb))

    for server in enums.ParseURL:
        bos_list = sql_methods.get_all_boss_names(server.name)
        castle_list = sql_methods.get_all_castle_name_by_server(server.name)
        parse.DatasaverFortnesCastleBoss.apdate_boss_list(data_fortness, bos_list, server.name)
        parse.DatasaverFortnesCastleBoss.apdate_castle_dict(data_fortness, castle_list, server.name)


def timer_s():
    vl_current_time = curent_time_now()
    near_boss = sql_methods.select_near_boss()
    time_l_boss = near_boss[0].replace('.0000000', '')
    time_l_boss = datetime.datetime.strptime(
        time_l_boss,
        "%Y-%m-%d %H:%M:%S",
    )
    if time_l_boss < vl_current_time:
        parse.start_parse()
        for server in enums.ParseURL:
            bos_list = sql_methods.get_all_boss_names(server.name)
            parse.DatasaverFortnesCastleBoss.apdate_boss_list(data_fortness, bos_list, server.name)
        threading.Timer(300, timer_s).start()
        return 300
    else:
        for server in enums.ParseURL:
            bos_list = sql_methods.get_all_boss_names(server.name)
            parse.DatasaverFortnesCastleBoss.apdate_boss_list(data_fortness, bos_list, server.name)
            return (vl_current_time - time_l_boss).total_seconds()


def timer_nitification():
    t_ds = datetime.timedelta(seconds=2)
    vl_current_time = curent_time_now()
    data_near_boss = data_store.TimerNotific.get_data_notifc(time_notif)
    try:
        near_notification_time = data_near_boss['time']
        # print(f'near_notification_time_simple--------------{near_notification_time}')
        # print(f'vl_current_time_simple-----------------------{vl_current_time}')
        if near_notification_time - t_ds < vl_current_time < near_notification_time + t_ds:  # было == но так лучше
            time_resp = data_near_boss['boss_resp_time']
            time_resp = time_resp.replace('.0000000', '')
            time_resp = datetime.datetime.strptime(
                time_resp,
                "%Y-%m-%d %H:%M:%S",
            )
            bos = data_near_boss['bossname']
            wait_time = time_resp - vl_current_time
            for tg_id in data_near_boss['tg_id_list']:
                msg = f'Респ {bos} начнется через {wait_time} на сервере {data_near_boss["server"]}'
                bot.send_message(tg_id, msg)
            sql_methods.delete_notific_time(data_near_boss['subsid'], data_near_boss['type_notification'])
            sql_methods.deleteNotactivesubsckribe()  # вот это можно в одну хрень запихать (хранимаю функцию)
            update_cash()
        else:
            if vl_current_time > near_notification_time:
                sql_methods.delete_notific_time(data_near_boss['subsid'], data_near_boss['type_notification'])
                update_cash()
    except BaseException as error:
        print(error)


def timer_nitification_3rb():
    t_ds = datetime.timedelta(seconds=2)
    vl_current_time = curent_time_now()
    data_near_boss = data_store.TimerNotific.get_data_3rb(time_notif)
    try:
        near_notification_time = data_near_boss['time']
        # print(f'near_notification_time_3rb--------------{near_notification_time}')
        # print(f'vl_current_time_3rb-----------------------{vl_current_time}')
        if near_notification_time - t_ds < vl_current_time < near_notification_time + t_ds:  # было == но так лучше
            time_kill = data_near_boss['killtime']
            time_kill = time_kill.replace('.0000000', '')
            time_kill = datetime.datetime.strptime(
                time_kill,
                "%Y-%m-%d %H:%M:%S",
            )
            bos = data_near_boss['bossname']
            wait_time = time_kill + datetime.timedelta(hours=4) - vl_current_time
            for tg_id in data_near_boss['tg_id_list']:
                msg = f'Респ {bos} (3 РБ ЛОА) начнется через {wait_time} на сервере {data_near_boss["server"]}'
                bot.send_message(tg_id, msg)
            sql_methods.delete_notific_time_3rb(data_near_boss['subsid'], data_near_boss['type_notification'])
            sql_methods.deleteNotactivesubsckribe_3rb()  # вот это можно в одну хрень запихать (хранимаю функцию)
            update_cash()
        else:
            if vl_current_time > near_notification_time:
                sql_methods.delete_notific_time_3rb(data_near_boss['subsid'], data_near_boss['type_notification'])
                update_cash()
    except BaseException as error:
        print(error)


def check_status_saite(server_status):
    try:
        saite_request = requests.get("https://asterios.tm")
        if saite_request.ok:
            if not server_status:
                for tg_id in sql_methods.get_all_tg_ids_for_server_stus():
                    msg = "Сайт поднялся, скорее всего поднялся и сам сервер"
                    bot.send_message(tg_id, msg)
                server_status = True
            return server_status

        else:
            if server_status:
                for tg_id in sql_methods.get_all_tg_ids_for_server_stus():
                    msg = "Сайт сервера упал скорее всего и сервер упал, мы предупредим как сервер поднимется"
                    bot.send_message(tg_id, msg)
            server_status = False
            return server_status
    except BaseException as error:
        print(error)
        return server_status


def chec_status_server(servers_status_dict):
    servers_status = data_store.TimerNotific.get_server_status(time_notif)
    for server, status in servers_status.items():
        if status == 'ofline':
            tg_id_list = sql_methods.get_all_users_subrkribe_to_server(server)
            for tg_id in tg_id_list:
                msg = f"Сервер {server} упал"
                bot.send_message(tg_id, msg)
                servers_status_dict[server] = 0
        else:
            try:
                if servers_status_dict[server] == 0:
                    tg_id_list = sql_methods.get_all_users_subrkribe_to_server(server)
                    for tg_id in tg_id_list:
                        msg = f"Сервер {server} поднялся"
                        bot.send_message(tg_id, msg)
                servers_status_dict[server] = 1
            except KeyError:
                servers_status_dict[server] = 1
    return servers_status_dict


def start_update_cash_for_servrs():
    print('start_server_parse')
    while True:
        parse.start_server_parser()
        time.sleep(300)


def start_servrs_status():
    server_status_dict = dict()
    while True:
        server_status_dict = chec_status_server(server_status_dict)
        print(server_status_dict)
        time.sleep(1)


def start_saite_status():
    print("start_saite_status")
    server_status = True
    while True:
        server_status = check_status_saite(server_status)
        time.sleep(300)


def start_not():
    print('start_timer_notif')

    while True:
        if len(data_store.TimerNotific.get_data_notifc(time_notif)) != 0:
            timer_nitification()
        time.sleep(1)


def start_not_3rb():
    print('start_timer_not_3rb')
    while True:
        if len(data_store.TimerNotific.get_data_3rb(time_notif)) != 0:
            timer_nitification_3rb()
        time.sleep(1)


def timer_parse():
    print('start_timer_parse')
    parse.start_parse()
    parse.start_server_parser()
    print('End First Parse')
    timer_s()
    while True:
        waittime = timer_s()
        time.sleep(waittime)
        timer_s()


def bot_start():
    print('bot_start')
    update_cash()
    bot.infinity_polling()


if __name__ == "__main__":
    update_cash()
    timer_parse_thread = Thread(target=timer_parse)
    timer_notification_thread = Thread(target=start_not)
    bot_thread = Thread(target=bot_start)
    timer_notific_3rb_thread = Thread(target=start_not_3rb)
    timer_status_saite_thread = Thread(target=start_saite_status)
    timer_start_servrs_status_thread = Thread(target=start_servrs_status)
    timer_start_update_cash_for_servrs = Thread(target=start_update_cash_for_servrs)
    timer_parse_thread.start()
    time.sleep(60)
    bot_thread.start()
    timer_notification_thread.start()
    timer_notific_3rb_thread.start()
    timer_status_saite_thread.start()
    timer_start_servrs_status_thread.start()
    timer_start_update_cash_for_servrs.start()

# TODO: при инициализации
#  №1 сделать 3 рб в первую очередь!!!
#   жив ли бос ? да жду убийство последнего босса желаете уведомление перед спавном 4
#  №2 оповещение о работоспособности сервера (поднялся, умер)
#  №3 парсить осаду можно только одну дату и сервер и записывать в кеш
#  сделать ТВ тв начинаются за сутки до начала осады тоже в 18:00 ( уточнить мб не в 6)
#  №4 разбить все разделы в пределах 1 файла
#   парсить осаду можно только одну дату и сервер и записывать в кеш узнать как файл разбивать по разделам
#   f11 сделать закладку
#   shift + F11 что бы по ним бегать
#  №5 прикрутить нейросетку
#  №6 datetime не должно писать day/minet
#  №7 сделать логирование
#  №8 запихать в докер и сделать чтоб типо опен сорс
#  №9 сунь дзы искусство войны
#  №10 о семье и частной собственности эенгельсв
#  №11 тамыщев древний
