#! /usr/bin/python

import jellyfish # jellyfish requires installation
import os
import sys
import csv
import mysql.connector # mysql requires installation
from mysql.connector import Error
from dotenv import load_dotenv # dotenv requires installation

def get_files(dirpath):
    """
    calculates a list containing all participants files
    :param dirpath: string of a directory containing the participants files
    :return: list of all participants files
    """
    attend_files = []
    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)
        if os.path.isfile(filepath) and "participant-" in file:
            attend_files.append(filepath)

    if len(attend_files) == 0:
        print("This directory has no participant's meetings files!")
        print("please provide a one containing those csv files")
        exit(1)
    return attend_files

def init_sql():
    
    load_dotenv()
    
    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_host = os.getenv("MYSQL_HOST")
    mysql_database = os.getenv("MYSQL_DATABASE")
    
    try: 
        connection = mysql.connector.connect(
            host = mysql_host,
            database = mysql_database,
            user = mysql_user,
            password=mysql_password
        )
        if connection.is_connected():
            print('Connected to database!')
            
    except Error as e:
        print('mysql error:', e)
        try:
            connection.close()
            print('Connection terminated')
        except:
            print('Connection never established')
        return None, None
    
    cursor = connection.cursor()
    
    create_attendance_table = """CREATE TABLE IF NOT EXISTS attendance(
        room_name varchar(50) NOT NULL,
        room_start varchar(30) NOT NULL,
        room_finish varchar(30) NOT NULL,
        name varchar(20) NOT NULL,
        email varchar(30) NOT NULL,
        time varchar(200) NOT NULL,
        overall_time varchar(30) NOT NULL,
        platform varchar(30) NOT NULL,
        PRIMARY KEY(room_name, room_start, email)
    )"""
    
    cursor.execute(create_attendance_table)
    
    return connection, cursor

def get_data(csvread, cursor):
    # csv columns headers columns:
    ROOM_NAME = "Meeting Name"
    ROOM_START = "Meeting Start Time"
    ROOM_FINISH = "Meeting End Time"
    JOIN_TIME = "Join Time"
    LEAVE_TIME = "Leave Time"
    OVERALL_TIME = "Attendance Duration"
    
    with open(csvread, newline='', encoding="utf-16LE") as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")
                  
        mysql_Create_Table = """ CREATE TABLE temp (
                room_name varchar(50) NOT NULL,
                room_start varchar(30) NOT NULL,
                room_finish varchar(30) NOT NULL,
                name varchar(20) NOT NULL,
                email varchar(30) NOT NULL,
                join_time varchar(30) NOT NULL,
                leave_time varchar(30) NOT NULL,
                overall_time varchar(30) NOT NULL,
                platform varchar(30) NOT NULL  
        ) """
        
        cursor.execute(" DROP TABLE IF EXISTS temp; ") 
        cursor.execute(mysql_Create_Table)
        
        mysql_Insert_To_Table = """ INSERT INTO temp (
                room_name,
                room_start,
                room_finish,
                name,
                email,
                join_time,
                leave_time,
                overall_time,
                platform) VALUES (
                %(Meeting Name)s,
                %(Meeting Start Time)s,
                %(Meeting End Time)s,
                %(Name)s,
                %(Attendee Email)s,
                %(Join Time)s,
                %(Leave Time)s,
                %(Attendance Duration)s,
                %(Connection Type)s
            ) """
        
        for row in reader:
            row[ROOM_START] = row[ROOM_START].replace('=','').replace('"','')
            row[ROOM_FINISH] = row[ROOM_FINISH].replace('=','').replace('"','')
            row[JOIN_TIME] = row[JOIN_TIME].replace('=','').replace('"','')
            row[LEAVE_TIME] = row[LEAVE_TIME].replace('=','').replace('"','')
            row[OVERALL_TIME] = row[OVERALL_TIME].replace(' mins', '')
            row[ROOM_NAME] = row['\ufeffMeeting Name']
            del row['\ufeffMeeting Name']
            
            cursor.execute(mysql_Insert_To_Table, row)
        
    selectFromQuery = """ SELECT * FROM temp ORDER BY join_time ASC LIMIT 1 """
    cursor.execute(selectFromQuery)
    res = cursor.fetchone()
    earliest = res[5].rsplit(' ')[1]
    earliest_hour = int(earliest.rsplit(':')[0])
    earliest_min = int(earliest.rsplit(':')[1])
    selectFromQuery = """ SELECT * FROM temp ORDER BY leave_time DESC LIMIT 1 """
    cursor.execute(selectFromQuery)
    res = cursor.fetchone()
    latest = res[6].rsplit(' ')[1]
    latest_hour = int(latest.rsplit(':')[0])
    latest_min = int(latest.rsplit(':')[1])
    max_overall = (latest_hour - earliest_hour) * 60 + (latest_min-earliest_min)
    
    return max_overall

