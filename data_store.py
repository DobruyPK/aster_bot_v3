# import datetime
#
# import core
# import enums
# import sql_methods
#
#
# def update_data_boss(data_r):
#     if 'Boss' in str(data_r):
#         valid_data = core.validate_data(data_r)
#         bosstype = 0
#         if valid_data[1] in enums.BossNames.s_apic():
#             bosstype = 2
#         elif valid_data[1] in enums.BossNames.apic():
#             bosstype = 1
#         s_e_resp = core.calc_time_for_boss(valid_data[1], valid_data[0])
#         boss = sql_methods.select_boss(valid_data[1])
#         if boss is not None:
#             boss[1] = boss[1].replace('.0000000', '')
#             time = datetime.datetime.strptime(boss[1], "%Y-%m-%d %H:%M:%S")
#             if time < valid_data[0]:
#                 sql_methods.update_boss(valid_data[0], valid_data[1], s_e_resp[0], s_e_resp[1])
#         else:
#             sql_methods.create_boss(valid_data[0], valid_data[1], bosstype, s_e_resp[0], s_e_resp[1])
#
#
# class DatasaverBoss:
#     _instances = {}
#     _target_tag = str()
#     _data = dict()
#     _bosslist = list()
#     _selectedbos = ''
#
#     def __new__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             instance = super().__new__(cls)
#             cls._instances[cls] = instance
#         return cls._instances[cls]
#
#     def update_tag(self, tag):
#         self._target_tag = tag
#
#     def get_target_tag(self):
#         return self._target_tag
#
#     def apdate_boss_list(self, boslist):
#         self._bosslist = boslist
#
#     def get_bosslist(self):
#         return self._bosslist
#
#     def get_selctboss(self):
#         return self._selectedbos
#
#     def set_selctboss(self, bossname):
#         self._selectedbos = bossname


class TimerNotific:
    _instances = {}
    _data_notifc = dict()
    _data_3rb_notif = dict()
    _data_server_status = dict()

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def get_data_notifc(self):
        return self._data_notifc

    def set_data_notifc(self, data):
        self._data_notifc = data

    def update_data_3rb(self, data):
        self._data_3rb_notif = data

    def get_data_3rb(self):
        return self._data_3rb_notif

    def update_server_status(self, data):
        self._data_server_status = data

    def get_server_status(self):
        return self._data_server_status
