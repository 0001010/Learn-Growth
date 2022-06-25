import requests
from bs4 import BeautifulSoup
import json

def crawling(station_code):

    url = 'http://www.seoulmetro.co.kr/kr/getStationInfo.do?action=time&stationId=' + str(station_code )
    # 서울메트로 접속후 post방식으로 크롤링

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
    else :
        print(response.status_code)

    filter_data = soup.find_all('a')
    filter_data2 = soup.find_all('li')

    types = [] # 급행인지 일반인지(일반, 급행)
    times = [] # 시간(시:분) 
    weeks = [] # 1: 평일, 2: 주말, 3: 공휴일
    destinations = [] # 도착지(ex. 청량리행, 천안행, 구로행 등)

 
    for i in filter_data:
        try:
            strings = i.get_text().split()
            times.append(i['time'] + ':' + strings[0][:-1])
            
            if i['week'] == '1':
                weeks.append('평일')
            elif i['week'] == '2':
                weeks.append('주말')
            else:
                weeks.append('공휴일')
                
            destinations.append(strings[-1][:-1])
            
        except:
            continue

    for j in filter_data2:
        try:
            if j['class'][0]=='G':
                types.append('일반')
            elif j['class'][0]=='D':
                types.append('급행')
        except:
            continue
    
        
    data_full = {'types' : types, 
                 'times' : times, 
                 'weeks' : weeks, 
                 'destinations' : destinations}
    
    data_full_json = json.dumps(data_full, indent = 4, ensure_ascii = False)

    return data_full_json

# 신창역 코드: 1408