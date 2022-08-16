from riotwatcher import LolWatcher, ApiError
import os.path
import sqlite3

apikey = 'RGAPI-2423cddf-e9bc-494b-84ad-6bea26b180b8'
watcher = LolWatcher(api_key= apikey)

#Make Database

f = open('C://Users//cruzc//Documents//Python Scripts//LoL Project//lolmatchlistcombined.txt','r')
for line in f:
    matchlist = line.split(',')
f.close()

conn = sqlite3.connect('LOL_Match_Champion_Database.sqlite3')
cur = conn.cursor()

cur.executescript('''CREATE TABLE IF NOT EXISTS matchid_table( 
        match TEXT UNIQUE,
        match_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE);

        CREATE TABLE IF NOT EXISTS champion_table
        (champion_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        champion TEXT UNIQUE
        );


        CREATE TABLE IF NOT EXISTS teamPosition_table(
            teamPosition_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            teamPosition TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS match_summary(
            summonerName TEXT,
            teamId INTEGER,
            match_id INTEGER,
            champion_id INTEGER,
            kills INTEGER,
            assists INTEGER, 
            deaths INTEGER,
            goldEarned INTEGER,
            neutralMinionsKilled INTEGER,
            totalMinionsKilled INTEGER,
            physicalDamageDealt INTEGER,
            magicDamageDealt INTEGER,
            teamPosition_id INTEGER,
            win INTEGER,
            FOREIGN KEY (match_id) REFERENCES matchid_table(match_id)
            FOREIGN KEY (champion_id) REFERENCES champion_table(champion_id)
            FOREIGN KEY (teamPosition_id) REFERENCES teamPosition_table(teamPosition_id)
        )
        ''')

size = len(matchlist)
halfsize = size//2 
quartersize = halfsize//2

for x in range(halfsize+1,size,1):
    try:
        matchdata = watcher.match.by_id(region='americas',match_id=matchlist[x])
    except:
        continue
    matchid = matchlist[x]


    cur.execute('''INSERT OR REPLACE INTO matchid_table (match) VALUES (?) ''', (matchid,))
    cur.execute('''SELECT match_id FROM matchid_table WHERE match = ?''', (matchid,))
    match_id = cur.fetchone()[0]

    conn.commit()
    print('Starting Entry', x)
    for i in range(0,10,1):
        
        summonerName = matchdata['info']['participants'][i]['summonerName']
        teamId = matchdata['info']['participants'][i]['teamId']
        championName = matchdata['info']['participants'][i]['championName']
        kills = matchdata['info']['participants'][i]['kills']
        assists = matchdata['info']['participants'][i]['assists']
        deaths = matchdata['info']['participants'][i]['deaths']
        teamPosition = matchdata['info']['participants'][i]['teamPosition'] #TOP MID JUNGLE BOT UTILITY APEX NONE (Want to use this?)
        goldEarned =matchdata['info']['participants'][i]['goldEarned']
        neutralMinionsKilled = matchdata['info']['participants'][i]['neutralMinionsKilled']
        totalMinionsKilled = matchdata['info']['participants'][i]['totalMinionsKilled']
        physicalDamageDealt = matchdata['info']['participants'][i]['physicalDamageDealt']
        magicDamageDealt = matchdata['info']['participants'][i]['magicDamageDealt']
        win = matchdata['info']['participants'][i]['win']


        cur.execute('''INSERT OR IGNORE INTO champion_table (champion) VALUES (?)''', (championName,))
        cur.execute('''SELECT champion_id FROM champion_table WHERE champion = ?''', (championName,))
        champion_id = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO teamPosition_table (teamPosition) VALUES (?)''', (teamPosition,))
        cur.execute('''SELECT teamPosition_id FROM teamPosition_table WHERE teamPosition = ?''', (teamPosition,))
        teamPosition_id = cur.fetchone()[0]
        conn.commit()

        
        cur.execute('''INSERT INTO match_summary (summonerName, teamId, kills, assists, deaths, goldEarned,
        neutralMinionsKilled,totalMinionsKilled,physicalDamageDealt,magicDamageDealt,teamPosition_id, match_id,champion_id,win) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''', 
        (summonerName,teamId, kills, assists, deaths, goldEarned, neutralMinionsKilled, totalMinionsKilled,physicalDamageDealt,magicDamageDealt,teamPosition_id,match_id, champion_id,win))
        conn.commit()
        
    