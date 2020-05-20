import requests
import pandas as pd
import json
import fire
from tqdm import tqdm

class TaasCrawler:
    
    def __init__(self):
        self.url = 'http://taas.koroad.or.kr/gis/srh/ash/selectAccidentInfo.do'
        self.headers = {
            'Host': 'taas.koroad.or.kr',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Cookie':'Cookie: JSESSIONID=j1Vt21OrZ7dQ18QXrcWqbs1jyhgH517EiXvLkmvfaIt7R7YS43inXXnom313U21g.kr-ph-was1_servlet_engine1; TAASJSESSIONID=ZOXAAdjq2eGFLqRaj4a9CDaghCa8XBfriH9ZZwEORcIfM8a548eMOLcHvozx6yTw.amV1c19kb21haW4vc2VydmVyMQ==',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'http://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_ABS',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.payload = {
            "searchType":"00",
            "pageIndex":"1",
            "zoneYn":"false",
            "engnCode":"00",
            # 검색 시작 연도
            "startAcdntYear":"2007",
            # 검색 종료 연도
            "endAcdntYear":"2018",
            "acdntGaeCode":"01",
            # 사고 유형: 차대사람, 차대차 ...
            "acdntCode":"110,120,130,140,199,210,220,221,235,231,232,299,310,321,322,330,340,341,342,399,400,410,420,430,499" 
        }
            
    def request_and_parse(self, searchSimpleCondition):
        result = []
        print(f"사고유형: {searchSimpleCondition}")
        for sido in tqdm(range(11, 27)):
            self.payload["searchSimpleCondition"] = searchSimpleCondition # 사고유형: 여린이사고(27), 어린이보호구역 내 어린이사고(29)
            self.payload['legaldongCode'] = str(sido) + "%"
            res = requests.post(self.url, data=json.dumps(self.payload), headers=self.headers)
            result += res.json()['resultValue']['accidentInfoList']
        print(f"{len(result)} 건의 데이터를 수집하였습니다. \n")
        return result
    
    def run(self):
        # 사고부문: 어린이사고(27), 어린이구역내어린이사고(29)
        for searchSimpleCondition in ["27", "29"]:
            json_obj = self.request_and_parse(searchSimpleCondition)
            filepath = f"data/kids-accident-{searchSimpleCondition}.json"
            with open(filepath, "w") as f:
                json.dump(json_obj, f)

if __name__=='__main__':
    fire.Fire(TaasCrawler)