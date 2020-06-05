# 어린이 교통사고 분석

```bash
├── README.md
├── TaasCrawler.py
├── TrafficApiClient.py
├── data
│   ├── codes
│   │   ├── 구군코드.csv
│   │   ├── 시도코드.csv
│   │   └── 지역코드.csv
│   ├── accident.json
│   ├── kids-accident-27.json
│   ├── kids-accident-29.json
│   └── kids-accident.geojson
└── requirements.txt
```

## 1. Requirements

```bash
pip install -r requirements.txt
```

## 2. TaasCrawler.py

[TAAS GIS 시스템](http://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN) 어린이사고 데이터 크롤러. 저장소 포크뜬 후 디렉토리에서 아래 명령어로 실행. `kids-accident-{condition}.json` 파일에 데이터 저장. 권한승인이 된 아이디로 실행해주세요. `condition=27`은 어린이 교통사고, `condtion=29`는 어린이보호구역 내 어린이교통사고입니다.

```bash
$ python TaasCrawler.py run --loginid=YOUR-ID --loginpwd=YOUR-PASSWORD --condition=27
```

## 3. TrafficApiClient.py

[사망교통사고 API](https://www.data.go.kr/data/15059126/openapi.do) 클라이언트. 키 받아서 txt 파일로 저장한 후 아래 명령어로 실행. `accident.json` 파일에 저장됨.

```bash
$ python TrafficApiClinet.py run --key_path=YOUR-KEY-PATH
```

## 4. Preprocess.py

`data_dir ` 인자에는 크롤링된 데이터가 저장된 디렉토리명을 넣어주면 됩니다. 전처리된 데이터는 해당 디렉토리에 `kids-accident.geojson` 파일로 저장됩니다.

```bash
$ python Preprocess.py run --data_dir=data
```