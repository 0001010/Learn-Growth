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
    

    return types, times, weeks, destinations

def real_time_subway_location(location):
    url = 'http://swopenAPI.seoul.go.kr/api/subway/544f6a5a766b6b73313036426657754f/json/realtimeStationArrival/0/10/' + location

    response = requests.get(url)
    src = response.text
    src_json  = json.loads(src)

    updnline = [] # 상행, 하행
    bstatnNm = [] # 도착역
    cur_loc = [] # 현재 위치
    cur_loc2 = []
    arvlCd = []


    for row in src_json['realtimeArrivalList']:
        updnline.append(row['updnLine'])
        bstatnNm.append(row['bstatnNm'])
        cur_loc2.append(row['arvlMsg2'])
        cur_loc.append(row['arvlMsg3'])
        arvlCd.append(row['arvlCd'])
        
    return updnline, bstatnNm, cur_loc, arvlCd


def main():
    crawling_data = crawling(1408)
    api_data = real_time_subway_location('신창')
    
    crawling_data_json = {
        'types' : crawling_data[0],
        'times' : crawling_data[1],
        'weeks' : crawling_data[2],
        'destinations' : crawling_data[3]
        }
    
    api_data_json = {
        'updnline' : api_data[0],
        'bstatnNm' : api_data[1],
        'cur_loc' : api_data[2],
        'arvlCd' : api_data[3]
        }
    
    crawling_data_json = json.dumps(crawling_data_json, indent = 4, ensure_ascii = False)
    api_data_json = json.dumps(api_data_json, indent = 4, ensure_ascii = False)
    
    return crawling_data_json, api_data_json


if __name__ == "__main__":
    main()
# 신창역 코드: 1408