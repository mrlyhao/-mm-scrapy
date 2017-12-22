import requests
from bs4 import BeautifulSoup
import os
import re

pindaonamelist= []
pindaourllist = []
mmnamelist = []
mmurllist = []
DIR_PATH = '/mm'


def gethtmltext(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return  '产生异常'

def getUrllist(startUrl):
    global URL_LIST
    URL_LIST = ''
    try:
        soup = BeautifulSoup(startUrl,'html.parser')
        infos = soup.select('.sp-index-listc span a')
        for info in infos:
            pindaourllist.append(info.get('href'))
            pindaonamelist.append(info.text.strip())
            pindaourl = info.get('href')
            path = info.text.strip()
            URL_LIST = DIR_PATH +'/' + path
            exists = os.path.exists(URL_LIST)
            if not exists:
                os.makedirs(URL_LIST)
            getMMurllist(gethtmltext(pindaourl))
        return pindaourllist
    except:
        return'cuowu'

def getMMurllist(pindaourl):
    global dir_path
    try:
        soup = BeautifulSoup(pindaourl,'html.parser')
        infos = soup.select('.title span a')
        for info in infos:
            mmurllist.append(info.get('href'))
            mmnamelist.append(info.text.strip())
            mmurl = info.get('href')
            print(mmurl)
            path = info.text.strip()
            dir_path = URL_LIST +'/' + path
            exists = os.path.exists(dir_path)
            if not exists:
                os.makedirs(dir_path)
            getInfo(mmurl)
        return mmurllist
    except:
        return'cuowu1'

def getInfo(mmurl):
    try:
        info = gethtmltext(mmurl)
        pattern = re.compile('<li><a>共(.* ?).*?页:',re.S)
        yema = re.findall(pattern,info)
        if yema:
            for i in range(1,int(yema[0])):
                url = mmurl.split('.h')
                url.insert(1,'_')
                url.insert(2,str(i))
                url.insert(3,'.h')
                url = (''.join(url))
                print(url,i)
                a = gethtmltext(url)
                soup = BeautifulSoup(gethtmltext(url),'html.parser')
                mminfos = soup.select('.arcBody p a img')
                for mminfo in mminfos:
                    content = mminfo.get('src')
                    name = content.split('/')[-1]
                    path = dir_path +'/' + name
                    r = requests.get(content)
                    print(path)
                    f= open(path,'wb')
                    f.write(r.content)
                    f.close()

    except:
        return'huoqucuowu'

def main():
    url = 'http://www.5442.com/special/'
    starturl = gethtmltext(url)
    getUrllist(starturl)


main()

