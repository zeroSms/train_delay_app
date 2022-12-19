import requests
import json

Timetable_Number = 9
#JR東日本の運行状況のURL
JR_East_location = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:Train?odpt:operator=odpt.Operator:JR-East&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_Timetable = [
    'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid,odpt.Railway:JR-East.ChuoSobuLocal,odpt.Railway:JR-East.Hachiko&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
    'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Ito,odpt.Railway:JR-East.Itsukaichi,odpt.Railway:JR-East.Joban,odpt.Railway:JR-East.JobanLocal,odpt.Railway:JR-East.JobanRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
    'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Kashima,odpt.Railway:JR-East.Kawagoe,odpt.Railway:JR-East.KeihinTohokuNegishi,odpt.Railway:JR-East.Keiyo&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
    'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Kururi,odpt.Railway:JR-East.Musashino,odpt.Railway:JR-East.Nambu,odpt.Railway:JR-East.NambuBranch&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
    'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Narita,odpt.Railway:JR-East.NaritaAbikoBranch,odpt.Railway:JR-East.NaritaAirportBranch,odpt.Railway:JR-East.Ome&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
    'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Sagami,odpt.Railway:JR-East.SaikyoKawagoe,odpt.Railway:JR-East.ShonanShinjuku,odpt.Railway:JR-East.Sobu,odpt.Railway:JR-East.SobuRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
    'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.SotetsuDirect,odpt.Railway:JR-East.Sotobo,odpt.Railway:JR-East.Takasaki,odpt.Railway:JR-East.Tsurumi,odpt.Railway:JR-East.TsurumiOkawaBranch,odpt.Railway:JR-East.TsurumiUmiShibaurBranch&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
    'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Togane,odpt.Railway:JR-East.Tokaido,odpt.Railway:JR-East.Uchibo,odpt.Railway:JR-East.Utsunomiya&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
    'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Yamanote,odpt.Railway:JR-East.Yokohama,odpt.Railway:JR-East.Yokosuka&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
]

JR_East_Timetable_TokyoMetro = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:operator=odpt.Operator:TokyoMetro&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'

#Requestsを利用してWebページを取得する
headers = {"content-type": "application/json"}
JR_East_location_Requests = requests.get(JR_East_location, headers=headers)
JR_East_Timetable_Requests = []
for i in range(Timetable_Number):
    JR_East_Timetable_Requests.append(requests.get(JR_East_Timetable[i], headers=headers))
JR_East_Timetable_TokyoMetro_Requests = requests.get(JR_East_Timetable_TokyoMetro, headers=headers)

#JSON形式でのデータ取得
JR_East_location_data = JR_East_location_Requests.json()
JR_East_Timetable_data = []
for i in range(Timetable_Number):
    JR_East_Timetable_data.append(JR_East_Timetable_Requests[i].json())
JR_East_Timetable_TokyoMetro_data = JR_East_Timetable_TokyoMetro_Requests.json()
# with open('JR_East_location.txt', mode='w') as f:
#     f.write(json.dumps(JR_East_location_data, indent=4))

# with open('JR_East_Timetable_ChuoRapid.txt', mode='w') as f:
#     f.write(json.dumps(JR_East_Timetable_ChuoRapid_data, indent=4))

# with open('JR_East_Timetable_TokyoMetro.txt', mode='w') as f:
#     f.write(json.dumps(JR_East_Timetable_TokyoMetro_data, indent=4))

#遅延列車情報の取得
with open('JR_East_location_delay.txt', mode='w') as f1:
    for line in range(len(JR_East_location_data)):
        if int(json.dumps(JR_East_location_data[line]['odpt:delay'])) > 0:
            f1.write(json.dumps(JR_East_location_data[line]))
            print(json.dumps(JR_East_location_data[line]['odpt:fromStation']), json.dumps(JR_East_location_data[line]['odpt:toStation']), json.dumps(JR_East_location_data[line]['odpt:trainNumber']), json.dumps(JR_East_location_data[line]['odpt:delay']))

            for i in range(Timetable_Number):
                #遅延列車Numberの照合
                for train in range(len(JR_East_Timetable_data[i])):
                    for trainNumber in range(len(JR_East_Timetable_data[i][train]['odpt:stationTimetableObject'])):
                        if json.dumps(JR_East_location_data[line]['odpt:trainNumber']) == json.dumps(JR_East_Timetable_data[i][train]['odpt:stationTimetableObject'][trainNumber]['odpt:trainNumber']):
                            if json.dumps(JR_East_location_data[line]['odpt:fromStation']) == json.dumps(JR_East_Timetable_data[i][train]['odpt:station']):
                                print(json.dumps(JR_East_Timetable_data[i][train]['odpt:stationTimetableObject'][trainNumber]["odpt:departureTime"]), '\n')



                            
            # for train in range(len(JR_East_Timetable_TokyoMetro_data)):
            #     for trainNumber in range(len(JR_East_Timetable_TokyoMetro_data[train]['odpt:stationTimetableObject'])):
            #         f2.write(json.dumps(JR_East_Timetable_TokyoMetro_data[train]['odpt:stationTimetableObject'][trainNumber]['odpt:trainNumber']))
            #         if json.dumps(JR_East_location_data[line]['odpt:fromStation']) == json.dumps(JR_East_Timetable_TokyoMetro_data[train]['odpt:station']):
            #         #   if json.dumps(JR_East_location_data[line]['odpt:trainNumber']) == json.dumps(JR_East_Timetable_data[train]['odpt:stationTimetableObject'][trainNumber]['odpt:trainNumber']):
            #             if i == 0:
            #                 print(json.dumps(JR_East_Timetable_TokyoMetro_data[train]['odpt:stationTimetableObject'][trainNumber]["odpt:departureTime"]))
            #                 print('aaa')
            #                 i += 1
                    # elif json.dumps(JR_East_location_data[line]['odpt:fromStation']).rsplit('.', 1)[1] == json.dumps(JR_East_Timetable_ChuoRapid_data[train]['odpt:station']).rsplit('.', 1)[1]:
                    #     if i == 0:
                    #         print(json.dumps(JR_East_Timetable_ChuoRapid_data[train]['odpt:stationTimetableObject'][trainNumber]["odpt:departureTime"]))
                    #         print('aaaaa\n')
                    #         i += 1

























