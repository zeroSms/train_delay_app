from flask import Flask, request, render_template
import requests
import json
import datetime
import time
import collections as cl
import jpholiday

app = Flask(__name__)

@app.route('/')
def index():
    # フォームを表示する --- (*2)
    JR_East_location = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:Train?odpt:operator=odpt.Operator:JR-East'\
                        '&odpt:railway=odpt.Railway:JR-East.ChuoRapid'\
                        '&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'

    # Requestsを利用してWebページをjson形式で取得する
    headers = {"content-type": "application/json"}
    JR_East_location_data = requests.get(
        JR_East_location, headers=headers).json()  # 現在の運行情報


    train_location = [[[] for i in range(2)] for i in range(23)]
    station_name=['東京','神田','御茶ノ水','四ツ谷','新宿','中野','高円寺','阿佐ヶ谷','荻窪',
                  '西荻窪','吉祥寺','三鷹','武蔵境','東小金井','武蔵小金井','国分寺','西国分寺',
                  '国立','立川','日野','豊田','八王子','西八王子']

    t_station = 0
    f_station = 0
    for i in JR_East_location_data:
        d_flag = 0
        # print(i["odpt:fromStation"])
        # print(i["odpt:toStation"])
        if i['odpt:toStation'] is None:
            continue
        f_station = Station_number(i["odpt:fromStation"].split('.')[3])
        t_station = Station_number(i["odpt:toStation"].split('.')[3])

        if (f_station - t_station) == -1:
            delay = int(i['odpt:delay'] / 60)
            if delay > 0:
                d_flag = 1
            train_location[f_station - 1][1].append({'t_number': i['odpt:trainNumber'],
                                        'd_flag': d_flag, 'd_time': delay})


        if (f_station - t_station) == 1:
            delay = int(i['odpt:delay'] / 60)
            if delay > 0:
                d_flag = 1
            train_location[f_station - 2][0].append({'t_number': i['odpt:trainNumber'],
                                        'd_flag': d_flag, 'd_time': delay})


    print(train_location)

    return render_template(
        'index2.html', s=train_location, station_name=station_name)


# 列車ロケーション情報の処理
def Station_number(station_Title):  # 駅番号変換
    JR_East_Route = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:Railway?odpt:operator=odpt.Operator:JR-East'\
                    '&odpt:railwayTitle.en=Chuo%20Rapid%20Line'\
                    '&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
    headers = {"content-type": "application/json"}

    JR_East_Route_data = requests.get(
        JR_East_Route, headers=headers).json()  # 駅番号

    for line in range(len(JR_East_Route_data[0]['odpt:stationOrder'])):
        if (station_Title == JR_East_Route_data[0]['odpt:stationOrder'][line]['odpt:stationTitle']['en'].replace("-", "")):
            return JR_East_Route_data[0]['odpt:stationOrder'][line]['odpt:index']


# /hello へアクセスがあった時 --- (*3)
@app.route('/hello', methods=['POST'])
def hello():
    # nameのパラメータを得る --- (*4)
    train_number = request.form.get('number')
    print(train_number)
    station = int(request.form.get('station_name'))

    print(type(station))

    DATE = datetime.date.today().strftime('%Y%m%d')
    Date = datetime.date(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8]))
    if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
        print("holiday")
        calnder='SaturdayHoliday'
    else:
        print("weekday")
        calnder='Weekday'

    # 列車到着時間
    station_name=['東京','神田','御茶ノ水','四ツ谷','新宿','中野','高円寺','阿佐ヶ谷','荻窪',
                  '西荻窪','吉祥寺','三鷹','武蔵境','東小金井','武蔵小金井','国分寺','西国分寺',
                  '国立','立川','日野','豊田','八王子','西八王子','高尾']
    train_time_table_url = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainTimetable?odpt:operator=odpt.Operator:JR-East'\
                    '&odpt:calendar=odpt.Calendar:%s&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:trainNumber=%s'\
                    '&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4' % (calnder,train_number)
    headers = {"content-type": "application/json"}
    train_time_table_data = requests.get(train_time_table_url, headers=headers).json()  # 現在の運行情報

    #列車の到着時刻表を作成（全部）
    train_time_table=[]#到着時間表格納用
    railDirection = train_time_table_data[0]['odpt:railDirection']
    timetable_object = train_time_table_data[0]['odpt:trainTimetableObject']
    train_time_table_len = len(timetable_object)
    #odpt:arrivalStationをodpt:departureStationに変換
    if len(timetable_object[train_time_table_len-1]) == 2:
        timetable_object[train_time_table_len-1]['odpt:departureTime'] = timetable_object[train_time_table_len-1].pop('odpt:arrivalTime')
        timetable_object[train_time_table_len-1]['odpt:departureStation'] = timetable_object[train_time_table_len-1].pop('odpt:arrivalStation')
    else:
        train_time_table_len = train_time_table_len-1

    for i in range(train_time_table_len):
        number = Station_number(timetable_object[i]["odpt:departureStation"].split('.')[3])
        if railDirection == 'odpt.RailDirection:Outbound':
            if station < number-1:
                timetable_object[i]["odpt:departureStation"] = station_name[number-1]
                train_time_table.append(timetable_object[i])
                date_dt = datetime.datetime.strptime(timetable_object[i]['odpt:departureTime'], '%H:%M')
        else:
            if station >= number-1:
                timetable_object[i]["odpt:departureStation"] = station_name[number-1]
                train_time_table.append(timetable_object[i])
                date_dt = datetime.datetime.strptime(timetable_object[i]['odpt:departureTime'], '%H:%M')

    return render_template(
        'time-table.html', test=train_time_table)


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
