import pandas as pd
import requests
import os
import json
import fire
from math import ceil
from tqdm import tqdm

class TrafficApiClient:
    def get_and_parse(self, url, key, searchYear, siDo, guGun):
        uri = url + f"?ServiceKey={key}&searchYear={searchYear}&siDo={siDo}&guGun={guGun}&type=json&numOfRows=1000&pageNo=1"
        res = requests.get(uri)
        if res.ok:
            try:
                json = res.json()
                result = []
                result += json['items']['item']
                n_pages = ceil(json['totalCount']/100)
                if n_pages >= 2:
                    for i in range(2, n_pages+1):
                        uri = url + f"?ServiceKey={key}&searchYear={searchYear}&siDo={siDo}&guGun={guGun}&type=json&numOfRows=1000&pageNo={i}"
                        res = requests.get(uri)
                        result += res.json()['items']['item']  
            except:
                print(f"파싱 에러 발생: {uri}")
        else:
            print(f"응답이 유효하지 않습니다: {res.__str__()}")
        return result
    
    def run(self, key_path, code_fname='data/codes/지역코드.csv', start=2012, end=2017):
        codes = pd.read_csv(code_fname)
        url = 'http://apis.data.go.kr/B552061/trafficAccidentDeath/getRestTrafficAccidentDeath'

        with open(key_path, 'r') as f:
        	key = f.read().strip()
        
        result = []
        for searchYear in range(start, end+1):
        	print(f"{searchYear}년 데이터를 조회합니다.")
        	n_data = 0
	        for i in tqdm(range(codes.shape[0])):
	            siDo, guGun = codes.시도코드.values[i], codes.구군코드.values[i]
	            json_obj = self.get_and_parse(url, key, searchYear, siDo, guGun)
	            result += json_obj
	            n_data += len(json_obj)
	        print(f"{searchYear}년의 데이터는 총 {n_data}건입니다.")
        with open('data/accident.json', 'w') as f:
            json.dump(result, f)

if __name__ == "__main__":
    fire.Fire(TrafficApiClient)