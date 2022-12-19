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

# file open
start = datetime.datetime(2020, 11, 29).date()
end = datetime.datetime(2020, 11, 29).date()
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

def write_delay_ave(y1, y2, types, unit):
    ylabel = types + '  [{}]'.format(unit)
    ax_L.bar(x, y1)
    ax_L.set_title(r'$Weekday$')
    ax_L.set_xlabel(r'$hour$'), ax_L.set_ylabel(r'${}$'.format(ylabel))
    ax_R.bar(x, y2)
    ax_R.set_title(r'$Holiday$')
    ax_R.set_xlabel(r'$hour$'), ax_R.set_ylabel(r'${}$'.format(ylabel))
    ax_L.grid(True), ax_R.grid(True)

# # # グラフ描画
# x = list(range(24))
# fig1, (ax_L, ax_R) = plt.subplots(ncols=2, figsize=(16,4))
# y1, y2 = [delay_data['weekday']['sum'][i]/60 for i in range(24)], [delay_data['holiday']['sum'][i]/60 for i in range(24)]
# write_delay_ave(y1, y2, 'sum', 'minutes')

# fig2, (ax_L, ax_R) = plt.subplots(ncols=2, figsize=(16,4))
# y1, y2 = [delay_data['weekday']['lines'][i]/60 for i in range(24)], [delay_data['holiday']['lines'][i]/60 for i in range(24)]
# write_delay_ave(y1, y2, 'lines', 'n')

# fig3, (ax_L, ax_R) = plt.subplots(ncols=2, figsize=(16,4))
# y1 = [delay_data['weekday']['sum'][i]/(delay_data['weekday']['lines'][i]*60) if delay_data['weekday']['lines'][i]!=0 else 0 for i in range(24)]
# y2 = [delay_data['holiday']['sum'][i]/(delay_data['holiday']['lines'][i]*60) if delay_data['holiday']['lines'][i]!=0 else 0 for i in range(24)]
# write_delay_ave(y1, y2, 'sum', 'minutes')

def make_xy(day):
    sorted_cdf = sorted(cdf_set[day].items(), key=lambda x:x[0])
    delay_list = [sorted_cdf[i][0]/60 for i in range(len(sorted_cdf))]
    count_list = [sorted_cdf[i][1] for i in range(len(sorted_cdf))]
    sum_list = []
    for i in range(len(count_list)):
        if i == 0:  sum_list.append(count_list[i])
        else:   sum_list.append(sum_list[i-1]+count_list[i])
    return delay_list, count_list, sum_list

def write_cdf(ax, day):
    delay_list, count_list, sum_list = make_xy(day)
    ax.plot(delay_list, count_list, 'C0', marker="o", label=r'$count$')
    ax_2 = ax.twinx()
    ax_2.plot(delay_list, [i/sum(count_list) for i in sum_list], 'C1', marker="v", label=r'$sum$')
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax_2.get_legend_handles_labels()
    ax.legend(h1+h2, l1+l2, loc='lower right')
    ax.set_xlabel(r'$delay[minutes]$')
    ax.set_ylabel(r'$count$'), ax_2.set_ylabel(r'$sum$')
    ax.grid(True)    

# fig4, (ax_L, ax_R, ax_C) = plt.subplots(ncols=3, figsize=(24,4))
# write_cdf(ax_L, 'weekday')
# write_cdf(ax_R, 'holiday')
# write_cdf(ax_C, 'Allday')

# ax_L.set_title(r'$Weekday$')
# ax_R.set_title(r'$Holiday$')
# ax_C.set_title(r'$Allday$')

# 遅延発生と列車番号の照合
class Delay_num(Enum):
    date = 0
    delay = auto()
    fromStation = auto()
    toStation = auto()
    trainInformationCause = auto()
    trainInformationStatus = auto()

def alt_list():
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
                delay_train[trainNumber][-1].append(alt_list())
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
                    delay_train[trainNumber][-1].append(alt_list())
                else:
                    delay_train[trainNumber][-1].append(alt_list())
                
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
                    # pprint.pprint(delay_train[train][s])
                    # print(train)
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
        sample.append(delay_train[train][s][0][Delay_num.trainInformationCause.value])
        sample.append(delay_train[train][s][0][Delay_num.trainInformationStatus.value])
                
        delay_station.append(sample)

