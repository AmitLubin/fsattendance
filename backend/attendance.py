#!/usr/bin/python3

import jellyfish
import os
import csv
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

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
    """ 
    establishes the connection to mysql database and initiates an attendance table
    :return: the connection to the database, 
                the cursor of the database and whether an error has occured or not
    """
    # loading the environment variables from the env-file:
    load_dotenv()
    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_host = os.getenv("MYSQL_HOST")
    mysql_database = os.getenv("MYSQL_DATABASE")
    # connecting to mysql:
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
        return None, None, True
    
    # after connection is established, creating table:
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
    
    return connection, cursor, False

def get_data(csvread, cursor):
    """
    inserts the data of a csv file into a new mysql table and calculates
    the maximal overall time one could have in the meeting
    :param csvread: a path to a csv file
    :param cursor: a cursor of a mysql database
    :return: the maximal overall time one participant could have in the csv file 
    """
    # csv header columns:
    ROOM_NAME = "Meeting Name"
    ROOM_START = "Meeting Start Time"
    ROOM_FINISH = "Meeting End Time"
    JOIN_TIME = "Join Time"
    LEAVE_TIME = "Leave Time"
    OVERALL_TIME = "Attendance Duration"
    # reading the csv file:
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

        # creating the query format before executing it:
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
        # executing the insert query, row by row from the csv file:
        for row in reader:
            # trimming the values from the csv-reader
            row[ROOM_START] = row[ROOM_START].replace('=','').replace('"','')
            row[ROOM_FINISH] = row[ROOM_FINISH].replace('=','').replace('"','')
            row[JOIN_TIME] = row[JOIN_TIME].replace('=','').replace('"','')
            row[LEAVE_TIME] = row[LEAVE_TIME].replace('=','').replace('"','')
            row[OVERALL_TIME] = row[OVERALL_TIME].replace(' mins', '')
            row[ROOM_NAME] = row['\ufeffMeeting Name']
            del row['\ufeffMeeting Name']
            
            cursor.execute(mysql_Insert_To_Table, row)
    # calculating the maximal overall time one could have inside the csv file:
    # fetching the earliest join time by sorting the join-time column in 
    # ascending order and taking the first value    
    selectFromQuery = """ SELECT join_time FROM temp ORDER BY join_time ASC LIMIT 1 """
    cursor.execute(selectFromQuery)
    res = cursor.fetchone()
    earliest = res[0].rsplit(' ')[1]   # taking the string that comes after the date
    # taking the string that comes before the ':' (hours) and converting it to integer
    earliest_hour = int(earliest.rsplit(':')[0])
    # taking the string that comes after the ':' (minutes) and converting it to integer
    earliest_min = int(earliest.rsplit(':')[1])
    # fetching the latest leave time by sorting the leave-time column in 
    # descending order and taking the first value
    selectFromQuery = """ SELECT leave_time FROM temp ORDER BY leave_time DESC LIMIT 1 """
    cursor.execute(selectFromQuery)
    res = cursor.fetchone()
    latest = res[0].rsplit(' ')[1] # taking the string that comes after the date
    # taking the string that comes before the ':' (hours) and converting it to integer
    latest_hour = int(latest.rsplit(':')[0])
    # taking the string that comes after the ':' (minutes) and converting it to integer
    latest_min = int(latest.rsplit(':')[1])
    max_overall = (latest_hour - earliest_hour) * 60 + (latest_min - earliest_min)
    
    return max_overall

def check_spell(username, time_dict):
    """
    checks for typos of a given username by calculating its distance from 
    an existing username in a dictionary
    :param username: a given username that might be having typos
    :param time_dict: a dictionary holding the login times of each participant
    :return: a corrected username if typos were exposed or none otherwise
    """
    for user in time_dict.keys():
        # checking if up to 2 typos occured:
        if jellyfish.damerau_levenshtein_distance(user, username) <3:
            return user
    return

def get_time(join, leave):
    """
    gets a join timestamp and a leave timestamp and joins the times together into one timeframe,
    discarding the dates
    :param join: a string of join date and time
    :param leave: a string  of leave date and time
    :return: a string of timeframe in the following format: "join_time - leave_time"
    """
    time = join.rsplit(' ')[1] + ' - ' + leave.rsplit(' ')[1]
    
    return time

def platform_updater(userPlatform, platform):
    """
    gets two platform strings from two different logins of one user and compares between them.
    if the user logged in from two different platforms, it returns the string 'mixed',
    otherwise, return the most accurate one
    :param userPlatform: a string of a login platform
    :param platform: a string of a login platform
    :return: a string 'mixed' if the arguments differ, or the most accurate string otherwise
    """
    if userPlatform == '':
        return platform
    elif userPlatform != platform:
        return 'mixed'
    else:
        return userPlatform

