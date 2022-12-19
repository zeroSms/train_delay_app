import requests
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt

def Station_number(station_Title): #駅番号変換
    for line in range(len(JR_East_Route_data[0]['odpt:stationOrder'])):
        if (station_Title == JR_East_Route_data[0]['odpt:stationOrder'][line]['odpt:stationTitle']['en'].replace("-", "")):
            return JR_East_Route_data[0]['odpt:stationOrder'][line]['odpt:index']
        
def TimeScheme(ttime,Time_list):
    if ttime > datetime.datetime(1900,1,1,hour=4):
        Time_list.append(ttime)
    else:
        Time_list.append((ttime + datetime.timedelta(days=1)))

def Diagram(JR_East_TrainTimeTable_data):
    plt.figure(figsize=(50,10))
    plt.xlabel('Time')
    plt.ylabel('Station')
    plt.grid()
    for train in JR_East_TrainTimeTable_data:
        Time_list = []
        Station_list = []
        for line in train['odpt:trainTimetableObject']:
            if 'odpt:departureTime' in line and 'odpt:departureStation' in line:
                DepartureTime = datetime.datetime.strptime(line['odpt:departureTime'],'%H:%M')
                TimeScheme(DepartureTime,Time_list)
                Station_list.append(Station_number(line['odpt:departureStation'][31:]))
            elif 'odpt:arrivalTime' in line and 'odpt:arrivalStation' in line:
                ArrivalTime = datetime.datetime.strptime(line['odpt:arrivalTime'],'%H:%M')
                TimeScheme(ArrivalTime,Time_list)
                Station_list.append(Station_number(line['odpt:arrivalStation'][31:]))                       
        plt.plot(Time_list,Station_list)
               
    plt.show()
        
JR_East_TrainTimeTable_Weekday_Outbound = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainTimetable?odpt:operator=odpt.Operator:JR-East'\
                                            '&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:calendar=odpt.Calendar:Weekday&'\
                                            'odpt:railDirection=odpt.RailDirection:Outbound'\
                                            '&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_TrainTimeTable_Weekday_Inbound = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainTimetable?odpt:operator=odpt.Operator:JR-East'\
                                            '&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:calendar=odpt.Calendar:Weekday&'\
                                            'odpt:railDirection=odpt.RailDirection:Inbound'\
                                            '&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_TrainTimeTable_Saturdayholiday_Outbound = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainTimetable?odpt:operator=odpt.Operator:JR-East'\
                                                    '&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:calendar=odpt.Calendar:SaturdayHoliday&'\
                                                    'odpt:railDirection=odpt.RailDirection:Outbound'\
                                                    '&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_TrainTimeTable_Saturdayholiday_Inbound = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:TrainTimetable?odpt:operator=odpt.Operator:JR-East'\
                                                    '&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:calendar=odpt.Calendar:SaturdayHoliday&'\
                                                    'odpt:railDirection=odpt.RailDirection:Inbound'\
                                                    '&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
JR_East_Route = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:Railway?odpt:operator=odpt.Operator:JR-East&odpt:railwayTitle.en=Chuo%20Rapid%20Line&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'

#Requestsを利用してWebページをjson形式で取得する
headers = {"content-type": "application/json"}

JR_East_TrainTimeTable_Weekday_Outbound_data = requests.get(JR_East_TrainTimeTable_Weekday_Outbound, headers=headers).json() 
JR_East_TrainTimeTable_Weekday_Inbound_data = requests.get(JR_East_TrainTimeTable_Weekday_Inbound, headers=headers).json() 
JR_East_TrainTimeTable_Saturdayholiday_Outbound_data = requests.get(JR_East_TrainTimeTable_Saturdayholiday_Outbound, headers=headers).json() 
JR_East_TrainTimeTable_Saturdayholiday_Inbound_data = requests.get(JR_East_TrainTimeTable_Saturdayholiday_Inbound, headers=headers).json() 
JR_East_Route_data = requests.get(JR_East_Route, headers=headers).json()

#print("{}".format(json.dumps(JR_East_TrainTimeTable_data[],indent=4,ensure_ascii=False)))
#print(datetime.datetime.strptime(JR_East_TrainTimeTable_data[0]['odpt:trainTimetableObject'][0]['odpt:departureTime'],'%H:%M').time())

Diagram(JR_East_TrainTimeTable_Weekday_Outbound_data)
Diagram(JR_East_TrainTimeTable_Weekday_Inbound_data)
Diagram(JR_East_TrainTimeTable_Saturdayholiday_Outbound_data)
Diagram(JR_East_TrainTimeTable_Saturdayholiday_Inbound_data)
