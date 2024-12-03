import json
from constants import * 


inverse_dic={}
file = open("result.txt", "w")
for key,val in CHGAU_GROUPS.items():
    if 'EF' == val['url']:
        inverse_dic[val['groupid']] = key
        file.write(f"'{val['groupid']}':'{key}',\n")
file.close()

