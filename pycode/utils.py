import os
import numpy as np
import pandas as pd
import datetime
import csv
import json
import networkx as nx

def read_csv(path):
    '''
    read the data files in ./data
    '''
    # use pandas to read and store the data of the .csv files
    data_wb = pd.read_csv(os.path.join(path, "网吧信息.csv"))
    print("Reading 网吧信息.csv......")
    # the index of the swjl data
    Index = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    # for index in Index[0: 2]: # just for test of the code
    for index in Index[0: 16]:
        swjl_path = "hydata_swjl_" + str(index) + ".csv"
        data_swjl_tmp = pd.read_csv(os.path.join(path, swjl_path), low_memory=False)
        if index == 0:
            data_swjl = data_swjl_tmp
        else:
            data_swjl = pd.concat((data_swjl, data_swjl_tmp), axis=0, join="inner")
        print("Reading %s......"% swjl_path)
    return data_swjl, data_wb

def data_clean(swjl, wb):
    '''
    clean the swjl and wb data
    '''
    # clean the swjl data
    # swjl_clean = []
    # for i in range(swjl.shape[0]):
    #     print(swjl_clean)
    #     birthday = swjl.at[i, 'BIRTHDAY'].to_numpy()[0]
    #     if int(birthday) > 20170000 or len(str(birthday)) != 8:
    #         swjl_clean.append(i)
    #         continue
    #
    #     areaid = str(int(swjl.at[i, 'AREAID'].to_list()[0]))
    #     if len(areaid) != 6:
    #         swjl_clean.append(i)
    #         continue
    #
    #     # online, offline = map(int, [swjl.loc[i, 'ONLINETIME'].to_numpy()[0]
    #     #                             , swjl.loc[i, 'OFFLINETIME'].to_numpy()[0]])
    #     # if online > offline:
    #     #     swjl_clean.append(i)
    #     #     continue
    # swjl.drop(swjl_clean)
    # for i in range(swjl.shape[0]):
    #     # clean the 'BIRTHDAY' column
    #     person_birth = swjl.iloc[i, swjl.columns.get_loc('BIRTHDAY')]
    #     try:
    #         person_birth = int(person_birth)
    #     except:
    #         swjl.loc[i, 'BIRTHDAY'] = pd.NA
    #         continue
    #     if person_birth > 20170000 or len(str(person_birth)) != 8:
    #         swjl.loc[i, 'BIRTHDAY'] = pd.NA
    #         continue
    #     birth_format = dayformatter(str(person_birth))
    #     if birth_format == "Invalid date":
    #         swjl.loc[i, 'BIRTHDAY'] = pd.NA
    #         continue
    #     # clean the 'AREAID' column
    #     area = str(swjl.iloc[i, swjl.columns.get_loc('AREAID')])
    #     if len(area) != 6 or not is_number(area):
    #         swjl.loc[i, 'AREAID'] = pd.NA
    #         continue
    #     # clean the 'ONLINETIME' and 'OFFTIMELINE' column
    #     onlinetime, offlinetime = swjl.iloc[i, swjl.columns.get_loc('ONLINETIME')],\
    #                                     swjl.iloc[i, swjl.columns.get_loc('OFFLINETIME')]
    #     if timediff(str(onlinetime), str(offlinetime)) <= 0:
    #         swjl.loc[i, 'ONLINETIME'] = pd.NA
    #         continue
    # drop the NAs
    swjl = swjl.dropna(axis=0, how='any')
    # clean the wb data
    for i in range(wb.shape[0]):
        title = str(wb.at[i, 'TITLE'])
        # delete the bracket and space in the title of bar
        new_title = (title.replace(")", "").replace("）", "").replace(" ", "")
                     .replace("(", "").replace("（", ""))
        if new_title != title:
            wb.at[i, 'TITLE'] = new_title
    wb = wb.drop(wb.columns[-1], axis=1)
    wb = wb.dropna(how="any", axis=0)
    return swjl, wb

def series_to_numpy(data, col):
    return data[col].to_numpy()

def series_to_list(data, col):
    return data[col].tolist()

