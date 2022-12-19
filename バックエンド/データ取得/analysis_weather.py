import json
import glob
import datetime
import pandas as pd

# file open
start = datetime.datetime(2020, 11, 20).date()
end = datetime.datetime(2020, 11, 22).date()
# end = datetime.date.today()
data = []
i = 0
# while start != (end + datetime.timedelta(days = 1)):
while start != end:
    filename ='log_' + start.strftime('%Y%m%d') + '.json'
    with open(filename, 'r') as f:
        data.append(json.load(f))  
    start = start + datetime.timedelta(days = 1)
    i += 1

# l = glob.glob('log_*.json')
# data = []
# for filename in l:
#     with open(filename, 'r') as f:
#         data.append(json.load(f))
 
df_weather = pd.read_csv('data.csv',header=2,encoding="shift-jis")
df_weather = df_weather.drop(0)
df_weather = df_weather.rename(columns={'Unnamed: 0':'日付'})
df_weather_date = []
for i in df_weather['日付']:
    if i[-3:-1] == "24":
        i = i[:-3] + "00" + i[-1]
        tdatetime = datetime.datetime.strptime(i,'%Y年%m月%d日%H時')
        tdatetime = tdatetime + datetime.timedelta(days=1)
    else:
        tdatetime = datetime.datetime.strptime(i,'%Y年%m月%d日%H時')
    df_weather_date.append(tdatetime.strftime('%Y_%m_%d_%H'))

df_weather = df_weather.assign(date=df_weather_date)

for k in range(len(data)):
    for i in data[k]:
        for j in range(len(df_weather)):
            if df_weather.iat[j,7] == data[1][i]["date"][:13]:
                data[1][i]['Precipitation'] = df_weather.iat[j,1]
                data[1][i]['Temperature'] = df_weather.iat[j,2]
                data[1][i]['Snowfall'] = df_weather.iat[j,3]
                data[1][i]['SnowCover'] = df_weather.iat[j,4]
                data[1][i]['WindSpeed'] = df_weather.iat[j,5]
                data[1][i]['WindDirection'] = df_weather.iat[j,6]
                
print("{}".format(json.dumps(data[1],indent=4,ensure_ascii=False)))
