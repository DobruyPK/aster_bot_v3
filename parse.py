import datetime
import time
from html.parser import HTMLParser
import re
import requests

import core
import data_store
import enums
import sql_methods

timenotifserverstatus = data_store.TimerNotific()


class DatasaverFortnesCastleBoss:
    _instances = {}
    _target_tag = str()
    _data_fort_str = str()
    _data_castl_str = str()
    _castle_dict = dict()
    _data = dict()
    _bosslist = dict()
    _selectedbos = dict()

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def update_tag(self, tag):
        self._target_tag = tag

    def get_target_tag(self):
        return self._target_tag

    def get_data_fort_str(self):
        return self._data_fort_str

    def set_data_fort_str(self, datastr):
        self._data_fort_str = datastr

    def set_data_castle_str(self, datastr):
        self._data_castl_str = datastr

    def get_data_castle_str(self):
        return self._data_castl_str

    def apdate_boss_list(self, boslist, server):
        self._bosslist[server] = boslist

    def get_bosslist(self, server):
        return self._bosslist[server]

    def set_selctboss(self, bossname, server):
        self._selectedbos[server] = bossname

    def apdate_castle_dict(self, castle_list, server):
        self._castle_dict[server] = castle_list

    def get_castle_dict(self, server):
        return self._castle_dict[server]


data_fortness = DatasaverFortnesCastleBoss()


def update_data_castle(data_row, server):
    if data_row in enums.Castle.allcastllit.value:
        DatasaverFortnesCastleBoss.set_data_castle_str(data_fortness, data_row)
    else:
        valid_str = re.search(r"(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})",
                              data_row)
        if valid_str is not None:
            data_str = DatasaverFortnesCastleBoss.get_data_castle_str(data_fortness)
            data_str = data_str + ',' + data_row
            valid_data = data_str.split(',')
            valid_data[1] = datetime.datetime.strptime(valid_data[1], "%Y-%m-%d %H:%M:%S")
            try:
                old_data_castle = sql_methods.get_castle_time(valid_data[0], server)
                old_time = datetime.datetime.strptime(old_data_castle.replace('.0000000', ''), "%Y-%m-%d %H:%M:%S")
                if valid_data[1] > old_time and valid_data[1] is not None:
                    sql_methods.update_Castle(valid_data[0], valid_data[1], server)
                if valid_data[1] is None:
                    sql_methods.create_castl(valid_data[0], valid_data[1], server)
                DatasaverFortnesCastleBoss.set_data_castle_str(data_fortness, '')
            except:
                sql_methods.create_castl(valid_data[0], valid_data[1], server)
                DatasaverFortnesCastleBoss.set_data_castle_str(data_fortness, '')


def update_data_fortness(data_row, server):
    if data_row in enums.Forts.allfortslist.value:
        DatasaverFortnesCastleBoss.set_data_fort_str(data_fortness, data_row)
    else:
        if 'часов' in data_row:
            data_str = DatasaverFortnesCastleBoss.get_data_fort_str(data_fortness)
            data_str = data_str + ',' + data_row.replace(' часов', '')
            valid_data = data_str.split(',')
            try:
                old_time = sql_methods.get_fort_time(valid_data[0], server)
                if old_time is None:
                    sql_methods.create_fort(valid_data[0], valid_data[1], server)
                elif old_time != int(valid_data[1]):
                    sql_methods.update_fort_time(valid_data[0], valid_data[1], server)
                DatasaverFortnesCastleBoss.set_data_fort_str(data_fortness, '')
            except:
                sql_methods.create_fort(valid_data[0], valid_data[1], server)


def update_data_boss(data_r, server):
    if 'Boss' in str(data_r) or 'Убит босс' in str(data_r):
        valid_data = core.validate_data(data_r)
        bosstype = 0
        if valid_data[1] in enums.BossNames.s_apic():
            bosstype = 2
        elif valid_data[1] in enums.BossNames.apic():
            bosstype = 1
        s_e_resp = core.calc_time_for_boss(valid_data[1], valid_data[0])
        boss = sql_methods.select_boss(valid_data[1], server)
        if boss is not None:
            boss[1] = boss[1].replace('.0000000', '')
            time = datetime.datetime.strptime(boss[1], "%Y-%m-%d %H:%M:%S")
            if time < valid_data[0]:
                sql_methods.update_boss(valid_data[0], valid_data[1], s_e_resp[0], s_e_resp[1], server)
        else:
            sql_methods.create_boss(valid_data[0], valid_data[1], bosstype, s_e_resp[0], s_e_resp[1], server)


def update_server_status(data_row, server_nimber):
    res_dict = data_store.TimerNotific.get_server_status(timenotifserverstatus)
    res_dict[enums.ServersStatus.server_list.value[server_nimber]] = data_row
    data_store.TimerNotific.update_server_status(timenotifserverstatus, res_dict)


# parser
class FortnessCastleHTMLParser(HTMLParser):
    type_info = ''
    server = str()

    def handle_starttag(self, tag, attrs):
        DatasaverFortnesCastleBoss.update_tag(data_fortness, tag)

    def handle_data(self, data):
        if self.type_info == "Boss":
            if DatasaverFortnesCastleBoss.get_target_tag(data_fortness) == 'a':
                update_data_boss(data, self.server)
        elif self.type_info == "Fort":
            if DatasaverFortnesCastleBoss.get_target_tag(
                    data_fortness) == 'b' or DatasaverFortnesCastleBoss.get_target_tag(
                    data_fortness) == 'td':
                update_data_fortness(data, self.server)
        else:
            if DatasaverFortnesCastleBoss.get_target_tag(
                    data_fortness) == 'b' or DatasaverFortnesCastleBoss.get_target_tag(
                    data_fortness) == 'td':
                update_data_castle(data, self.server)


class Serverparser(HTMLParser):
    server_int = 0

    def handle_starttag(self, tag, attrs):
        DatasaverFortnesCastleBoss.update_tag(data_fortness, tag)

    def handle_data(self, data):
        if DatasaverFortnesCastleBoss.get_target_tag(data_fortness) == 'font':
            update_server_status(data, self.server_int)
            self.server_int = self.server_int + 1


# TODO получить все внутри тега center как текст и запихать это обратно в парсер

def start_server_parser():
    parser = Serverparser()
    saite_request = requests.get(enums.ServersStatus.url_status.value)
    parser.feed(saite_request.text)


def start_parse():
    parser = FortnessCastleHTMLParser()
    for item_server in enums.ParseURL:
        parser.server = item_server.name
        for typeurl, url in item_server.value.items():
            parser.type_info = typeurl
            saite_request = requests.get(url)
            parser.feed(saite_request.text)
            parser.type_info = ''


# print(data_store.TimerNotific.get_server_status(timenotifserverstatus))
# parse.start_parse(item.value, item.name)
# saite_request = requests.get(url)
# parser = FortnessCastleHTMLParser()
# parser.type_info = typeurl
# parser.feed(saite_request.text)

# -----------------------
#
# from html.parser import HTMLParser
#
# import requests
#
# from data_store import DatasaverBoss, update_data_boss
#
# data_l = DatasaverBoss()
#
#
# class BossHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         DatasaverBoss.update_tag(data_l, tag)
#
#     def handle_data(self, data):
#         if DatasaverBoss.get_target_tag(data_l) == 'a':
#             update_data_boss(data)
#
#
# def start_parse():
#     url = 'https://asterios.tm/index.php?cmd=rss&serv=3&filter=all'
#     saite_request = requests.get(url)
#     parser = BossHTMLParser()
#     parser.feed(saite_request.text)
