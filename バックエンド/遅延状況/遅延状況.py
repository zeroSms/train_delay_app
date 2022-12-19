import requests
import json
import datetime
import time
import collections as cl

# 日数入力部
Number_of_days = input('Number of days: ')
collection_time = int(Number_of_days)*24*60*60

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

#JR東日本の運行状況のURL
JR_East_status = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?odpt:operator=odpt.Operator:JR-East&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'

#1分おきに遅延調査
N = 0
for i in range (0,collection_time,60):
    flug_delay = 0
    while datetime.datetime.now().strftime('%S') != '00': # 00秒になるまで待機
        time.sleep(1)

    now = datetime.datetime.now()
    if i==0: train_list = cl.OrderedDict() # はじめの初期化
    if now.strftime('%H_%M_%S') == '00_00_00': # 日付変更とともに初期化
    # if now.strftime('%S') == '00': # 日付変更とともに初期化
        train_list = cl.OrderedDict()
        N = 0

    #Requestsを利用してWebページをjson形式で取得する
    headers = {"content-type": "application/json"}
    JR_East_status_data = get_retry(JR_East_status, headers).json() #現在の遅延情報
    
    for line in range(len(JR_East_status_data)):
        #遅延している＋終着駅でないもの
        if json.dumps(JR_East_status_data[line]['odpt:trainInformationText']['ja'], ensure_ascii=False).replace('"', '') != '平常運転':
            flug_delay = 1
            break

    if flug_delay == 1:
        train_list[N] = {}
        train_list[N]['date'] = now.strftime('%Y_%m_%d_%H_%M_%S')
        
        for line in range(len(JR_East_status_data)):
            if json.dumps(JR_East_status_data[line]['odpt:trainInformationText']['ja'], ensure_ascii=False).replace('"', '') != '平常運転':
                print(json.dumps(JR_East_status_data[line], indent=4, ensure_ascii=False))
                train_list[N]['trainInformationText'] = json.dumps(JR_East_status_data[line]['odpt:trainInformationText']['ja']).strip('"')
                train_list[N]['trainInformationCause'] = json.dumps(JR_East_status_data[line]['odpt:trainInformationCause']['en']).strip('"')
                train_list[N]['trainInformationStatus'] = json.dumps(JR_East_status_data[line]['odpt:trainInformationStatus']['en']).strip('"')
        N += 1
    else: print("null")

    filename ='delay_' + now.strftime('%Y%m%d') + '.json'
    with open(filename, 'w') as f:
        json.dump(train_list, f)

    time.sleep(1)