def time_updater(time_lst):
    """
    calculates the overall login-time of one user in a meeting based on a list containing
    all the login timeframes of the user.
    :param time_lst: list of at least 2 login timeframes of a user, sorted from earliest to latest
    :return: the overall minutes a user was logged-in to the meeting
    """
    # if the user has only one log-in timeframe then no need to calculate anything
    #if len(time_lst) < 2: return 
    
    i = 0
    while i + 1 < len(time_lst):
        start = time_lst[i].rsplit(' - ')[0]  # take first login time
        end = time_lst[i].rsplit(' - ')[1]  # take first logout time
        start1 = time_lst[i + 1].rsplit(' - ')[0]  # take second login time
        end1 = time_lst[i + 1].rsplit(' - ')[1]  # take second logout time
        # if the earlier timeframe ended after the later timeframe, 
        # then no need to count the subset timeframe:
        if end >= end1:
            del (time_lst[i + 1])
        # if the logged-in timeframes overlap then join them togeter as a longer timeframe:
        elif start1 <= end <= end1:
            time_lst[i] = start + " - " + end1 # join to a longer timeframe 
            del (time_lst[i + 1])  # deleting the already considered timeframe
        else:   # if the two timeframes are distinct then move on to the next couple of timeframes
            i += 1

    # starting the total overall minutes calculation:
    overall = 0
    for frame in time_lst:
        sh = int(frame.rsplit(":")[0])  # starting hour
        sm = int(frame.rsplit(":")[1])  # starting minute
        eh = int(frame.rsplit(":")[2].rsplit("- ")[1])  # ending hour
        em = int(frame.rsplit(":")[3])  # ending minute

        overall += (eh - sh) * 60 + (em - sm)
            
    return overall

def check_hebrew(s):
    """
    checks if a string contains any hebrew letter, if so returns true, else returns false
    :param s: string
    :return: bool
    """
    for c in s:
        if ord('\u05d0') <= ord(c) <= ord('\u05ea'):    # if the character is in range of the unicode of hebrew letters
            return True
    return False

def choose_name(origin_name, new_name):
    """
    Chooses a better name from a pair of two names
    return: string of the better name
    """
    if check_hebrew(origin_name) and not check_hebrew(new_name):
        return new_name
    elif not check_hebrew(origin_name) and check_hebrew(new_name):
        return origin_name
    else:
        if len(origin_name) > len(new_name):
            return origin_name
        else:
            return new_name

def check_empty_fields(line, user):
    ROOM_NAME = 0
    ROOM_START = 1
    ROOM_FINISH = 2
    OVERALL_TIME = 7
    
    if user['room'] == '': user['room'] = line[ROOM_NAME]
    if user['room start'] == '': user['room start'] = line[ROOM_START]
    if user['room finish'] == '': user['room finish'] = line[ROOM_FINISH]
    if user['overall time'] == '': user['overall time'] = line[OVERALL_TIME]
    
        
def sql_arrange(time_dict, cursor, max_time):
    """
    goes over each row in a meeting table and updates the paticipant's dictionary accordingly
    :param time_dict: a dictionary holding the login times of each participant in a meeting
    :param cursor: a cursor to the mysql attendance database
    :param max_time: the maximal time one can be logged-in in a meeting 
    :return:
    """
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
    # now tempList is a list of tupples, each tupple is a row in the temp table sorted by join time 
    for line in tempList:
        # if participant is non-student then skip:
        if "bynet" in line[EMAIL] or "8200" in line[EMAIL] or "nan" in line[EMAIL] or '' == line[EMAIL]: 
            continue
        username = line[EMAIL].rsplit('@')[0]   # take the username before the email '@' character
        fix =  check_spell(username, time_dict) # check if typos occured in the username and correct them
        if not fix: # if the username doesn't exist in the dictionary then create an entry for it
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
            username = fix # if the username exists, then correct the typos if necessary 
            time_dict[username]['name'] = choose_name(time_dict[username]['name'], line[NAME])
            check_empty_fields(line, time_dict[username])
            
        
        time = get_time(line[JOIN_TIME], line[LEAVE_TIME])
        time_dict[username]['time'].append(time)
        time_dict[username]['platform'] = platform_updater(time_dict[username]['platform'], line[PLATFORM])
    # calculate the accurate overall login time of each user:
    for user in time_dict.keys():
        # if more than one timeframe exists for the user then calculate the overall time:
        if len(time_dict[user]['time']) > 1:
            time_dict[user]['overall time'] =  time_updater(time_dict[user]['time'])
            """if time_dict[user]['overall time'] > max_time:
                time_dict[user]['overall time'] = max_time"""
        # update the string of all timeframes to be equal to the timeframes list delimited by ','
        time_dict[user]['time string'] = ', '.join(time_dict[user]['time'])
        del time_dict[user]['time'] # no need for this list now that we're done with timeframes calculation

