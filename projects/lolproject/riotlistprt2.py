from riotwatcher import LolWatcher, ApiError
import os.path




apikey = 'RGAPI-65f38914-9123-4819-81e5-efb770ae5f4b'
watcher = LolWatcher(api_key= apikey)

#Get puuID's from the summoner list.
counter = 0
file_exists = os.path.exists('lolpuuidlist.txt')
if file_exists == False:
    print('No PuuID List File Detected. Generating new one')
    puuidlist = []
    f= open('lolsummonerlist.txt','r')
    for line in f:
        idlist=(line.split(','))
    f.close()
    smallidlist = idlist[50:-1]
    with open('lolpuuidlist.txt','w', encoding='utf-8') as f:
        for i in smallidlist:
            summonerinfo = watcher._summoner.by_id(region='na1', encrypted_summoner_id=i)
            f.write(summonerinfo['puuid'])
            f.write(',')
            counter = counter + 1
            txt = 'Completed {fcounter} entry'.format(fcounter=counter)
            print(txt)
        f.close()