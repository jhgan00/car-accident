import geopandas as gpd

# 국토지리정보원 연속수치지형도 안전지대 데이터: http://data.nsdi.go.kr/dataset/20180927ds0002/resource/f791be59-3153-491d-8952-8e015d0ef6bf?inner_span=True
schoolzone = gpd.read_file("data/maps/N3A_A0053326.shp", encoding="euckr").query("STRU=='SZS003'")
schoolzone.crs = "EPSG:5179"
schoolzone = schoolzone.to_crs("EPSG:4326")

# 대한민국 행정구역 경계파일: http://www.gisdeveloper.co.kr/?p=2332
sido = gpd.read_file("data/maps/CTPRVN.shp", encoding="euckr")
seoul = sido.query("CTP_KOR_NM=='서울특별시'").to_crs("EPSG:4326")

schoolzone_seoul = gpd.sjoin(schoolzone, seoul)
schoolzone_seoul.to_file("data/maps/schoolzone-seoul.geojson", driver="GeoJSON")
