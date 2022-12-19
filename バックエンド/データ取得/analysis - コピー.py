import requests
import json
import csv
import datetime
import jpholiday
import time
import collections as cl
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family'] = 'HGGothicM'
import pprint

# file open
start = datetime.datetime(2020, 11, 20).date()
end = datetime.datetime(2020, 11, 25).date()
# end = datetime.date.today()
json_data = cl.OrderedDict()
i = 0
# while start != (end + datetime.timedelta(days = 1)):
while start != end:
    filename ='log_' + start.strftime('%Y%m%d') + '.json'
    with open(filename, 'r') as f:
        json_data[i] = json.load(f)     
    start = start + datetime.timedelta(days = 1)
    i += 1

delay_data = {}
delay_data['weekday'], delay_data['holiday'] = {}, {}
delay_data['weekday']['sum'], delay_data['weekday']['lines'] = [0]*24, [0]*24
delay_data['holiday']['sum'], delay_data['holiday']['lines'] = [0]*24, [0]*24

for days in range(len(json_data)):
    for minutes in json_data[days]:
        date_data = json_data[days][minutes]['date'].split('_')
        holiday = datetime.datetime(int(date_data[0]), int(date_data[1]), int(date_data[2]))
        if holiday.weekday() >= 5 or jpholiday.is_holiday(holiday): #土日祝日
            for hour in range(0, 24):
                if int(date_data[3]) >= hour and  int(date_data[3]) < hour+1:
                    for lines in json_data[days][minutes]['delaytrain']:
                        delay_data['weekday']['sum'][hour] += int(json_data[days][minutes]['delaytrain'][lines]['delay'])
                        delay_data['weekday']['lines'][hour] += 1
                
        else: # 平日
            for hour in range(0, 24):
                if int(date_data[3]) >= hour and  int(date_data[3]) < hour+1:
                    for lines in json_data[days][minutes]['delaytrain']:
                        delay_data['holiday']['sum'][hour] += int(json_data[days][minutes]['delaytrain'][lines]['delay'])
                        delay_data['holiday']['lines'][hour] += 1

print(delay_data['weekday'])

""" # グラフ描画
    fig1, (ax_L, ax_R) = plt.subplots(ncols=2, figsize=(16,4))
    x = list(range(24))
    ax_L.bar(x, [delay_data['weekday']['sum'][i]/60 for i in range(24)])
    ax_L.set_title('Weekday')
    ax_L.set_xlabel('Hour'), ax_L.set_ylabel('Sum[分]')
    ax_R.bar(x, [delay_data['holiday']['sum'][i]/60 for i in range(24)])
    ax_R.set_title('Holiday')
    ax_R.set_xlabel('Hour'), ax_R.set_ylabel('Sum[分]')


    fig2, (ax_L, ax_R) = plt.subplots(ncols=2, figsize=(16,4))
    x = list(range(24))
    ax_L.bar(x, delay_data['weekday']['lines'])
    ax_L.set_title('Weekday')
    ax_L.set_xlabel('Hour'), ax_L.set_ylabel('lines[本]')
    ax_R.bar(x, delay_data['holiday']['lines'])
    ax_R.set_title('Holiday')
    ax_R.set_xlabel('Hour'), ax_R.set_ylabel('lines[本]')

    fig3, (ax_L, ax_R) = plt.subplots(ncols=2, figsize=(16,4))
    x = list(range(24))

    ax_L.bar(x, [delay_data['weekday']['sum'][i]/(delay_data['weekday']['lines'][i]*60) if delay_data['weekday']['lines'][i]!=0 else 0 for i in range(24)])
    ax_L.set_title('Weekday')
    ax_L.set_xlabel('Hour'), ax_L.set_ylabel('Ave[分]')
    ax_R.bar(x, [delay_data['holiday']['sum'][i]/(delay_data['holiday']['lines'][i]*60) if delay_data['holiday']['lines'][i]!=0 else 0 for i in range(24)])
    ax_R.set_title('Holiday')
    ax_R.set_xlabel('Hour'), ax_R.set_ylabel('Ave[分]')
 """

# 遅延発生と列車番号の照合
from enum import Enum, auto
class Delay_num(Enum):
    date = 0
    delay = auto()
    fromStation = auto()
    toStation = auto()
    trainInformationCause = auto()
    trainInformationStatus = auto()

