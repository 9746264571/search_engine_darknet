import socket
import socks
import http.client
import requests
import pymongo
import re
import shutil
import sys
import urllib.request
import selenium.webdriver as webdriver
from pymongo import MongoClient
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
list(socket.SocketKind)
def get_results(search_term):
    urll ="https://ahmia.fi"
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type',1)
    profile.set_preference('network.proxy.socks','127.0.0.1')
    profile.set_preference('network.proxy.socks_port',9150)
    browser = webdriver.Firefox(profile)
    browser.get(urll)
    search_box = browser.find_element_by_id("query")
    search_box.send_keys(search_term)
    search_box.submit()
    try:
        linkz = browser.find_elements_by_xpath("//ol[@class='searchResults']//cite")
    except:
        linkz = browser.find_elements_by_path("//cite")
    resl = []
    for lin in linkz:
        print(lin)
        resl.append(lin)
    browser.close()
    return resl
def connecttor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050 , True)
    s= socket.socket()
    s.setblocking(False)
    s= socks.socksocket

def main():
    connecttor()
    print("connected to tor...")
    client = MongoClient()
    print("connected to database...")
    es = Elasticsearch([{'host' : 'localhost', 'port' :9200}])
    print("connected to search...")
    db = client["darklinks"]
    links = db.links
    #get_results("dog")
   # x= links.delete_one({'url' : 'http://silkroad7rn2puhj.onion/'})
    #y= links.delete_many({'url' : 'http://midcity7ccxtrzhn.onion/'})
    #print(x)
    # print(y)
    #links.insert_one({'url':'http://silkroad7rn2puhj.onion/'})
    #try:
    #links.insert_one({'url':'http://midcity7ccxtrzhn.onion/'})
    #except Exception as e:
    #    print(str(e))
    session = requests.session()
    session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
   # x = "http://cavetord6bosm3sl.onion/images/catalog/medium/ea8ed97ca2da70bcba34ec3b39ebde60.jpg"
    #ll = session.get(x, stream = True)
    
    #with open('img.png','wb') as out_file:
        #shutil.copyfileobj(ll.raw,out_file)
    #del ll
    linkslist = []
    print(1)
    while True:
        for x in links.find({},{"_id":0,"url":1}):
            print(2)
            for key,val in x.items():
               try:
                   response = session.get(val, timeout = 20)
                   #print(response.text)
               except socket.timeout:
                   errno, errstr = sys.exec_info()[:2]
                   if errno == socket.timeout:
                       print(val + ' timed out ---')
                       continue
               except :
                       print(val + ' timed out --- ')
                       #links.delete_many({ 'url' : val})
                       continue
               print(response.status_code)
               if response.status_code == 200:
                   soup= BeautifulSoup(response.text, 'html.parser')
                   try:
                       print('Title:')
                       title = soup.title.get_text()
                       print(title)
                       print('Links:')
                       x = soup.find_all('a', href = True)
                       for ll in soup.find_all('a',attrs={'href':re.compile("!^http://")}):
                           links.create_index("url",unique = True)
                           uu = ll.get('href')
                           try:
                               print(val+"/"+uu)
                               links.insert_one({'url' :val + "/" +uu})
                           except:
                               print('duplicate...')
                               continue
                       for link in soup.find_all('a', attrs={'href':re.compile("^http://")}):
                           links.create_index("url",unique = True)
                           l = link.get('href')
                           try:
                               #links.create_index("url",unique = True)
                               links.insert_one({'url' :l})
                               u = l
                           except:
                               print('duplicate..')
                               continue
               #for link in soup.find_all('a'):
                #  print(3)
                #  s=link.get('href')
                #  if 'http' or 'https' in s:
                #      links.insert_one({'url' :s[link]})
                #  else:
                #      linkslist.append(s[link])
           
                       print(linkslist)
                       print('Text:')
                       s = soup.get_text()
                       print(s)
                       html= soup.prettify() 
                       print(html)
                       meta = soup.find_all('meta')
                       e={
                           "url" :l,
                           "title": title,              
                           "html": html,
                           "meta": meta,
                           "plain":s
                       }
                       print(4)
                       es.index(index = 'darklinks', doc_type = 'data',body =e)
                   except:
                       continue    
               else:
                   continue 

if __name__ == "__main__":
    main()

