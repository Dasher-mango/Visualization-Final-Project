# import csv
# import os
# import pandas as pd
#
# path = "./data"  # the path to the .csv data
# dirs = os.listdir(path)  # get the name list of data files
# data_swjl = []
# data_wb = []
#
# name = str(path)+'/'+str(dirs[len(dirs)-1])
# df = pandas.read_csv(name,encoding="utf-8")
# for each in df['lng']:
#     print(each)
# import datetime
# a = datetime.date(2018, 9, 5)
# b = datetime.date(2020, 8, 10)
# print(b.__sub__(a).days)

# d = {7: 5, 2: 1, 3: 3}
# d = sorted(d.items(), key=lambda d:d[0])
# print(d)

# print("2365".isdigit())

# df = pd.read_csv("./output_csv/float.csv")
# print(len(df))

from utils import *

process_areaid()