finish_station_list = {}
for i in range(len(delay_station)):
    List = delay_station[i][:24]
    min_num = List.index(min(List))

    # 遅延終了駅を割り出す
    i = 1
    if min_num+1 < 24 and List[min_num+1] > 0:
        start_delay = List[min_num+1]
        while min_num+1+i < 24 and List[min_num+1+i] > 0:
            i += 1
        finish_station_num = min_num + i    
    # elif min_num-1 >= 0 and List[min_num-1] > 0:
    else:
        start_delay = List[min_num-1]
        while min_num-1-i >= 0 and List[min_num-1-i] > 0:
            i += 1
        finish_station_num = min_num - i

    if min_num not in finish_station_list:
        finish_station_list[min_num] = {}
    if start_delay not in finish_station_list[min_num]:
        finish_station_list[min_num][start_delay] = [0]*24
        finish_station_list[min_num][start_delay][min_num] = '-'
    finish_station_list[min_num][start_delay][finish_station_num] += 1
        
# print("{}".format(json.dumps(finish_station_list[0], indent=4, ensure_ascii=False)))
# print("{}".format(json.dumps(sorted(finish_station_list[0].items(), key=lambda x:x[0]), indent=4, ensure_ascii=False)))

# 遅延終了駅　累積　表
    # for start_station in range(24):
    # # start_station = 0
    #     pd_list = []
    #     sorted_finish = sorted(finish_station_list[start_station].items(), key=lambda x:x[0])
    #     for delay in range(len(sorted_finish)):
    #         pd_list.append(sorted_finish[delay][1])
    #     df = pd.DataFrame(pd_list)
    #     df.index = [sorted_finish[delay][0] for delay in range(len(sorted_finish))]
    #     df.columns = [i+1 for i in range(24)]
    #     pd.set_option('display.max_columns', 100)
    #     filename = "delay_station_" + str(start_station+1) + ".csv"
    #     df.to_csv(filename)
    #     df

#JR東日本の運行状況のURL
JR_East_Route = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:Railway?odpt:operator=odpt.Operator:JR-East&odpt:railwayTitle.en=Chuo%20Rapid%20Line&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_TrainTime_weekday = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:calendar=odpt.Calendar:Weekday&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_TrainTime_holiday = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:calendar=odpt.Calendar:Holiday&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_StationTime = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'

#Requestsを利用してWebページをjson形式で取得する
headers = {"content-type": "application/json"}
JR_East_TrainTime_data = {}
JR_East_TrainTime_data['weekday'] = requests.get(JR_East_TrainTime_weekday, headers=headers).json() 
JR_East_TrainTime_data['holiday'] = requests.get(JR_East_TrainTime_holiday, headers=headers).json()
JR_East_StationTime_data = requests.get(JR_East_StationTime, headers=headers).json()    #現在の運行情報
JR_East_Route_data = requests.get(JR_East_Route, headers=headers).json()    #現在の運行情報


# print("{}".format(json.dumps(JR_East_TrainTime_data[0]['odpt:trainTimetableObject'], indent=4, ensure_ascii=False)))

# print("{}".format(json.dumps(JR_East_TrainTime_data[0], indent=4, ensure_ascii=False)))
# for s in range(len(JR_East_StationTime_data)):
#     print(JR_East_StationTime_data[s][station])
#     print("{}".format(json.dumps(JR_East_StationTime_data[s], indent=4, ensure_ascii=False)))
# print("{}".format(json.dumps(json_data, indent=4, ensure_ascii=False)))


def Station_number(station_Title): #駅番号変換
    for line in range(len(JR_East_Route_data[0]['odpt:stationOrder'])):
        if (station_Title == JR_East_Route_data[0]['odpt:stationOrder'][line]['odpt:stationTitle']['en'].replace("-", "")):
            return JR_East_Route_data[0]['odpt:stationOrder'][line]['odpt:index']

# Station_number(json.dumps(JR_East_location_data[line]['odpt:fromStation'].split('.')[3]).strip('"'))

