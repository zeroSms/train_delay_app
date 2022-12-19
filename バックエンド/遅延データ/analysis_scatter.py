import requests
import glob
import json
import csv
from enum import Enum, auto
import datetime
import jpholiday
import time
import pandas as pd
import collections as cl
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family'] = 'HGGothicM'
import pprint


start_time = time.perf_counter()

# file open
start = datetime.datetime(2020, 11, 30).date()
end = datetime.datetime(2020, 12, 6).date()
# end = datetime.date.today()
json_data = cl.OrderedDict()
i = 0
while start != (end + datetime.timedelta(days = 1)):
    filename ='log_' + start.strftime('%Y%m%d') + '.json'
    with open(filename, 'r') as f:
        json_data[i] = json.load(f)
    start = start + datetime.timedelta(days = 1)
    i += 1

# l = glob.glob('log_*.json')
# json_data = []
# for filename in l:
#     with open(filename, 'r') as f:
#         json_data.append(json.load(f))

# 遅延時間　累積分布
cdf_set = {}
cdf_set['weekday'], cdf_set['holiday'], cdf_set['Allday'] = {}, {}, {}
delay_data = {}
delay_data['weekday'], delay_data['holiday'] = {}, {}
delay_data['weekday']['sum'], delay_data['weekday']['lines'] = [0]*24, [0]*24
delay_data['holiday']['sum'], delay_data['holiday']['lines'] = [0]*24, [0]*24
toStation_set = {}

class toStation_num(Enum):
    date = 0
    trainNumber = auto()
    delay = auto()
    fromStation = auto()
    direction = auto()
    dayOfWeek = auto()
    trainInformationCause = auto()

def split_hour(dayOfWeek):
    for hour in range(24):
        if int(date_data[3]) >= hour and  int(date_data[3]) < hour+1:
            for lines in json_data[days][minutes]['delaytrain']:
                delay_data[dayOfWeek]['sum'][hour] += int(json_data[days][minutes]['delaytrain'][lines]['delay'])
                delay_data[dayOfWeek]['lines'][hour] += 1
    return delay_data

def count_cfd(day):
    if delay not in cdf_set[day]:
        cdf_set[day][delay] = 1
    else:
        cdf_set[day][delay] += 1
    return cdf_set

for days in range(len(json_data)):
    for minutes in json_data[days]:
        for lines in json_data[days][minutes]['delaytrain']:
            delay = int(json_data[days][minutes]['delaytrain'][lines]['delay'])
            tostation = json_data[days][minutes]['delaytrain'][lines]['toStation']
            toStation_mini = []
            toStation_mini.append(json_data[days][minutes]['date'])
            toStation_mini.append(json_data[days][minutes]['delaytrain'][lines]['trainNumber'])
            toStation_mini.append(json_data[days][minutes]['delaytrain'][lines]['delay'])
            toStation_mini.append(json_data[days][minutes]['delaytrain'][lines]['fromStation'])
            if tostation > json_data[days][minutes]['delaytrain'][lines]['fromStation']:
                toStation_mini.append('Outbound')
            else:   toStation_mini.append('Inbound')

            date_data = json_data[days][minutes]['date'].split('_')
            holiday = datetime.datetime(int(date_data[0]), int(date_data[1]), int(date_data[2]))
            if holiday.weekday() >= 5 or jpholiday.is_holiday(holiday): #土日祝日
                delay_data = split_hour('holiday')
                cdf_set = count_cfd('holiday')
                toStation_mini.append('SaturdayHoliday')

            else: # 平日
                delay_data = split_hour('weekday')
                cdf_set = count_cfd('weekday')
                toStation_mini.append('Weekday')
            cdf_set = count_cfd('Allday')
            
            toStation_mini.append(json_data[days][minutes]['trainInformationCause'])
            if tostation not in toStation_set:
                toStation_set[tostation] = []
                toStation_set[tostation].append(toStation_mini)
            else:
                toStation_set[tostation].append(toStation_mini)

elapsed_time = int(time.perf_counter()) - int(start_time)
print ("elapsed_time1:{0}".format(elapsed_time) + "[sec]")
start_time = time.perf_counter()

#JR東日本の運行状況のURL
JR_East_Route = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:Railway?odpt:operator=odpt.Operator:JR-East&odpt:railwayTitle.en=Chuo%20Rapid%20Line&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_TrainTime_weekday = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:calendar=odpt.Calendar:Weekday&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_TrainTime_holiday = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:calendar=odpt.Calendar:Holiday&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'

