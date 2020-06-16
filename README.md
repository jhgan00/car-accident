# 어린이 교통사고 분석

```bash
├── Clustering.py
├── EDA&시각화
│   └── 어린이_교통사고_현황_서울.html
├── EDA.ipynb
├── Preprocess.py
├── README.md
├── TaasCrawler.py
├── data
│   ├── accident-total-pp.geojson
│   ├── accident-total-pp.json
│   ├── accident-total.json
│   ├── codes
│   │   ├── 구군코드.csv
│   │   ├── 시도코드.csv
│   │   └── 지역코드.csv
│   ├── kids-accident-27.json
│   ├── kids-accident-29.json
│   ├── kids-accident-pp.geojson
│   └── kids-accident-pp.json
├── requirements.txt
└── 클러스터링_실험.ipynb
```

## 1. Requirements

- Ubuntu 20.04 LTS
- 16GB RAM

```bash
pip install -r requirements.txt
```

## 2. TaasCrawler.py

[TAAS GIS 시스템](http://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN) 어린이사고 데이터 크롤러입니다.
 권한승인이 된 아이디를 준비해서 아래 커맨드로 실행해주시면 됩니. `data/kids-accident-27.json`은 어린이 교통사고,
 `data/kids-accident-29.json`는 어린이보호구역 내 어린이교통사고입니다.

```bash
$ python TaasCrawler.py run
```

## 3. Preprocess.py

크롤링된 데이터를 전처리합니다. 전처리된 데이터는 해당 디렉토리에 `kids-accident.geojson` 파일로 저장됩니다.

```bash
$ python Preprocess.py run
```

## 4. Clustering.py