# ある列車が同じ方向に日に2度以上走行することはあるのか調査
train_check = {}
train_check['weekday'], train_check['holiday'] = {}, {}
count = 0
for dayOfWeek in train_check:
    train_check[dayOfWeek]['Inbound'], train_check[dayOfWeek]['Outbound'] = [], []
    for train in range(len(JR_East_TrainTime_data[dayOfWeek])):
        trainNumber = JR_East_TrainTime_data[dayOfWeek][train]['odpt:trainNumber']
        if JR_East_TrainTime_data[dayOfWeek][train]['odpt:railDirection'] == 'odpt.RailDirection:Inbound':
            if trainNumber not in train_check[dayOfWeek]['Inbound']:
                train_check[dayOfWeek]['Inbound'].append(trainNumber)
            else:
                # print("{}".format(json.dumps(JR_East_TrainTime_data[dayOfWeek][train]['odpt:trainTimetableObject'], indent=4, ensure_ascii=False)))
                count += 1
        else:
            if trainNumber not in train_check[dayOfWeek]['Outbound']:
                train_check[dayOfWeek]['Outbound'].append(trainNumber)
            else:
                # print("{}".format(json.dumps(JR_East_TrainTime_data[dayOfWeek][train]['odpt:trainTimetableObject'], indent=4, ensure_ascii=False)))
                count += 1
# print(count)

pre_post_plot = [[[], []], [[], []]]
def make_pre_post(num):
    post_check = False
    for k in range(len(toStation_set[tostation])):
        if JR_East_StationTime_data[station]['odpt:stationTimetableObject'][time+num+1]['odpt:trainNumber'] == toStation_set[tostation][k][toStation_num.trainNumber.value]:
            # print(toStation_set[tostation][k])
            pre_post_plot[num][0].append(int(toStation_set[tostation][i][toStation_num.delay.value]))
            pre_post_plot[num][1].append(int(toStation_set[tostation][k][toStation_num.delay.value]))
            post_check = True
            break
    if post_check == False:
        pre_post_plot[num][0].append(int(toStation_set[tostation][i][toStation_num.delay.value]))
        pre_post_plot[num][1].append(0)

for tostation in toStation_set:
    for i in range(len(toStation_set[tostation])):
        direction = toStation_set[tostation][i][toStation_num.direction.value]
        trainNumber = toStation_set[tostation][i][toStation_num.trainNumber.value]
        dayOfWeek = toStation_set[tostation][i][toStation_num.dayOfWeek.value]
        # print(toStation_set[tostation][i])
        for station in range(len(JR_East_StationTime_data)):
            if tostation == Station_number(json.dumps(JR_East_StationTime_data[station]['odpt:station'].split('.')[-1]).strip('"')) \
                and direction == JR_East_StationTime_data[station]['odpt:railDirection'].split(':')[-1] \
                and dayOfWeek == JR_East_StationTime_data[station]['odpt:calendar'].split(':')[-1]:
                # print("{}".format(json.dumps(JR_East_StationTime_data[station], indent=4, ensure_ascii=False)))
                for time in range(len(JR_East_StationTime_data[station]['odpt:stationTimetableObject'])):
                    if trainNumber == JR_East_StationTime_data[station]['odpt:stationTimetableObject'][time]['odpt:trainNumber']:
                        # print("{}".format(json.dumps(JR_East_StationTime_data[station]['odpt:stationTimetableObject'][time], indent=4, ensure_ascii=False)))
                        # print("{}".format(json.dumps(JR_East_StationTime_data[station]['odpt:stationTimetableObject'][time+1], indent=4, ensure_ascii=False)))
                        if 'odpt:isLast' not in JR_East_StationTime_data[station]['odpt:stationTimetableObject'][time]:
                            make_pre_post(0)
                            if 'odpt:isLast' not in JR_East_StationTime_data[station]['odpt:stationTimetableObject'][time+1]:
                                make_pre_post(1)



def write_pre_post(ax, i, title):
    ax.scatter(pre_post_plot[i][0], pre_post_plot[i][1])
    ax.set_title('{} scatter plot'.format(title))
    ax.set_xlabel('pre_train'), ax.set_ylabel('post_train')
    ax.set_xlim(-60, max(pre_post_plot[i][0])+60)
    ax.set_ylim(-60, max(pre_post_plot[i][1])+60)
    ax.grid(True), ax_R.grid(True)

# # グラフ描画
fig5, (ax_L, ax_R) = plt.subplots(ncols=2, figsize=(16,4))
write_pre_post(ax_L, 0, 'first')
write_pre_post(ax_R, 1, 'second')




