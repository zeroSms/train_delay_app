import requests
import json
import datetime
import time
import collections as cl

def get_retry(url,headers): #データ取得部
    for i in range(5):
        try:
            r = requests.get(url,headers=headers)
            r.raise_for_status
        except requests.exceptions.RequestException as e:
            print("エラー：",e)
            time.sleep(2)
        else:
            return r

def Station_number(station_Title): #駅番号変換
    for line in range(len(JR_East_Route_data[0]['odpt:stationOrder'])):
        if (station_Title == JR_East_Route_data[0]['odpt:stationOrder'][line]['odpt:stationTitle']['en'].replace("-", "")):
            return JR_East_Route_data[0]['odpt:stationOrder'][line]['odpt:index']
            
# 日数入力部
Number_of_days = input('Number of days: ')
collection_time = int(Number_of_days)*24*60*60

#駅ナンバー変換したもの
#1分おきに遅延調査
N = 0
for i in range (0,collection_time,60):
    flug_delay = 0
    while datetime.datetime.now().strftime('%S') != '00': # 00秒になるまで待機
        time.sleep(1)

    now = datetime.datetime.now()
    if i==0: train_list = cl.OrderedDict() # はじめの初期化
    if now.strftime('%H_%M_%S') == '00_00_00': # 日付変更とともに初期化
        train_list = cl.OrderedDict()
        N = 0        

        #JR東日本の運行状況のURL
    JR_East_location = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:Train?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
    JR_East_status = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
    JR_East_Route = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:Railway?odpt:operator=odpt.Operator:JR-East&odpt:railwayTitle.en=Chuo%20Rapid%20Line&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'

    #Requestsを利用してWebページをjson形式で取得する
    headers = {"content-type": "application/json"}
    JR_East_location_data = get_retry(JR_East_location, headers).json()#現在の運行情報
    JR_East_status_data = get_retry(JR_East_status, headers).json() #現在の遅延情報
    JR_East_Route_data = get_retry(JR_East_Route, headers).json() #駅番号

    now = datetime.datetime.now()

    #遅延状況の取得
    for line in range(len(JR_East_location_data)):
        #遅延している＋終着駅でないもの
        if int(json.dumps(JR_East_location_data[line]['odpt:delay'])) > 0 and json.dumps(JR_East_location_data[line]['odpt:toStation']) != "null":
            flug_delay = 1
            break
    
    if flug_delay == 1:
        train_list[N] = {}
        train_list[N]['date'] = now.strftime('%Y_%m_%d_%H_%M_%S')

        if json.dumps(JR_East_status_data[0]['odpt:trainInformationText']['ja'], ensure_ascii=False).replace('"', '') != '平常運転':
            train_list[N]['trainInformationCause'] = json.dumps(JR_East_status_data[0]['odpt:trainInformationCause']['en']).strip('"')
            train_list[N]['trainInformationStatus'] = json.dumps(JR_East_status_data[0]['odpt:trainInformationStatus']['en']).strip('"')
        else:
            train_list[N]['trainInformationCause'] = "平常運転"
            train_list[N]['trainInformationStatus'] = "平常運転"

        #遅延列車情報の取得
        train_list[N]['delaytrain'] = {}
        num = 0
        for line in range(len(JR_East_location_data)):
            #遅延している＋終着駅でないもの
            if int(json.dumps(JR_East_location_data[line]['odpt:delay'])) > 0 and json.dumps(JR_East_location_data[line]['odpt:toStation']) != "null":
                train_list[N]['delaytrain'][num] = {}
                train_list[N]['delaytrain'][num]['trainNumber'] = json.dumps(JR_East_location_data[line]['odpt:trainNumber']).strip('"')
                train_list[N]['delaytrain'][num]['delay'] = json.dumps(JR_East_location_data[line]['odpt:delay'])
                train_list[N]['delaytrain'][num]['fromStation'] = Station_number(json.dumps(JR_East_location_data[line]['odpt:fromStation'].split('.')[3]).strip('"'))
                train_list[N]['delaytrain'][num]['toStation'] = Station_number(json.dumps(JR_East_location_data[line]['odpt:toStation'].split('.')[3]).strip('"'))
                num += 1
        
        print(train_list[N]) # 1分ごとに出力（動作確認用）
        N += 1
    else: print("null")

    filename ='log_' + now.strftime('%Y%m%d') + '.json'
    with open(filename, 'w') as f:
        json.dump(train_list, f)
        
    time.sleep(1)
