import datetime
import os.path
import os
from dotenv import load_dotenv
import pyodbc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "AsterBotDB")
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


def create_connection():
    conn_str = (
        fr'DRIVER={os.environ.get("DRIVER")};'
        fr'SERVER={os.environ.get("SERVER")};'
        fr'DATABASE={os.environ.get("DATABASE")};'
        fr'UID={os.environ.get("UID")};'
        fr'PWD={os.environ.get("PWD")};'
        fr'Trusted_Connection=No;'
    )
    conn = pyodbc.connect(conn_str)
    return conn


def create_boss(killdatetime, bossname, bosstype, startresp, endresp, server):
    sqlite_connection = create_connection()
    cursor = sqlite_connection.cursor()
    sql_querry = f'''EXEC dbo.create_boss @bossname='{bossname}', @killdatettime='{killdatetime}', 
                     @bosstype='{bosstype}', @startresp='{startresp}', @endresp='{endresp}', @server= '{server}';'''
    cursor.execute(sql_querry)
    cursor.commit()
    cursor.close()


def update_boss(killdatetime, bossname, startresp, endresp, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.update_boss @bossname='{bossname}', @killdatettime='{killdatetime}', 
                     @startresp='{startresp}', @endresp='{endresp}', @server = '{server}';'''
        cursor.execute(sql_querry)

        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def select_boss(bossname, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.select_boss @bossname='{bossname}', @server='{server}';'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def select_boss_type(bosstype, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.select_boss_type @bosstypee='{bosstype}', @server ='{server}';'''
        cursor.execute(sql_querry)
        result = cursor.fetchall()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# вроде как тут нам плевать на серв ведь это для таймера
def select_near_boss():
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.select_near_boss;'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def create_subscribe(tg_id, bossname, subsckribe_tybe, not_time, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.create_subscribe @tg_id = {tg_id},
                        @bossname='{bossname}', @subsckribe_tybe ='{subsckribe_tybe}',
                        @not_time='{not_time}', @server = '{server}' ;'''
        cursor.execute(sql_querry)
        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# вроде как тут нам плевать на серв ведь это для поиска подписок
def create_user(telegram_id, username):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.create_user @telegram_id = {telegram_id}, @username='{username}' ;'''
        cursor.execute(sql_querry)
        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_user(telegram_id):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_user @telegram_id = {telegram_id};'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_all_boss_names(server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_all_boss_names @server = '{server}';'''
        cursor.execute(sql_querry)
        result = list()
        for boss in cursor.fetchall():
            result.append(boss[0])
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_subscribe(tg_id, bossname, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_subscribe @tg_id={tg_id}, @bossname='{bossname}', @server = '{server}';'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_subscribe(tg_id, bossname, subsckribe_tybe, not_time, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        if not_time == 'Null':
            sql_querry = f'''EXEC dbo.update_subscribe @tg_id = {tg_id}, @bossname ='{bossname}',
                    @subsckribe_tybe = '{subsckribe_tybe}', @not_time = {not_time}, @server = '{server}';'''
        else:
            sql_querry = f'''EXEC dbo.update_subscribe @tg_id = {tg_id}, @bossname ='{bossname}',
                        @subsckribe_tybe = '{subsckribe_tybe}', @not_time = '{not_time}', @server = '{server}' ;'''
        cursor.execute(sql_querry)
        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_all_user_id():
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_subscribe ;'''
        cursor.execute(sql_querry)
        result = dict()
        for user in cursor.fetchall():
            result[str(user[0])] = user[1]
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def all_get_subscribe():
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.all_get_subscribe ;'''
        cursor.execute(sql_querry)
        result = cursor.call()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_all_boss():
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_all_boss ;'''
        cursor.execute(sql_querry)
        result = cursor.fetchall()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def getnearestsub():
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''set nocount on; EXEC dbo.GetNearestSub;'''
        cursor.execute(sql_querry)
        result = cursor.fetchall()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_all_tg_ids(ids_text):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''set nocount on; EXEC dbo.get_all_tg_ids @List = '{ids_text}';'''
        cursor.execute(sql_querry)
        result1 = cursor.fetchall()
        result = list()
        for x in result1:
            result.append(x[0])
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def select_near_boss_by_id(bosid: int):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.select_near_boss_by_id @bosid ={bosid};'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def delete_notific_time(ids: list(), substype: str()):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.delete_notific_time @sids='{ids}', @subsckribe_tybe='{substype}';'''
        cursor.execute(sql_querry)

        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def deleteNotactivesubsckribe():
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.deleteNotactivesubsckribe;'''
        cursor.execute(sql_querry)

        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def create_fort(name, waittime, server):
    sqlite_connection = create_connection()
    cursor = sqlite_connection.cursor()
    sql_querry = f'''EXEC dbo.create_fort @name='{name}', @waittime='{waittime}', 
                     @server='{server}';'''
    cursor.execute(sql_querry)
    cursor.commit()
    cursor.close()


def create_castl(name, waittime, server):
    sqlite_connection = create_connection()
    cursor = sqlite_connection.cursor()
    sql_querry = f'''EXEC dbo.create_castl @name='{name}', @waittime='{waittime}', 
                     @server='{server}';'''
    cursor.execute(sql_querry)
    cursor.commit()
    cursor.close()


def get_all_castless(name):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_all_castless @name = '{name}';'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_castle_time(name, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_castle_time @name = '{name}', @server = {server};'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_Castle(name, time, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.update_Castle @name='{name}', @time='{time}', 
                     @server='{server}';'''
        cursor.execute(sql_querry)

        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_fort_time(name, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_fort_time @name = '{name}', @server = '{server}';'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_fort_time(name, time, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.update_fort @name = '{name}', @time='{time}', @server='{server}';'''
        cursor.execute(sql_querry)

        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_all_castle_name_by_server(server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_all_castle_name_by_server @server = '{server}';'''
        cursor.execute(sql_querry)
        result = list()
        for castle_name in cursor.fetchall():
            result.append(castle_name[0])
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_all_fort_name_by_server(server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_all_fort_name_by_server @server = '{server}';'''
        cursor.execute(sql_querry)
        result = list()
        for fort_name in cursor.fetchall():
            result.append(fort_name[0])
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def select_castles(catlename, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.select_castle @castelname='{catlename}', @server='{server}';'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_subscribe_3rb(tg_id, bossname, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_subskribe_3rb @tg_id={tg_id}, @bossname='{bossname}', @server = '{server}';'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def create_subscribe_3rb(tg_id, bossname, subsckribe_tybe, not_time, server, time_kill):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.create_subscribe_3rb @tg_id = {tg_id},
                        @bossname='{bossname}', @subsckribe_tybe ='{subsckribe_tybe}',
                        @not_time='{not_time}', @server = '{server}', @timekill = '{time_kill}' ;'''
        cursor.execute(sql_querry)
        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_subscribe_3rb(tg_id, bossname, subsckribe_tybe, not_time, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        if not_time == 'Null':
            sql_querry = f'''EXEC dbo.update_subscribe_3rb @tg_id = {tg_id}, @bossname ='{bossname}',
                             @subsckribe_tybe = '{subsckribe_tybe}', @not_time = {not_time}, @server = '{server}';'''
        else:
            sql_querry = f'''EXEC dbo.update_subscribe_3rb @tg_id = {tg_id}, @bossname ='{bossname}',
                             @subsckribe_tybe = '{subsckribe_tybe}', @not_time = '{not_time}', @server = '{server}' ;'''
        cursor.execute(sql_querry)
        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def deleteNotactivesubsckribe_3rb():
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.deleteNotactivesubsckribe_3rb;'''
        cursor.execute(sql_querry)

        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def GetNearestSub_3rb():
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''set nocount on; EXEC dbo.GetNearestSub_3rb;'''
        cursor.execute(sql_querry)
        result = cursor.fetchall()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def delete_notific_time_3rb(ids: list(), substype: str()):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.delete_notific_time_3rb @sids='{ids}', @subsckribe_tybe='{substype}';'''
        cursor.execute(sql_querry)

        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_all_tg_ids_for_server_stus():
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_all_tg_ids_for_server_stus;'''
        cursor.execute(sql_querry)
        result = list()
        for boss in cursor.fetchall():
            result.append(boss[0])
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_subsckribe_server_status(tg_id, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_subsckribe_server_status @tg_id={tg_id}, @server = '{server}';'''
        cursor.execute(sql_querry)
        result = cursor.fetchone()
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def create_subsckribe_server_status(userid, server):
    sqlite_connection = create_connection()
    cursor = sqlite_connection.cursor()
    sql_querry = f'''EXEC dbo.create_subsckribe_server_status @userid='{userid}', @server='{server}';'''
    cursor.execute(sql_querry)
    cursor.commit()
    cursor.close()


def create_subsckribe_server_status(tg_id, server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.create_subsckribe_server_status @tg_id = {tg_id}, @server = '{server}';'''
        cursor.execute(sql_querry)
        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def delete_subsckribe_server_status(tg_id, servername):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.delete_subsckribe_server_status @tg_id = {tg_id}, @server = {servername} ;'''
        cursor.execute(sql_querry)

        sqlite_connection.commit()
        cursor.close()
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_all_users_subrkribe_to_server(server):
    try:
        sqlite_connection = create_connection()
        cursor = sqlite_connection.cursor()
        sql_querry = f'''EXEC dbo.get_all_users_subrkribe_to_server @server = '{server}';'''
        cursor.execute(sql_querry)
        result = list()
        for boss in cursor.fetchall():
            result.append(boss[0])
        cursor.close()
        return result
    except pyodbc.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
