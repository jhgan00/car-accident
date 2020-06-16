# 어린이 교통사고 분석

- [01. 어린이 교통사고 현황](https://https://jhgan00.github.io/car-accident/kids-accident.html)
- [02. 탐색적 데이터 분석](https://jhgan00.github.io/car-accident/EDA.html)
- [03. 클러스터링 결과](https://jhgan00.github.io/car-accident/cluster.html)

```bash
├── ClusterVisualization.py
├── Clustering.py
├── Preprocess.py
├── README.md
├── Schoolzone.py
├── TaasCrawler.py
├── data
│   ├── maps
│   │   ├── CTPRVN.dbf
│   │   ├── CTPRVN.prj
│   │   ├── CTPRVN.shp
│   │   ├── CTPRVN.shx
│   │   ├── N3A_A0053326.dbf
│   │   ├── N3A_A0053326.shp
│   │   ├── N3A_A0053326.shx
│   │   └── schoolzone-seoul.geojson
│   └── 전국어린이보호구역표준데이터.csv
└── requirements.txt

```

## 1. Requirements

- Ubuntu 20.04 LTS
- 16GB RAM

```bash
pip install -r requirements.txt
```

## 2. TaasCrawler.py

[TAAS GIS 시스템](http://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN) 교통사고 데이터 크롤러입니다.
 권한승인이 된 아이디를 준비해서 아래 커맨드로 실행해주시면 됩니다. `data/kids-accident-27.json`은 어린이 교통사고,
 `data/kids-accident-29.json`는 어린이보호구역 내 어린이교통사고입니다. 어린이 교통사고가 아닌 전체 교통사고 데이터를 수집하려면
 `--kids=0` 으로 설정해주세요.

```bash
$ python TaasCrawler.py run # 어린이 교통사고 데이터 수집
$ python TaasCrawler.py run --kids=0 # 전체 교통사고 데이터 수집
```

## 3. Preprocess.py

크롤링된 데이터를 전처리합니다. 전처리된 데이터는 해당 디렉토리에 `kids-accident-pp.json`, `kids-accident-pp.geojson` 파일로 저장됩
니다. 어린이 데이터가 아닌 전체 교통사고 데이터를 전처리하는 경우에는 `--kids=0` 으로 설정해주세요.

```bash
$ python Preprocess.py run # 어린이 교통사고 데이터 전처리
$ python Preprocess.py run --kids=0 # 전체 교통사고 데이터 전처리
```

## 4. Clustering.py

전처리된 데이터를 클러스터링합니다. 클러스터는 `data/cluster.geojson`, 클러스터 지역에 속하는 사고들은 `acdnt-cls.geojson`에 저장
됩니다. 

```bash
$ python Clustering.py run
```

## 5. Schoolzone.py

- [국토정보지리원 연속수치지형도 안전지대 데이터](http://data.nsdi.go.kr/dataset/20180927ds0002/resource/f791be59-3153-491d-8952-8e015d0ef6bf?inner_span=True)
- [대한민국 행정구역 경계 데이터](http://www.gisdeveloper.co.kr/?p=2332)

어린이 보호구역 데이터와 서울시 경계 파일을 통해 서울시 내 어린이 보호구역 데이터를 WGS84(EPSG 4326) 좌표계로 추출합니다. 결과는 
`data/maps/schoolzone-seoul.geojson`으로 저장됩니다.

```bash
$ python Schoolzone.py
```

## 6. ClusterVisualization.py

클러스터와 어린이 보호구역의 경계를 지도 시각화하여 `docs/cluster.html`로 저장합니다.

```bash
$ python ClusterVisualization.py
```