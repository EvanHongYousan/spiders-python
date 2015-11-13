__author__ = 'yantianyu'

import requests
from bs4 import BeautifulSoup
from collections import deque
import time
import codecs
import csv

queue = deque()
visited = set()

url = 'https://s.2.taobao.com/list/list.htm?q=ps4+%CE%D7%CA%A63&search_type=item&app=shopsearch'
# url='https://www.baidu.com'
# url = 'http://www.taobao.com/'

queue.append(url)
cnt = 0
blbnObjs = []

# response = requests.get(url)
# soup = BeautifulSoup(response.text)
# hrefs = soup.find(id='J_Pages').find_all('a')
# for items in hrefs:
# print('https:'+items['href'])

def getUrls(data):
    hrefs = data.find(id='J_Pages').find_all('a')
    tempurls = []
    for href in hrefs:
        tempurls.append('https:' + href['href'])
    return tempurls


def getBlbnObj(data):
    dataContainers = []
    data = data.find(id='J_ItemListsContainer')
    items = data.find(attrs={'class': 'item-lists'}).findAll(attrs={'class': 'item-idle'})
    for item in items:
        title = item.find('div', {'class': 'item-info'}).find('h4', {'class': 'item-title'}).find('a').contents[0]
        price = item.find('div', {'class': 'item-info'}).find('div', {'class': 'item-price'}).find('em').contents[0]
        url = 'http:' + item.find('div', {'class': 'item-info'}).find('h4', {'class': 'item-title'}).find('a')['href']
        dataContainers.append((title, price, url))
    return dataContainers


while queue:
    url = queue.popleft()

    visited.add(url)
    print('已经抓取:', str(cnt), '正在抓取 <---', url)
    print('当前len(visited)：', len(visited))
    print('当前len(queue):', len(queue))
    cnt += 1

    time.sleep(2)
    response = requests.get(url)
    soup = BeautifulSoup(response.text)

    blbnObjs.extend(getBlbnObj(soup))

    tempurls = getUrls(soup)
    for item in tempurls:
        if item not in visited and item not in queue:
            queue.append(item)
            print('加入队列--->', item)

with open('visited.txt', 'w') as f:
    temp = ''
    for visiI in visited:
        temp += visiI + '\n'
    f.write(str(temp))
    f.close()

print(blbnObjs)

with open('wicher3Objs.csv', 'w', newline='') as csvF:
    writer = csv.writer(csvF)
    writer.writerow(['标题', '价钱', '网址'])
    writer.writerows(blbnObjs)
    csvF.close()