def check_spell(username, time_dict):
    for user in time_dict.keys():
        if jellyfish.damerau_levenshtein_distance(user, username) < 3:
            return user
    return

def get_time(join, leave):
    
    time = join.rsplit(' ')[1] + ' - ' + leave.rsplit(' ')[1]
    
    return time

def platform_updater(userPlatform, platform):
    
    if userPlatform == '':
        return platform
    elif userPlatform != platform:
        return 'mixed'
    else:
        return userPlatform

def time_updater(timeArray):
    
    if len(timeArray) < 2: return
    
    i = 0
    while i + 1 < len(timeArray):
        start = timeArray[i].rsplit(' - ')[0]  # take first login time
        end = timeArray[i].rsplit(' - ')[1]  # take first logout time
        start1 = timeArray[i + 1].rsplit(' - ')[0]  # take second login time
        end1 = timeArray[i + 1].rsplit(' - ')[1]  # take second logout time
        if end >= end1:  # it means, that user was logged in from several devices
            del (timeArray[i + 1])
        elif start1 <= end <= end1:  # if the logged time frames overlap then take the longest frame
            timeArray[i] = start + " - " + end1
            del (timeArray[i + 1])
        else:
            i += 1
        
    overall = 0
    for frame in timeArray:
        sh = int(frame.rsplit(":")[0])  # starting hour
        sm = int(frame.rsplit(":")[1])  # starting minute
        eh = int(frame.rsplit(":")[2].rsplit("- ")[1])  # ending hour
        em = int(frame.rsplit(":")[3])  # ending minute

        overall += (eh - sh) * 60 + (em - sm)
            
    return overall
        


def sql_arrange(time_dict, cursor, max_time):
    ROOM_NAME = 0
    ROOM_START = 1
    ROOM_FINISH = 2
    NAME = 3
    EMAIL = 4
    JOIN_TIME = 5
    LEAVE_TIME = 6
    OVERALL_TIME = 7
    PLATFORM = 8
    
    cursor.execute(" SELECT * FROM temp ORDER BY join_time ASC; ")
    tempList = cursor.fetchall()
    
    for line in tempList:
        
        if "bynet" in line[EMAIL] or "8200" in line[EMAIL] or "nan" in line[EMAIL] or '' == line[EMAIL]: 
            continue
        username = line[EMAIL].rsplit('@')[0]
        fix =  check_spell(username, time_dict)
        if not fix:
            time_dict[username] = {
                'room': line[ROOM_NAME],
                'room start': line[ROOM_START],
                'room finish': line[ROOM_FINISH],
                'name': line[NAME],
                'email': line[EMAIL],
                'time': [],
                'time string': '',
                'overall time': line[OVERALL_TIME],
                'platform': ''
            }
        else:
            username = fix
        
        time = get_time(line[JOIN_TIME], line[LEAVE_TIME])
        time_dict[username]['time'].append(time)
        time_dict[username]['platform'] = platform_updater(time_dict[username]['platform'], line[PLATFORM])
        
    for user in time_dict.keys():
        if len(time_dict[user]['time']) > 1:
            time_dict[user]['overall time'] =  time_updater(time_dict[user]['time'])
            if time_dict[user]['overall time'] > max_time:
                time_dict[user]['overall time'] = max_time
        
        time_dict[user]['time string'] = ', '.join(time_dict[user]['time'])
        del time_dict[user]['time']

def print_time_dict(time_dict):
    for user in time_dict.keys():
        print(time_dict[user])            
    
def insert_dict(time_dict, cursor, connection): 
    for user in time_dict.keys():
        
        insertOrUpdateQuery = """
            INSERT INTO attendance (
                room_name,
                room_start,
                room_finish,
                name,
                email,
                time,
                overall_time,
                platform
            ) VALUES (
                %(room)s,
                %(room start)s,
                %(room finish)s,
                %(name)s,
                %(email)s,
                %(time string)s,
                %(overall time)s,
                %(platform)s
            ) ON DUPLICATE KEY UPDATE
                name = %(name)s,
                time = %(time string)s,
                overall_time = %(overall time)s,
                platform = %(platform)s
        """
        
        cursor.execute(insertOrUpdateQuery, time_dict[user])
    
    connection.commit()
        
