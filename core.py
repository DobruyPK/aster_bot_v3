import datetime

import enums
import sql_methods
from enums import SubscribeFilds, SubscribeFilds_3rb
import locale

locale.setlocale(locale.LC_TIME, "ru_RU")
S_apic = ['Antharas', 'Valakas']
apic = ['Orfen', 'Beleth', 'Baium', 'Core', 'Queen Ant']
week_day_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
Month_list = ['', 'Января', 'Февраля', 'Марта', 'Апреля', 'Майя', 'Июн', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
              'Ноябрь', 'Декабрь']


def validate_data(unvalid_data):
    print(unvalid_data)
    valid_str = str(unvalid_data).replace(' Boss', '')
    valid_str = valid_str.replace(' was killed', '')
    valid_str = valid_str.replace('Убит босс ', '')
    valid_data = str(valid_str).split(': ')
    print(valid_data)
    valid_data[1] = valid_data[1].replace("'", '')
    valid_data[0] = datetime.datetime.strptime(
        valid_data[0],
        "%Y-%m-%d %H:%M:%S",
    )

    return valid_data


# TODO: ПЕРЕДЕЛАТЬ ЧТОБ ВРЕМЯ РЕСПА В ДНЯХ БРАЛОСЬ ИЗ ЕНУМС
def calc_time_for_boss(boss_name, time):
    if boss_name in enums.BossNames.s_apic():
        if enums.BossNames.s_apic_l()[boss_name] != 0:
            t_d_sup_apic_start_resp = datetime.timedelta(enums.BossNames.s_apic_l()[boss_name][2])
            d_t_resp = time + t_d_sup_apic_start_resp
            start_resp = datetime.datetime(year=d_t_resp.year,
                                           month=d_t_resp.month,
                                           day=d_t_resp.day,
                                           hour=enums.BossNames.apic_drake_l()[boss_name][0],
                                           minute=0,
                                           second=0,
                                           microsecond=0
                                           )
            end_resp = datetime.datetime(year=d_t_resp.year,
                                         month=d_t_resp.month,
                                         day=d_t_resp.day,
                                         hour=enums.BossNames.apic_drake_l()[boss_name][1],
                                         minute=0,
                                         second=0,
                                         microsecond=0
                                         )
            return start_resp, end_resp
    elif boss_name in enums.BossNames.apic():
        if enums.BossNames.apic_l()[boss_name] != 0:
            t_d_sup_apic_start_resp = datetime.timedelta(enums.BossNames.apic_l()[boss_name][2])
            d_t_resp = time + t_d_sup_apic_start_resp
            start_resp = datetime.datetime(year=d_t_resp.year,
                                           month=d_t_resp.month,
                                           day=d_t_resp.day,
                                           hour=enums.BossNames.apic_l()[boss_name][0],
                                           minute=0,
                                           second=0,
                                           microsecond=0
                                           )
            end_resp = datetime.datetime(year=d_t_resp.year,
                                         month=d_t_resp.month,
                                         day=d_t_resp.day,
                                         hour=enums.BossNames.apic_l()[boss_name][1],
                                         minute=0,
                                         second=0,
                                         microsecond=0
                                         )
            return start_resp, end_resp
        else:
            t_d_sup_apic_start_resp = datetime.timedelta(days=5)
            d_t_resp = datetime.timedelta(hours=12)
            start_resp = time + t_d_sup_apic_start_resp - d_t_resp
            end_resp = time + t_d_sup_apic_start_resp + d_t_resp
            return start_resp, end_resp

    else:
        t_d_sup_start_resp = datetime.timedelta(hours=24)
        d_t_resp = datetime.timedelta(hours=6)
        start_resp = time + t_d_sup_start_resp - d_t_resp
        end_resp = time + t_d_sup_start_resp + d_t_resp
        return start_resp, end_resp


def curent_time_now():
    offset = datetime.timezone(datetime.timedelta(hours=3))
    current_time = datetime.datetime.now(offset)
    current_time_vl = datetime.datetime(year=current_time.year,
                                        month=current_time.month,
                                        day=current_time.day,
                                        hour=current_time.hour,
                                        minute=current_time.minute,
                                        second=current_time.second,
                                        )
    return current_time_vl


def nice_data_string(data):
    return data.strftime("%A, %d %b  %H:%M")


