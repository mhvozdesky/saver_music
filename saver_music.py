import requests
import re
from tkinter.filedialog import askdirectory
import os
import os.path
import sys

my_dict_1 = {'do': 'search',
           'subaction': 'search',
           'search_start': '0',
           'full_search': '0',
           'result_from': '1',
           'story': ''
           }

headers_1 = {'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'uk,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Content-Length': '103',
           'Content-Type': r'application/x-www-form-urlencoded',
           'Cookie': r'__cfduid=d0b7e44e3cec68cd918db93cd055535d81581607661; PHPSESSID=1636bf61f6915e269b5b4dd1151305c2; _ym_uid=1581607664154607041; _ym_d=1581607664; _ym_isad=1',
           'Host': 'pesnigoo.ru',
           'Origin': r'http://pesnigoo.ru',
           'Referer': r'http://pesnigoo.ru/12544-queen-dont-stop-me-now.html',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': r'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
           }

#https://z1.fm/mp3/search?keywords=Battle+Beast-Out+of+Control

headers_2 = {'authority': 'z1.fm',
           'method': 'GET',
           'path': r'/mp3/search?keywords=Battle+Beast-Out+of+Control',
           'scheme': 'http',
           'accept': r'*/*',
           'accept-encoding': 'gzip, deflate',
           'accept-language': r'uk,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6',
           'cookie': r'__cfduid=d60d152608df70e79cd6752bbd251ab5c1554273538; zvAuth=1; zvLang=0; _zvMobile_=0; PHPSESSID=k77pt5hentk4tp7a7comm91d60; ZvcurrentVolume=100',
           'if-modified-since': 'Tue, 18 Feb 2020 10:20:00 GMT',
           'referer': r'https://z1.fm/mp3/search?keywords=Battle+Beast-Out+of+Control',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'same-origin',
           'user-agent': r'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
           'x-pjax': 'true',
           'x-requested-with': 'XMLHttpRequest'
           }


#payload = {'keywords': 'Battle Beast-Out of Control'}
#r = requests.get("https://z1.fm/mp3/search", params=payload, headers = headers, verify=False)

def initial_checks(our_dir):
    #log dir
    if os.path.exists(r'{}/logDir'.format(our_dir)) == False:
        os.makedirs(r'{}/logDir'.format(our_dir))
        
    #file of songs
    if os.path.exists(r'{}/logDir/list_songs.txt'.format(our_dir)) == False:
        print('Need a file with songs')
        sys.exit()
    
    #file of bad songs
    file = open(r'{}/logDir/bad_songs.txt'.format(our_dir), 'w')
    file.close()

def parse_dock(text):
    return re.findall(r'data-track="(\S+)">\n', text)

def make_log(query):
    with open(bad_songs, 'a') as file:
        file.write(query + '\n')

def make_name(query):
    for z in range(100):
        s = str(z)
        if s == '0':
            s = ''
        
        #check if there is a file
        if os.path.exists(r'{0}/{1}{2}.mp3'.format(our_dir, query, s)) == False:
            return r'{0}/{1}{2}.mp3'.format(our_dir, query, s)
    
    return 'ERROR'    
            

def request_1(query, executor, song):
    my_dict_1['story'] = query
    
    req = requests.post(r'http://pesnigoo.ru/index.php?do=search', data = my_dict_1, headers = headers_1)
    if req.status_code == 200:
        link = parse_dock(req.text)
        if link == []: # there is no song
            return 'bad result'
        else:
            #try to download
            r = requests.get(link[0], stream=True)
            if r.status_code == 200:
                name_file = make_name(query)
                with open(name_file, 'wb') as file:
                    file.write(r.content)
            else:
                return 'bad result'
    else:
        return 'bad result'

def read_songs(our_work_file):
    with open(our_work_file, 'r', encoding='utf-8') as file:
        for string in file:
            string = string.strip('\ufeff')
            string = string.strip('\n')
            query, executor, song = string, string.split('-')[0], string.split('-')[1]
            
            #request 1
            request_1(query, executor, song)

if __name__ == '__main__':
    #our_dir = askdirectory()
    our_dir = r'd:\Users\maksim.gvozdetskiy\Desktop\saver_music'
    if our_dir == '':
        sys.exit()
        
    initial_checks(our_dir)
    our_work_file = r'{}/logDir/list_songs.txt'.format(our_dir)
    bad_songs = r'{}/logDir/bad_songs.txt'.format(our_dir)
    
    #read our file with songs
    read_songs(our_work_file)