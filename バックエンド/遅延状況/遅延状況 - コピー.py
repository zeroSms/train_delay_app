import requests
import json
import datetime
import time
import collections as cl

# 日数入力部
# Number_of_days = input('Number of days: ')
# collection_time = int(Number_of_days)*24*60*60

#JR東日本の運行状況のURL
# JR_East_status = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_status = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?odpt:operator=odpt.Operator:JR-East&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'

# #Requestsを利用してWebページをjson形式で取得する
headers = {"content-type": "application/json"}
JR_East_status_data = requests.get(JR_East_status, headers=headers).json() #現在の遅延情報

#遅延状況の取得
for line in range(len(JR_East_status_data)):
    print(json.dumps(JR_East_status_data[line]['odpt:trainInformationText']['ja'], ensure_ascii=False).replace('"', ''))
    if json.dumps(JR_East_status_data[line]['odpt:trainInformationText']['ja'], ensure_ascii=False).replace('"', '') != '平常運転':
        print(json.dumps(JR_East_status_data[line], ensure_ascii=False, indent=4).replace('"', ''))