def create_message(bossname, server) -> str:
    bos = sql_methods.select_boss(bossname, server)
    bos_name = bos[0]
    bos[1] = bos[1].replace('.0000000', '')
    bos[2] = bos[2].replace('.0000000', '')
    bos[3] = bos[3].replace('.0000000', '')
    killdata = datetime.datetime.strptime(bos[1], "%Y-%m-%d %H:%M:%S")
    startresp = datetime.datetime.strptime(bos[2], "%Y-%m-%d %H:%M:%S")
    endresp = datetime.datetime.strptime(bos[3], "%Y-%m-%d %H:%M:%S")
    now = curent_time_now()
    if startresp < now < endresp:
        waitrespend = endresp - now
        message = (f'''Босс {bos_name} был убит {nice_data_string(killdata)} \n'''
                   f'''Время начала респауна *{nice_data_string(startresp)}* \n'''
                   f'''Респаун уже идет !!! \n'''
                   f'''Максимальное время ожидания респа {waitrespend}''')
    elif now < startresp:
        waitrespstart = startresp - now
        waitrespend = endresp - now
        message = (f'''Босс {bos_name} был убит {nice_data_string(killdata)} \n'''
                   f'''Время начала респауна *{nice_data_string(startresp)}* \n'''
                   f'''До начала респауна осталось {waitrespstart} \n'''
                   f'''Максимальное время ожидания {waitrespend}''')
    else:
        waitboss = now - endresp
        message = (f'''Босс {bos_name} был убит {nice_data_string(killdata)}  \n'''
                   f'''Время начала респауна {startresp} \n'''
                   f'''Респаун кончился, Босс жив в течении {waitboss}....''')
    return message


def find_min_time_for_timer_notification_3rb(mintimetable: list[tuple]):
    res_dict = dict()
    user_id_text = str()
    if len(mintimetable) > 0:
        row = mintimetable[0]
        server = row[SubscribeFilds_3rb.server.value]
        time_5m = row[SubscribeFilds_3rb.not_5m.value]
        time_15m = row[SubscribeFilds_3rb.not_15m.value]
        time_30m = row[SubscribeFilds_3rb.not_30m.value]
        time_1h = row[SubscribeFilds_3rb.not_1h.value]
        bossname = row[SubscribeFilds_3rb.bossname.value]
        killtime = row[SubscribeFilds_3rb.timekill.value]
        times = [time_5m, time_15m, time_30m, time_1h]
        res = min(times).replace('.0000000', '')
        res = datetime.datetime.strptime(res, "%Y-%m-%d %H:%M:%S")
        type_notification = SubscribeFilds_3rb(list(row).index(min(times))).name
        for row in mintimetable:
            userid = row[SubscribeFilds_3rb.userid.value]
            user_id_text = str(str(user_id_text) + ',' + str(userid))
            sub_id = row[SubscribeFilds_3rb.subid.value]
        tg_id_list = sql_methods.get_all_tg_ids(user_id_text)
        res_dict['tg_id_list'] = tg_id_list
        res_dict['time'] = res
        res_dict['bossname'] = bossname
        res_dict['type_notification'] = type_notification
        res_dict['server'] = server
        res_dict['killtime'] = killtime
        res_dict['subsid'] = sub_id
    return res_dict


def find_min_time_for_timer_notification(
        mintimetable: list[tuple]) -> datetime.datetime:  # возврвращает время для таймера
    user_id_text = str()
    res_dict = dict()
    sub_id_text = str()
    if len(mintimetable) > 0:
        row = mintimetable[0]
        server = row[SubscribeFilds.server.value]
        time_5m = row[SubscribeFilds.not_5m.value]
        time_15m = row[SubscribeFilds.not_15m.value]
        time_30m = row[SubscribeFilds.not_30m.value]
        time_1h = row[SubscribeFilds.not_1h.value]
        times = [time_5m, time_15m, time_30m, time_1h]
        res = min(times).replace('.0000000', '')
        type_notification = SubscribeFilds(list(row).index(min(times))).name
        res = datetime.datetime.strptime(res, "%Y-%m-%d %H:%M:%S")
        select_boss = sql_methods.select_near_boss_by_id(row[2])
        bossname = select_boss[0]
        boss_resp_time = select_boss[1]
        for row in mintimetable:
            userid = row[SubscribeFilds.userid.value]
            user_id_text = str(str(user_id_text) + ',' + str(userid))
        for row in mintimetable:
            sub_id = row[SubscribeFilds.subid.value]
            sub_id_text = str(str(sub_id_text) + ',' + str(sub_id))

        tg_id_list = sql_methods.get_all_tg_ids(user_id_text)
        res_dict['tg_id_list'] = tg_id_list
        res_dict['time'] = res
        res_dict['bossname'] = bossname
        res_dict['boss_resp_time'] = boss_resp_time
        res_dict['type_notification'] = type_notification
        res_dict['subsid'] = sub_id_text
        res_dict['server'] = server
    return res_dict


def create_message_castle(castle_info, server) -> str:
    castle_name = castle_info[0]
    castle_siege_time = castle_info[1].replace('.0000000', '')
    castle_siege_time_valid = datetime.datetime.strptime(castle_siege_time, "%Y-%m-%d %H:%M:%S")
    now = curent_time_now()
    if castle_siege_time_valid > now:
        waitsiege = castle_siege_time_valid - now
        message = (f'''Осада Замка {castle_name} \n'''
                   f'''Начнется *{nice_data_string(castle_siege_time_valid)}* \n'''
                   f'''До начала осады осталось {waitsiege} \n''')
    else:
        sige_time = now - castle_siege_time_valid
        message = (f'''Осада Замка {castle_name} уже началась!\n'''
                   f'''Осада длится {sige_time} \n'''
                   f'''Беги форест!!!''')
    return message