def timeformatter(time):
    '''
    change the type of time(<str> to <datetime>)
    '''
    try:
        year, month, day, hour, minute, second = map(int, (time[0: 4], time[4: 6], time[6: 8],
                                                           time[8: 10], time[10: 12], time[12: 14]))
        time = datetime.datetime(year, month, day, hour, minute, second)
        return time
    except ValueError:
        return 0

def timediff(time1, time2):
    '''
    compute the time difference between time1 and time2
    '''
    time1, time2 = timeformatter(time1), timeformatter(time2)
    if time1 == 0 or time2 == 0:
        return 0
    duration = time2 - time1
    successive_hours = duration.days * 24 + duration.seconds / 3600
    return successive_hours

def minutediff(time1, time2):
    '''
    compute the difference of minute between time1 and time2
    '''
    time1, time2 = timeformatter(time1), timeformatter(time2)
    # if time1 == 0 or time2 == 0:
    #     return -1
    duration = time2 - time1
    return duration.seconds / 60

def dayformatter(day):
    '''
    transform the type of birthday(<str> to <datetime>)
    '''
    try:
        year, month, day = map(int, (day[0: 4], day[4: 6], day[6: 8]))
        date = datetime.date(year, month, day)
        return date
    except ValueError:
        return "Invalid date"

def daydiff(date):
    '''
    set the date of today as 2017.08.01
    '''
    now_date = datetime.date(2017, 8, 1)
    date_difference = now_date.__sub__(date).days
    if date_difference // 365 >= 18:
        return True
    return False

def average_time(time1, time2):
    '''
    Find the mean of time1 and time2
    '''
    time1, time2 = timeformatter(time1), timeformatter(time2)
    if time1 == 0 or time2 == 0:
        return False
    total_seconds = (time2 - time1).total_seconds()
    mean_seconds = total_seconds / 2
    mean_time = time1 + datetime.timedelta(seconds=mean_seconds)
    return mean_time.time()

def check_results(obj, name=""):
    '''
    print each dictionary in the list
    '''
    if name != "":
        print("The dictionaties in %s are listed below:" % name)
    for each in obj:
        print(each)

def list_to_dict(name, col):
    '''
    change the sorted dictionary in list to readable dictionary
    '''
    res = dict()
    for i in range(len(name)):
        title = name[i][col]
        remain = name[i]
        remain.pop(col)
        res[title] = remain
    return res

def save_as_csv(data, name):
    '''
    save the list with dictionaries as csv
    '''
    csv_file_path = name
    fields = data[0].keys()

    with open(csv_file_path, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

    print("File %s has been created in success!" % name)
    print("-----------------------------------------------")

def is_number(str):
    '''
    check if the input string is composed of pure numbers
    '''
    return str.isdigit()

def compute_age(day):
    '''
    compute the age of the person given the birthday
    '''
    now_date = datetime.date(2017, 8, 1)
    date_difference = now_date.__sub__(day).days
    return date_difference // 365

def save_chunk_csv(data, name):
    chunk_size = 1000000
    num_rows = len(data)
    num_chunks = num_rows // chunk_size + 1
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size
        # find the chunk
        current_chunk = data.iloc[start_idx:end_idx, :]
        current_name = name + "_%d" % (i + 1) + ".csv"
        current_chunk.to_csv(current_name, index=False)
    print("Data has been written to %s" % name)
    print("--------------------------------")

def process_areaid():
    '''
    process the "area.csv" in ./output_csv to get our desired areaid---areaname converter
    '''
    file_path = "./output_csv/area.csv"
    df = pd.read_csv(file_path)
    # df = df.dropna(axis=0, how='any')
    area_list = []
    areaid = series_to_numpy(df, "0")
    # yearidx = series_to_list(df, "2020")
    df = df.drop('0', axis=1)
    
    for i in range(len(df)):
        yearidx = df.loc[i].first_valid_index()
        area_list.append({"area": areaid[i], "name": df.loc[i, yearidx]})

    save_as_csv(area_list, "./output_csv/ID_NAME_convert.csv")

def check_df_length(data):
    '''
    print the length of rows in this dataframe
    '''
    path = "./output_csv/" + str(data) + ".csv"
    df = pd.read_csv(path)
    print("The number of rows in %s" % data + "is: %d" % len(df))
    return