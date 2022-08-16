from riotwatcher import LolWatcher, ApiError
import os.path


apikey = 'RGAPI-65f38914-9123-4819-81e5-efb770ae5f4b'
watcher = LolWatcher(api_key= apikey)

#Filter ranked matches from our puuid list
file_exists = os.path.exists('lolmatchlist.txt')
if file_exists == False:
    print('No Match List File Detected. Generating new one')
    f = open('lolpuuidlist2.txt', 'r')
    for line in f:
        puuidlist = line.split(',')
    f.close()
    f = open('lolmatchlist.txt','w')
    for i in puuidlist:
        try:
            matchids = watcher.match.matchlist_by_puuid(region='americas', count=5,puuid=i ,queue=420, type='ranked')
            for x in matchids:
                f.write(x)
                f.write(',')
        except:
            continue
    f.close()
