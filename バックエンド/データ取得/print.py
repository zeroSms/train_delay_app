import requests
import json
import datetime
import jpholiday
import time
import collections as cl
from matplotlib import pyplot as plt


start = datetime.datetime(2020, 11, 20)
end = datetime.datetime(2020, 11, 23)
json_data = {}
i = 0
while start != (end+ datetime.timedelta(days = 1)):
    filename ='log_' + start.strftime('%Y%m%d') + '.json'
    with open(filename, 'r') as f:
        json_data[i] = json.load(f)     
    start = start + datetime.timedelta(days = 1)
    i += 1

print("{}".format(json.dumps(json_data, indent=4, ensure_ascii=False)))

#import matplotlib as mpl
#mpl.font_manager._rebuild()

print([0]*3)
