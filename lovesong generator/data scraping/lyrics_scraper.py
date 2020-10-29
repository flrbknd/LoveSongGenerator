# -*- coding: utf-8 -*-
"""
Latest version: 23.10.2020

@author: bkndflr
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
import random
import os

user_agents = [
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
]

def get_header(agents):
    """Disguises browser for requests"""
    return {'User-agent': random.choice(agents)}

def simplify_chars(text):
    """cleans data from characters that are not url-friendly"""
    text = str(text)
    text = text.lower()
    for char in ["'", "(",")", ".", "!", "?", "*", " ", "  ", ",", "-"]:
        text = text.replace(char, "")
    return text

def generatelinks(excel_file): #CHANGE BACK!!
    """generates lyrics url on azlyrics.com based on artist name, title"""
    lovesongs_df = pd.read_excel(excel_file)
    url_list = []
    base_url = 'https://www.azlyrics.com/lyrics'
    for i in range(len(lovesongs_df)):
        artist = simplify_chars(lovesongs_df['artist'][i])
        title = simplify_chars(lovesongs_df['title'][i])
        url_list.append('{}/{}/{}.html'.format(base_url, artist, title))
        #creating alternative versions below for handling collaborations/inconsistent listings
        if '&' in artist: 
            artist_v2 = artist[:artist.index("&")]
            artist_v3 = artist[artist.index("&")+1:]
            url_list.append('{}/{}/{}.html'.format(base_url, artist_v2, title))
            url_list.append('{}/{}/{}.html'.format(base_url, artist_v3, title))
            
        if artist [:3] == 'the':
            artist_v4 = artist[3:]
            url_list.append('{}/{}/{}.html'.format(base_url, artist_v4, title))          
    return url_list

    
def getlyrics(url):
    """Scrapes lyrics from azlyrics.com"""
    resp = requests.get(url=url)
    doc = resp.content
    soup = BeautifulSoup(doc, 'html.parser')
    soup.find_all("div", class_="col-xs-12 col-lg-8 text-center")
    main_content_class = soup.find("div", class_="col-xs-12 col-lg-8 text-center")
    main_content_divs = main_content_class.find_all("div")
    lyrics = main_content_divs[5].get_text()
    sleep(random.randint(5, 25)) # for avoiding azlyrics.com to block me
    return lyrics

def savelyrics(lyrics, url):
    """Saves lyrics to dedicated folder"""
    if not os.path.exists('Lovesong Collection'):
        os.makedirs('Lovesong Collection')
    loc = './Lovesong Collection/'
    base_url = 'https://www.azlyrics.com/lyrics/' #specify if not for azlyrics.com!
    filename = url.replace(base_url, '')
    filename = filename.replace('/', '_')
    filename = filename.replace('.html', '.txt')
    f = open(loc+filename, "w")
    f.write(lyrics)
    f.close()

    
url_list = generatelinks('lovesong_list_2.xlsx')
for url in url_list:
    try:
        text = getlyrics(url)
        savelyrics(text, url)
    except:
        print('Error:', url)






    




