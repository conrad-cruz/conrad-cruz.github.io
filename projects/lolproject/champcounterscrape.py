
import urllib.request, urllib.parse, urllib.error
import ssl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sqlite3

conn = sqlite3.connect('Champ_Counter.sqlite3')
cur = conn.cursor()

cur.executescript('''CREATE TABLE IF NOT EXISTS champcounter_table(
    champion text UNIQUE, 
    bestcounter text,
    worstcounter text 
    )

        ''')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

site = 'https://www.counterstats.net/'
driver = webdriver.Chrome('C:/Users/conrad.cruz/OneDrive - Aldevron/Documents/Python Scripts/chromedriver100/chromedriver')
driver.get(site)

grandElement = driver.find_element(By.ID,('champions'))

#NameElement gives list of Champ names
nameElement = grandElement.find_elements(By.CLASS_NAME,('name'))
for champ in nameElement:
    champ = champ.text
    champ = champ.lower()
    if champ == 'nunu & willump':
        champ = 'nunu-willump'
    champ = champ.replace(' ','-')
    champ = champ.replace('\'','')
    champ = champ.replace('.','')
    champ = champ.strip()
    champid = grandElement.find_element(By.ID,(champ))

    BestElement = champid.find_element(By.CLASS_NAME,('best-wrap'))
    BestElementimg = BestElement.find_element(By.TAG_NAME,('img'))
    BestElementtext = BestElementimg.get_attribute('src')
    cleanbesttext = BestElementtext.replace('https://www.mobafire.com/images/champion/square/','')
    cleanbesttext = cleanbesttext.replace('-60x.png','')

    WorstElement = champid.find_element(By.CLASS_NAME,('worst-wrap'))
    WorstElementimg = WorstElement.find_element(By.TAG_NAME,('img'))
    WorstElementtext = WorstElementimg.get_attribute('src')
    cleanworsttext = WorstElementtext.replace('https://www.mobafire.com/images/champion/square/','')
    cleanworsttext = cleanworsttext.replace('-60x.png','')

    cur.execute('''INSERT OR IGNORE INTO champcounter_table (champion, bestcounter, worstcounter) VALUES (?,?,?)''', (champ,cleanbesttext,cleanworsttext))

    conn.commit()