def print_full_attendance(cursor):
    cursor.execute(" SELECT * FROM attendance; ")
    res = cursor.fetchall()
    print(res)

def disable_connection(connection, cursor):
    cursor.close()
    connection.close()
    return 0

def sum_of_days(cursor):
    cursor.execute(" SELECT DISTINCT room_start,room_finish FROM attendance ORDER BY room_start; ")
    days = cursor.fetchall()
    sum_days = 0
    
    for day in days:
        start_hours = int(day[0].rsplit(" ")[1].rsplit(":")[0])
        start_minutes = int(day[0].rsplit(" ")[1].rsplit(":")[1])
        end_hours = int(day[1].rsplit(" ")[1].rsplit(":")[0])
        end_minutes = int(day[1].rsplit(" ")[1].rsplit(":")[1])
        sum_days += (end_hours - start_hours)*60 + end_minutes - start_minutes
    return sum_days

def get_average_specific(cursor, text_input):
    sum_user = 0
    cursor.execute(f" SELECT overall_time FROM attendance WHERE email = '{text_input}'; ")
    res = cursor.fetchall()
    
    for i in res:
        sum_user += int(i[0])
    
    sum_all_days = sum_of_days(cursor)
    return (sum_user/sum_all_days)*100

def get_average_dynamic(cursor, text_input):
    sum_user = 0
    cursor.execute(" SELECT email,overall_time FROM attendance; ")
    res = cursor.fetchall()
    
    for i in res:
        if jellyfish.damerau_levenshtein_distance(text_input, i[0]) < 3:
            sum_user += int(i[1])
    
    sum_all_days = sum_of_days(cursor)
    return (sum_user/sum_all_days)*100

def get_table(cursor, categories):
    cursor.execute(f" SELECT {categories} FROM attendance; ")
    return cursor.fetchall()

def get_table_specifics(cursor, categories, input_type, input_text):
    cursor.execute(f" SELECT {categories} FROM attendance WHERE {input_type} = '{input_text}'; ")
    return cursor.fetchall()

def get_table_dynamic(cursor, categories, input_type, input_text):
    cursor.execute(f" SELECT {categories} FROM attendance; ")
    res = cursor.fetchall()
    cursor.execute(f" SELECT {input_type} FROM attendance ")
    search_by = cursor.fetchall()
    i = 0
    for search_result in search_by:
        if not (jellyfish.damerau_levenshtein_distance(search_result[0], input_text) < 3):
            del res[i]
        else:
            i += 1
    
    return res
    

def post_csv(dirpath):
    """
    initiates all parameters that are needed for the script: the dictionary of the participants, list of csv files
    and the initiative pd.DataFrame
    :return: pd.DataFrame, list of csv files and the dictionary of the participants
    """
    
    """
    helpful functions can be used to debug: print_full_attendance(cursor), print_time_dict(time_dict), get_table(cursor)
    """
    csv_lst = get_files(dirpath)
    connection, cursor = init_sql()
    if connection == None: return "Bad connection to database"
    for i in range(len(csv_lst)):
        time_dict = {}
        max_overall = get_data(csv_lst[i], cursor)
        sql_arrange(time_dict, cursor, max_overall)
        insert_dict(time_dict, cursor, connection)
    disable_connection(connection, cursor)
    return "good connection"

def post_api(dir):
    if not os.path.isdir(dir):
        return 'Not a Directory!'
    check_connection = post_csv(dir)
    if check_connection == "Bad connection to database": return check_connection
    return 'Done!'

def get_api(categories):
    connection, cursor = init_sql()
    if connection == None: return "Bad connection to database"
    try:
        results = get_table(cursor, categories)
    except:
        results = 'problem with request'
    finally:
        disable_connection(connection, cursor)
        return results
    
def get_specific_api(categories, input_type, input_text, dynamic):
    connection, cursor = init_sql()
    if connection == None: return "Bad connection to database"
    try:
        if dynamic: results = get_table_dynamic(cursor, categories, input_type, input_text)
        else: results = get_table_specifics(cursor, categories, input_type, input_text)
    except:
        results = 'problem with request'
    finally:
        disable_connection(connection, cursor)
        return results

def get_avg_api(input_text, dynamic):
    connection, cursor = init_sql()
    if connection == None: return "Bad connection to database"
    try:
        if dynamic: results = get_average_dynamic(cursor, input_text)
        else: results = get_average_specific(cursor, input_text)
    except:
        results = 'problem with request'
    finally:
        disable_connection(connection, cursor)
        return results

