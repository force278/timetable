import requests



r = requests.get(f'https://tt.chuvsu.ru/export/getgroups?user=guest')
r = r.json()

f = open('text.txt', 'w')

for fac in r.keys():
    for fo in r[fac].keys():
        for level in r[fac][fo].keys():
            for course in r[fac][fo][level].keys():
                for i in r[fac][fo][level][course]:
                    #f.write(str(r[fac][fo][level][course]).lower())
                    f.write(str({v:int(k) for k, v in r[fac][fo][level][course].items()}).lower())
f.close()
                    
                
    