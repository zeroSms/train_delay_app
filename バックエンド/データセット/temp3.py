import requests
import json
import datetime
import jpholiday
 

#JR東日本の運行状況のURL
JR_East_location = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:Train?odpt:operator=odpt.Operator:JR-East&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
# 今日が祝日かどうか判定する(祝日＝TRUE,平日＝FALSE)
holiday = jpholiday.is_holiday(datetime.date.today())
if holiday == False:
    JR_East_Timetable = [
        'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:Weekday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid,odpt.Railway:JR-East.ChuoSobuLocal,odpt.Railway:JR-East.Hachiko&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:Weekday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Ito,odpt.Railway:JR-East.Itsukaichi,odpt.Railway:JR-East.Joban,odpt.Railway:JR-East.JobanLocal,odpt.Railway:JR-East.JobanRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:Weekday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Kashima,odpt.Railway:JR-East.Kawagoe,odpt.Railway:JR-East.KeihinTohokuNegishi,odpt.Railway:JR-East.Keiyo&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:Weekday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Kururi,odpt.Railway:JR-East.Musashino,odpt.Railway:JR-East.Nambu,odpt.Railway:JR-East.NambuBranch&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:Weekday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Narita,odpt.Railway:JR-East.NaritaAbikoBranch,odpt.Railway:JR-East.NaritaAirportBranch,odpt.Railway:JR-East.Ome&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:Weekday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Sagami,odpt.Railway:JR-East.SaikyoKawagoe,odpt.Railway:JR-East.ShonanShinjuku,odpt.Railway:JR-East.Sobu,odpt.Railway:JR-East.SobuRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:Weekday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.SotetsuDirect,odpt.Railway:JR-East.Sotobo,odpt.Railway:JR-East.Takasaki,odpt.Railway:JR-East.Tsurumi,odpt.Railway:JR-East.TsurumiOkawaBranch,odpt.Railway:JR-East.TsurumiUmiShibaurBranch&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:Weekday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Togane,odpt.Railway:JR-East.Tokaido,odpt.Railway:JR-East.Uchibo,odpt.Railway:JR-East.Utsunomiya&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:Weekday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Yamanote,odpt.Railway:JR-East.Yokohama,odpt.Railway:JR-East.Yokosuka&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
    ]
else:
    JR_East_Timetable = [
        'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:SaturdayHoliday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid,odpt.Railway:JR-East.ChuoSobuLocal,odpt.Railway:JR-East.Hachiko&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:SaturdayHoliday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Ito,odpt.Railway:JR-East.Itsukaichi,odpt.Railway:JR-East.Joban,odpt.Railway:JR-East.JobanLocal,odpt.Railway:JR-East.JobanRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:SaturdayHoliday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Kashima,odpt.Railway:JR-East.Kawagoe,odpt.Railway:JR-East.KeihinTohokuNegishi,odpt.Railway:JR-East.Keiyo&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:SaturdayHoliday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Kururi,odpt.Railway:JR-East.Musashino,odpt.Railway:JR-East.Nambu,odpt.Railway:JR-East.NambuBranch&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:SaturdayHoliday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Narita,odpt.Railway:JR-East.NaritaAbikoBranch,odpt.Railway:JR-East.NaritaAirportBranch,odpt.Railway:JR-East.Ome&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:SaturdayHoliday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Sagami,odpt.Railway:JR-East.SaikyoKawagoe,odpt.Railway:JR-East.ShonanShinjuku,odpt.Railway:JR-East.Sobu,odpt.Railway:JR-East.SobuRapid&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:SaturdayHoliday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.SotetsuDirect,odpt.Railway:JR-East.Sotobo,odpt.Railway:JR-East.Takasaki,odpt.Railway:JR-East.Tsurumi,odpt.Railway:JR-East.TsurumiOkawaBranch,odpt.Railway:JR-East.TsurumiUmiShibaurBranch&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:SaturdayHoliday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Togane,odpt.Railway:JR-East.Tokaido,odpt.Railway:JR-East.Uchibo,odpt.Railway:JR-East.Utsunomiya&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4',
        # 'https://api-tokyochallenge.odpt.org/api/v4/odpt:StationTimetable?odpt:calendar=odpt.Calendar:SaturdayHoliday&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.Yamanote,odpt.Railway:JR-East.Yokohama,odpt.Railway:JR-East.Yokosuka&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
    ]

#Requestsを利用してWebページをjson形式で取得する
headers = {"content-type": "application/json"}
JR_East_location_data = requests.get(JR_East_location, headers=headers).json() #現在の運行情報
JR_East_Timetable_data = [] #路線ごとjson情報をまとめて格納するリスト
for i in JR_East_Timetable:
    JR_East_Timetable_data.append(requests.get(i, headers=headers).json())



#遅延列車情報の取得
for line in range(len(JR_East_location_data)):
    #遅延している＋終着駅でないもの
    # if int(json.dumps(JR_East_location_data[line]['odpt:delay'])) > 0 and  json.dumps(JR_East_location_data[line]['odpt:toStation']) != "null":
    if int(json.dumps(JR_East_location_data[line]['odpt:delay'])) > 0:
        for i in range(len(JR_East_Timetable)):
            #遅延列車Numberの照合
            for train in range(len(JR_East_Timetable_data[i])):
                for trainNumber in range(len(JR_East_Timetable_data[i][train]['odpt:stationTimetableObject'])):
                    if json.dumps(JR_East_location_data[line]['odpt:trainNumber']) == json.dumps(JR_East_Timetable_data[i][train]['odpt:stationTimetableObject'][trainNumber]['odpt:trainNumber']):
                        if json.dumps(JR_East_location_data[line]['odpt:toStation']) == json.dumps(JR_East_Timetable_data[i][train]['odpt:station']):
                            #結果の表示
                            print("------------------------------------------------")
                            print(json.dumps(JR_East_location_data[line]['odpt:fromStation'].split('.')[-1]), json.dumps(JR_East_location_data[line]['odpt:toStation'].split('.')[-1]), json.dumps(JR_East_location_data[line]['odpt:trainNumber']))
                            delaytime=int(JR_East_location_data[line]['odpt:delay'])/60
                            # dt2 = datetime.strptime(JR_East_Timetable_data[i][train]['odpt:stationTimetableObject'][trainNumber]["odpt:departureTime"], '%H:%M') + datetime.timedelta(minutes=delaytime)
                            print("到着予定時刻:"+JR_East_Timetable_data[i][train]['odpt:stationTimetableObject'][trainNumber]["odpt:departureTime"]+"  %d分遅れ\n"%delaytime)