def alt_list(json_data, days, minutes, delayNum):
    alt_list = []    
    alt_list.append(json_data[days][minutes]['date'])
    alt_list.append(int(json_data[days][minutes]['delaytrain'][delayNum]['delay']))
    alt_list.append(json_data[days][minutes]['delaytrain'][delayNum]['fromStation'])
    alt_list.append(json_data[days][minutes]['delaytrain'][delayNum]['toStation'])
    alt_list.append(json_data[days][minutes]['trainInformationCause'])
    alt_list.append(json_data[days][minutes]['trainInformationStatus'])
    return alt_list

delay_train = {}
for days in range(len(json_data)):
    for minutes in json_data[days]:
        for delayNum in json_data[days][minutes]['delaytrain']:
            trainNumber = json_data[days][minutes]['delaytrain'][delayNum]['trainNumber']
            """
            if:  新しい列車番号ならば
                辞書に2次元リストを新規登録・遅延追加
            else:
                if:　登録済み最新遅延の方向
                if:　比較する遅延の方向
                その列車の登録済み最新遅延と比較
                if:  10分以上の間隔 or 上り下りが反転
                    新しい遅延として追加
                else:  
                    遅延継続中として既存の遅延に追加
            """
            if trainNumber not in delay_train:
                delay_train[trainNumber] = [[]]
                delay_train[trainNumber][-1].append(alt_list(json_data, days, minutes, delayNum))
            else:
                if delay_train[trainNumber][-1][-1][Delay_num.fromStation.value] < delay_train[trainNumber][-1][-1][Delay_num.toStation.value]:
                    direction_1 = 1
                else: direction_1 = -1
                if json_data[days][minutes]['delaytrain'][delayNum]['fromStation'] < json_data[days][minutes]['delaytrain'][delayNum]['toStation']:
                    direction_2 = 1
                else: direction_2 = -1      
                date_pre = datetime.datetime.strptime(delay_train[trainNumber][-1][-1][Delay_num.date.value], '%Y_%m_%d_%H_%M_%S')
                date_this = datetime.datetime.strptime(json_data[days][minutes]['date'], '%Y_%m_%d_%H_%M_%S')
                if date_this - datetime.timedelta(minutes=10) > date_pre or direction_1 != direction_2:
                    delay_train[trainNumber].append([])
                    delay_train[trainNumber][-1].append(alt_list(json_data, days, minutes, delayNum))
                else:
                    delay_train[trainNumber][-1].append(alt_list(json_data, days, minutes, delayNum))
                
# print(json.dumps(delay_train, indent=4, ensure_ascii=False))

# for days in range(len(json_data)):
#     print(json.dumps(json_data[days], indent=4, ensure_ascii=False))

delay_station = []
for train in delay_train:
    for s in range(len(delay_train[train])):
        sample = [0]*24
        for t in range(len(delay_train[train][s])):
            """
            if:
                if:
                    上り下りを判定
                else:
                遅延発生駅は負の値を格納（index(min())でインデックス取得するため）
            tostation に delay を格納

            if:　下りのとき
                if:　1つ前の遅延が０か判定
                    ０を全てその前の遅延で書き換える
            else:　上りのとき
                同様
            """
            if t == 0:
                start_station = delay_train[train][s][t][Delay_num.fromStation.value]
                if start_station < delay_train[train][s][t][Delay_num.toStation.value]:
                    direction = 1
                else: direction = -1
                sample[start_station-1] = -1
            sample[delay_train[train][s][t][Delay_num.toStation.value]-1] = delay_train[train][s][t][Delay_num.delay.value]
            
            i = 1
            if direction > 0:
                if sample[delay_train[train][s][t][Delay_num.toStation.value]-1-i] == 0:
                    while sample[delay_train[train][s][t][Delay_num.toStation.value]-1-i] == 0:
                        i += 1
                    for emp_num in range(1, i):
                        sample[delay_train[train][s][t][Delay_num.toStation.value]-1-emp_num] = sample[delay_train[train][s][t][Delay_num.toStation.value]-1-i]
            else:
                if sample[delay_train[train][s][t][Delay_num.toStation.value]-1+i] == 0:
                    while sample[delay_train[train][s][t][Delay_num.toStation.value]-1+i] == 0:
                        i += 1
                    for emp_num in range(1, i):
                        sample[delay_train[train][s][t][Delay_num.toStation.value]-1+emp_num] = sample[delay_train[train][s][t][Delay_num.toStation.value]-1+i]
                
        delay_station.append(sample)

for i in range(len(delay_station)):
    print(delay_station[i])











