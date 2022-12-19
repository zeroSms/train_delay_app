import json

with open('Train-Higashinihon.json', 'r', encoding='utf-8') as file:
    F_load = json.load(file)

for line in range(len(F_load)):
    print(F_load[line]['odpt:railway'], ':', F_load[line]['odpt:delay'], '\n')