#Requestsを利用してWebページをjson形式で取得する
headers = {"content-type": "application/json"}
JR_East_TrainTime_data = {}
JR_East_TrainTime_data['weekday'] = requests.get(JR_East_TrainTime_weekday, headers=headers).json()
JR_East_TrainTime_data['holiday'] = requests.get(JR_East_TrainTime_holiday, headers=headers).json()
JR_East_Route_data = requests.get(JR_East_Route, headers=headers).json()

def Station_number(station_Title): #駅番号変換
    for line in range(len(JR_East_Route_data[0]['odpt:stationOrder'])):
        if station_Title == JR_East_Route_data[0]['odpt:stationOrder'][line]['odpt:stationTitle']['en'].replace("-", ""):
            return JR_East_Route_data[0]['odpt:stationOrder'][line]['odpt:index']

# def Return_Station(station_number): #番号駅変換
#     if station_number == JR_East_Route_data[0]['odpt:stationOrder'][station_number-1]['odpt:index']:
#         print(JR_East_Route_data[0]['odpt:stationOrder'][station_number-1]['odpt:stationTitle']['en'].replace("-", ""))
#         return JR_East_Route_data[0]['odpt:stationOrder'][station_number-1]['odpt:stationTitle']['en'].replace("-", "")

def StationTime_url(station_number):
    JR_East_StationTime = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:station=odpt.Station:JR-East.ChuoRapid.%s'\
                            '&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'\
                             % (JR_East_Route_data[0]['odpt:stationOrder'][station_number-1]['odpt:stationTitle']['en'].replace("-", ""))
    JR_East_StationTime_data = requests.get(JR_East_StationTime, headers=headers).json()
    return JR_East_StationTime_data


# ある列車が同じ方向に日に2度以上走行することはあるのか調査
# train_check = {}
# train_check['weekday'], train_check['holiday'] = {}, {}
# count = 0
# for dayOfWeek in train_check:
#     train_check[dayOfWeek]['Inbound'], train_check[dayOfWeek]['Outbound'] = [], []
#     for train in range(len(JR_East_TrainTime_data[dayOfWeek])):
#         trainNumber = JR_East_TrainTime_data[dayOfWeek][train]['odpt:trainNumber']
#         if JR_East_TrainTime_data[dayOfWeek][train]['odpt:railDirection'] == 'odpt.RailDirection:Inbound':
#             if trainNumber not in train_check[dayOfWeek]['Inbound']:
#                 train_check[dayOfWeek]['Inbound'].append(trainNumber)
#             else:
#                 # print("{}".format(json.dumps(JR_East_TrainTime_data[dayOfWeek][train]['odpt:trainTimetableObject'], indent=4, ensure_ascii=False)))
#                 count += 1
#         else:
#             if trainNumber not in train_check[dayOfWeek]['Outbound']:
#                 train_check[dayOfWeek]['Outbound'].append(trainNumber)
#             else:
#                 # print("{}".format(json.dumps(JR_East_TrainTime_data[dayOfWeek][train]['odpt:trainTimetableObject'], indent=4, ensure_ascii=False)))
#                 count += 1
# print(count)

pre_post_plot = [[[], []], [[], []]]
def make_pre_post(num):
    post_check = False
    for k in range(len(toStation_set[tostation])):
        if JR_East_StationTime_data[station]['odpt:stationTimetableObject'][STO+num+1]['odpt:trainNumber'] == toStation_set[tostation][k][toStation_num.trainNumber.value]:
            pre_post_plot[num][0].append(int(toStation_set[tostation][i][toStation_num.delay.value]))
            pre_post_plot[num][1].append(int(toStation_set[tostation][k][toStation_num.delay.value]))
            post_check = True
            break
    if post_check == False:
        pre_post_plot[num][0].append(int(toStation_set[tostation][i][toStation_num.delay.value]))
        pre_post_plot[num][1].append(0)


