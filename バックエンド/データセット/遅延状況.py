import requests
import json

#JR東日本の運行状況のURL
# JR_East_status = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_status = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainInformation?odpt:operator=odpt.Operator:JR-East&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'

#Requestsを利用してWebページをjson形式で取得する
headers = {"content-type": "application/json"}
JR_East_status_data = requests.get(JR_East_status, headers=headers).json() #現在の遅延情報

# print(json.dumps(JR_East_status_data, indent=4, ensure_ascii=False))

# with open('JR_East_status.txt', mode='w') as f:
#     f.write(json.dumps(JR_East_status_data, indent=4, ensure_ascii=False))

#遅延状況の取得
for line in range(len(JR_East_status_data)):
    if json.dumps(JR_East_status_data[line]['odpt:trainInformationText']['ja'], ensure_ascii=False).replace('"', '') != '平常運転':
        print(json.dumps(JR_East_status_data[line]['odpt:trainInformationText']['ja'], ensure_ascii=False).replace('"', ''))
        # print(json.dumps(JR_East_status_data[line]['odpt:trainInformationCause']), json.dumps(JR_East_status_data[line]['odpt:trainInformationStatus']))
        # print(json.dumps(JR_East_status_data[line]['odpt:trainInformationStatus']))



