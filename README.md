# 어린이 교통사고 분석

```
├── README.md
├── TaasCrawler.py
├── TrafficApiClient.py
├── data
│   ├── accident.json
│   ├── codes
│   │   ├── 구군코드.csv
│   │   ├── 시도코드.csv
│   │   └── 지역코드.csv
│   ├── kids-accident-27.json
└── requirements.txt
```

## 1. Requirements

```
pip install -r requirements.txt
```

## 2. TaasCrawler.py

[TAAS GIS 시스템](http://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN) 어린이사고 데이터 크롤러. 저장소 포크뜬 후 디렉토리에서 아래 명령어로 실행. `kids-accident-27.json` 파일에 데이터 저장. 권한승인이 된 아이디로 실행해주세요.

```bash
$ python TaasCrawler.py run --login_id=YOUR-ID --login_pwd=YOUR-PASSWORD 
```

## 3. TrafficApiClient.py

[사망교통사고 API](https://www.data.go.kr/data/15059126/openapi.do) 클라이언트. 키 받아서 txt 파일로 저장한 후 아래 명령어로 실행. `accident.json` 파일에 저장됨.

```bash
$ python TrafficApiClinet.py run --key_path=YOUR-KEY-PATH
```