# JR_East_StationTime = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
# JR_East_StationTime_data = requests.get(JR_East_StationTime, headers=headers).json()
# for tostation in toStation_set:
#     for i in range(len(toStation_set[tostation])):
#         direction = toStation_set[tostation][i][toStation_num.direction.value]
#         trainNumber = toStation_set[tostation][i][toStation_num.trainNumber.value]
#         dayOfWeek = toStation_set[tostation][i][toStation_num.dayOfWeek.value]
#         for station in range(len(JR_East_StationTime_data)):
#             if tostation == Station_number(json.dumps(JR_East_StationTime_data[station]['odpt:station'].split('.')[-1]).strip('"')) \
#                 and direction == JR_East_StationTime_data[station]['odpt:railDirection'].split(':')[-1] \
#                 and dayOfWeek == JR_East_StationTime_data[station]['odpt:calendar'].split(':')[-1]:
#                 for STO in range(len(JR_East_StationTime_data[station]['odpt:stationTimetableObject'])):
#                     if trainNumber == JR_East_StationTime_data[station]['odpt:stationTimetableObject'][STO]['odpt:trainNumber']:
#                         if 'odpt:isLast' not in JR_East_StationTime_data[station]['odpt:stationTimetableObject'][STO]:
#                             make_pre_post(0)
#                             if 'odpt:isLast' not in JR_East_StationTime_data[station]['odpt:stationTimetableObject'][STO+1]:
#                                 make_pre_post(1)

print('1111')

for tostation in toStation_set:
    JR_East_StationTime_data = StationTime_url(tostation)
    for i in range(len(toStation_set[tostation])):
        direction = toStation_set[tostation][i][toStation_num.direction.value]
        trainNumber = toStation_set[tostation][i][toStation_num.trainNumber.value]
        dayOfWeek = toStation_set[tostation][i][toStation_num.dayOfWeek.value]
        for station in range(len(JR_East_StationTime_data)):
            if tostation == Station_number(json.dumps(JR_East_StationTime_data[station]['odpt:station'].split('.')[-1]).strip('"')) \
                and direction == JR_East_StationTime_data[station]['odpt:railDirection'].split(':')[-1] \
                and dayOfWeek == JR_East_StationTime_data[station]['odpt:calendar'].split(':')[-1]:
                for STO in range(len(JR_East_StationTime_data[station]['odpt:stationTimetableObject'])):
                    if trainNumber == JR_East_StationTime_data[station]['odpt:stationTimetableObject'][STO]['odpt:trainNumber']:
                        if 'odpt:isLast' not in JR_East_StationTime_data[station]['odpt:stationTimetableObject'][STO]:
                            make_pre_post(0)
                            if 'odpt:isLast' not in JR_East_StationTime_data[station]['odpt:stationTimetableObject'][STO+1]:
                                make_pre_post(1)

print('2222')
elapsed_time = int(time.perf_counter()) - int(start_time)
print ("elapsed_time2:{0}".format(elapsed_time) + "[sec]")
start_time = time.perf_counter()

def write_pre_post(ax, i, title):
    for s in range(len(pre_post_plot[i][0])):
        x, y = pre_post_plot[i][0][s], pre_post_plot[i][1][s]
        ax.scatter(x, y, c='b', alpha=xy_count[i][x][y]/max_count[i][x])
    ax.set_title('{} scatter plot'.format(title))
    ax.set_xlabel('pre_train'), ax.set_ylabel('post_train')
    ax.set_xlim(-60, max(pre_post_plot[i][0])+60)
    ax.set_ylim(-60, max(pre_post_plot[i][1])+60)
    ax.grid(True), ax_R.grid(True)

xy_count = []
max_count = []
for i in range(2):
    xy_count.append({})
    max_count.append({})
    for line in range(len(pre_post_plot[i][0])):
        x = pre_post_plot[i][0][line]
        y = pre_post_plot[i][1][line]
        if x not in xy_count[i]:
            xy_count[i][x] = {}
            max_count[i][x] = 0
        if y not in xy_count[i][x]:
            xy_count[i][x][y] = 1
        else:
            xy_count[i][x][y] += 1
        # if xy_count[i][x][y] > max_count[i][x]:
        #     max_count[i][x] += 1
        max_count[i][x] += xy_count[i][x][y]

elapsed_time = int(time.perf_counter()) - int(start_time)
print ("elapsed_time3:{0}".format(elapsed_time) + "[sec]")
start_time = time.perf_counter()

# # グラフ描画
fig5, (ax_L, ax_R) = plt.subplots(ncols=2, figsize=(16,4))
write_pre_post(ax_L, 0, 'first')
elapsed_time = int(time.perf_counter()) - int(start_time)
print ("elapsed_time4:{0}".format(elapsed_time) + "[sec]")
start_time = time.perf_counter()

write_pre_post(ax_R, 1, 'second')
elapsed_time = int(time.perf_counter()) - int(start_time)
print ("elapsed_time5:{0}".format(elapsed_time) + "[sec]")