import requests
from bs4 import BeautifulSoup
import json


url = 'http://www.seoulmetro.co.kr/kr/getStationInfo.do?action=time&stationId=1408' # url post방식으로 크롤링을 진행해야겠네...
# 서울메트로 접속후 post방식으로 크롤링

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
else :
    print(response.status_code)

filter_data = soup.find_all('a')
filter_data2 = soup.find_all('li')

types = [] # 급행인지 일반인지(G: 일반, D: 급행)
hours = [] # 시간 
 
for i in filter_data:
    try:
        hours.append(i['time'])
        print( i.get_text(), i['week'])
    except:
        continue

for j in filter_data2:
    try:
        if j['class'][0]=='G' or j['class'][0]=='D':
            types.extend(j['class'])
    except:
        continue