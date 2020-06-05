import pandas as pd
import geopandas as gpd
import json
import re
import fire

class Preprocess:

	def run(self, data_dir):
		print("Reading raw data ...")
		df = pd.read_json(data_dir + "/kids-accident-27.json")
		merge_df = pd.read_json(data_dir + "/kids-accident-29.json")

		print("Processing ...")
		df = df.assign(
			kidszone = df.acdnt_no.isin(merge_df.acdnt_no).astype(int) 
			)
		del(merge_df)

		df=df.drop(["acdnt_year","acdnt_no","otn_acdnt_no","acdnt_frm_lv1", "acdnt_frm_lv2", "acdnt_frm_lv3", "acdnt_sta_lv1",
		        "acdnt_sta_lv2", "city_idt_code", "city_idt_dc", "engn_code", "pageIndex",
		        "pageUnit", "recordCountPerPage", "rn", "searchCondition", "searchConditionText",
		        "searchKeyword", "spt_otlnmap_at", "xCrdnt", "yCrdnt", "zoneYn"], axis=1)
		def rp(x):
		    if (x == '대사람 - 기타') or (x == '대사람 - 보도통행중') or (x == '대사람 - 횡단중') or (x == '도통행중'):
		        return "차" + x
		    elif (x == "행자보호의무위반") or (x == '도통행중'):
		        return "보" + x
		    elif (x == "일로 - 횡단보도상") or (x == "일로 - 기타"):
		        return "단" + x
		    elif (x == '차로 - 교차로부근') or (x == '차로 - 교차로안'):
		        return "교" + x
		    else:
		        return x

		df["acdnt_dc"]=df.acdnt_dc.apply(rp)
		df["acdnt_mdc"]=df.acdnt_mdc.apply(rp)
		df["lrg_violt_1_dc"]=df.lrg_violt_1_dc.apply(rp)
		df["road_stle_dc"]=df.road_stle_dc.apply(rp)

		dc_list = []
		code_list = []
		for columns in df.columns:
		    if "dc" in columns:
		        dc_list.append(columns)
		    elif "code" in columns:
		        code_list.append(columns)

		dc_list.remove('acdnt_dd_dc')
		dc_list.insert(15, "legaldong_name")

		df['dfk_dc'] = df.dfk_code.map(dict(zip(range(1,8), ["월","화","수","목","금","토","일"])))

		df["시도"]=df.legaldong_name.apply(lambda x : str(re.match("\w+\s",x)).split(",")[-1][8:-3])

		a=list(df[df.시도 == "상남도"].legaldong_name)
		b=list(df[df.시도 == "상남도"].legaldong_name.apply(lambda x : "경"+x))
		c=dict(zip(a,b))
		df["legaldong_name"]=df.legaldong_name.replace(c)
		tmp_dict = {"포장 - 젖음/습기": "포장 - 습기", '포장 - 서리/결빙':"포장 - 결빙", "비포장 - 젖음/습기":"비포장 - 습기"}

		df["rdse_sttus_dc"] = df.rdse_sttus_dc.replace(tmp_dict)

		df['acdnt_age_1_dc'] = df.acdnt_age_1_dc.replace({
		    "미분류":"0세",
		    "기타불명":"0세"
		}).str.replace("\D","").astype(int)

		df['acdnt_age_2_dc'] = df.acdnt_age_2_dc.replace({
		    "미분류":"0세",
		    "기타불명":"0세"
		}).str.replace("\D","").astype(int)

		df = df[df.acdnt_age_2_dc < 14]

		df = df.drop(code_list+[
		    "acdnt_hdc",
		    "acdnt_dc", # acdnt_hdc + acdnt_mdc
		    "dmge_vhcle_asort_hdc", # "dmge_vhcle_asort_code" 와 사실상 중복
		    "시도"
		    ], axis=1)

		df = df.assign(
		    acdnt_dd_dc = pd.to_datetime(df.acdnt_dd_dc, format="%Y년 %m월 %d일").astype(str),
		    occrrnc_time_dc = df.occrrnc_time_dc.str.slice(0,-1).astype(int)
		)

		gdf = gpd.GeoDataFrame(
		    df,
		    geometry=gpd.points_from_xy(df.x_crdnt, df.y_crdnt),
		)

		gdf.crs = {"init":"EPSG:5179"}
		gdf = gdf.to_crs({"init":"epsg:4326"})

		for column in gdf.columns:
		    uniques = gdf[column].unique()
		    print(
		        f"""
		        ===========================
		        Column: {column}
		        Unique: {uniques[:5]}
		        N-unique: {uniques.size}
		        ===========================
		        """
		    )	

		output_path = data_dir+"/kids-accident.geojson"
		print(f"Saving data: {output_path}...")
		gdf.to_file(output_path, driver="GeoJSON")
		print("Saved data")

if __name__ =="__main__":
	fire.Fire(Preprocess)