def print_time_dict(time_dict):
    for user in time_dict.keys():
        print(time_dict[user])            
    
def insert_dict(time_dict, cursor, connection):
    """
    updates the final table "attendance" with the values from the participant's dictionary
    :param time_dict: the participant's dictionary
    :param cursor: the cursor to the mysql attendance database
    :param connection: connection to the mysql datab
    """
    # insert the final values of the participant's dictionary from a csv file
    # if 
    for user in time_dict.keys():
        if time_dict[user]['room'] == '': continue
        
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

def get_user_average(cursor, mail, sum_all_days):
    OVERALL_DAY_TIME = 0
    
    cursor.execute(f" SELECT overall_time FROM attendance WHERE email='{mail}'; ")
    alluserdays = cursor.fetchall()
    
    sum_user_days = 0
    for day in alluserdays:
        sum_user_days += int(day[OVERALL_DAY_TIME])
    
    return sum_user_days/sum_all_days

def get_average(cursor):
    MAIL = 0
    NAME = 1
    
    cursor.execute(" SELECT DISTINCT email,name FROM attendance; ")
    users = cursor.fetchall()
    avg = []
    sum_all_days = sum_of_days(cursor)
    
    for user in users:
        avg.append([user[MAIL], user[NAME], 100*get_user_average(cursor, user[MAIL], sum_all_days)])
        
    return avg

def get_table(cursor, categories):
    cursor.execute(f" SELECT {categories} FROM attendance; ")
    return cursor.fetchall()

def get_table_specifics(cursor, categories, input_type, input_text):
    cursor.execute(f" SELECT {categories} FROM attendance WHERE {input_type} = '{input_text}'; ")
    return cursor.fetchall()

def get_table_dynamic(cursor, categories, input_type, input_text):
    cursor.execute(f" SELECT {categories} FROM attendance; ")
    res = cursor.fetchall()
    cursor.execute(f" SELECT {input_type} FROM attendance; ")
    search_by = cursor.fetchall()
    i = 0
    for search_result in search_by:
        if not (jellyfish.damerau_levenshtein_distance(search_result[0], input_text) < 3):
            del res[i]
        else:
            i += 1
    
    return res
    
def reset_time_dict(time_dict):
    for user in time_dict.keys():
        time_dict[user] = {
            'room': '',
            'room start': '',
            'room finish': '',
            'name': time_dict[user]['name'],
            'email': time_dict[user]['email'],
            'time': [],
            'time string': '',
            'overall time': '',
            'platform': ''
        }

def update_names(time_dict, cursor, connection):
    for user in time_dict.keys():
        cursor.execute(f" UPDATE attendance SET name='{time_dict[user]['name']}' WHERE email='{time_dict[user]['email']}'; ")
    connection.commit()

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
    connection, cursor, error = init_sql()
    if error == True: return "Bad connection to database"
    time_dict = {}
    for i in range(len(csv_lst)):
        reset_time_dict(time_dict)
        max_overall = get_data(csv_lst[i], cursor)
        sql_arrange(time_dict, cursor, max_overall)
        insert_dict(time_dict, cursor, connection)
    update_names(time_dict, cursor, connection)
    disable_connection(connection, cursor)
    return "good connection"

def delete_database(cursor, connection):
    cursor.execute(" DELETE FROM attendance; ")
    connection.commit()
    return "Database deleted successfully"

def post_api(dir):
    if not os.path.isdir(dir):
        return 'Not a Directory!'
    check_connection = post_csv(dir)
    if check_connection == "Bad connection to database": return check_connection
    return 'Done!'

def get_api(categories):
    connection, cursor, error = init_sql()
    if error == True: return "Bad connection to database"
    try:
        results = get_table(cursor, categories)
    except:
        results = 'problem with request'
    finally:
        disable_connection(connection, cursor)
        return results
    
def get_specific_api(categories, input_type, input_text, dynamic):
    connection, cursor, error = init_sql()
    if error == True: return "Bad connection to database"
    try:
        if dynamic: results = get_table_dynamic(cursor, categories, input_type, input_text)
        else: results = get_table_specifics(cursor, categories, input_type, input_text)
    except:
        results = 'problem with request'
    finally:
        disable_connection(connection, cursor)
        return results

def get_avg_api():
    connection, cursor, error = init_sql()
    if error == True: return "Bad connection to database"
    try:
        results = get_average(cursor)
    except:
        results = 'problem with request'
    finally:
        disable_connection(connection, cursor)
        return results

def delete_api():
    connection, cursor, error = init_sql()
    if error == True: return "Bad connection to database"
    try:
        results = delete_database(cursor, connection)
    except:
        results = 'problem with request'
    finally:
        disable_connection(connection, cursor)
        return results
