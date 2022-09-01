# import core
# import data_store
# import sql_methods
# from bot import time_notif
#
# timerinfo_3rb = sql_methods.GetNearestSub_3rb()
# x = data_store.TimerNotific.update_data_3rb(time_notif,
#                                         core.find_min_time_for_timer_notification_3rb(timerinfo_3rb))
# print(x)
#
# timerinfo = sql_methods.getnearestsub()
# z = data_store.TimerNotific.set_data_notifc(time_notif,
#                                         core.find_min_time_for_timer_notification(timerinfo))
# print(z)
from datetime import datetime

import requests
#
# from bot import start_not, start_not_3rb
import parse
from parse import start_parse
from sql_methods import get_all_tg_ids_for_server_stus, get_all_users_subrkribe_to_server

# saite_request = requests.get("https://asterios.tm")
# if saite_request.ok:
#     print ('OK!')
# else:
#     print ('Boo!')

import datetime
now = datetime.datetime.now()
print(now.month)