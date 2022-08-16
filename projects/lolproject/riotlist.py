from riotwatcher import LolWatcher, ApiError
import os.path




apikey = 'RGAPI-5471186a-5361-4cbf-8c71-23793b3938a5'
watcher = LolWatcher(api_key= apikey)

# Generating list of Diamond I Solo Players
# file_exists = os.path.exists('C:/Users/conrad.cruz/OneDrive - Aldevron/Documents/Python Scripts/Other/lolsummonerlist.txt')
file_exists = os.path.exists('lolsummonerlist.txt')
if file_exists == False:
    print("No Summoner List file detected. Generating new one")
    entrylist = watcher.league.entries(region='na1',queue='RANKED_SOLO_5x5', tier='DIAMOND',division='I')
    with open('lolsummonerlist.txt','w', encoding='utf-8') as f:
        for i in entrylist:
            f.write(i['summonerId'])
            f.write(',')
    f.close()


