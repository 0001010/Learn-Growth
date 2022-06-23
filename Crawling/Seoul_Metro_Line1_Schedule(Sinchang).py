import requests
from bs4 import BeautifulSoup
import json


url = 'http://www.seoulmetro.co.kr/kr/getStationInfo.do?action=time&stationId=1408'
# url post방식으로 크롤링을 진행해야겠네...
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
else :
    print(response.status_code)

filter_data = soup.find_all('a')
 
for i in filter_data:
    try:
        print(i['time'], i.get_text())
    except:
        continue