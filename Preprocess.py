import pandas as pd
import geopandas as gpd
import json
import fire


class Preprocess:
    @staticmethod
    def run(kids=True):
        def drop(row):
            for colname in dropcols:
                row.pop(colname)

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

        dropcols = ["acdnt_year", "otn_acdnt_no", "acdnt_frm_lv1", "acdnt_frm_lv2", "acdnt_frm_lv3",
                    "acdnt_sta_lv1",
                    "acdnt_sta_lv2", "city_idt_code", "city_idt_dc", "engn_code", "pageIndex",
                    "pageUnit", "recordCountPerPage", "rn", "searchCondition", "searchConditionText",
                    "searchKeyword", "spt_otlnmap_at", "xCrdnt", "yCrdnt", "zoneYn"]
        print("Reading raw data ...")
        if kids:
            df = pd.read_json("data/kids-accident-27.json")
            df = df.drop(dropcols, axis=1)
        else:
            with open("data/accident-total.json", "r") as jsonfile:
                df = json.load(jsonfile)
            _ = list(map(drop, df))
            df = pd.DataFrame(df)
        kidszone_acdnt = pd.read_json("data/kids-accident-29.json").acdnt_no.astype(int).values
        df = df.assign(
            kidszone=df.acdnt_no.astype(int).isin(kidszone_acdnt).astype(int)
        )
        del kidszone_acdnt

        print("Done")
        print("Processing ...")
        df["acdnt_dc"] = df.acdnt_dc.apply(rp)
        df["acdnt_mdc"] = df.acdnt_mdc.apply(rp)
        df["lrg_violt_1_dc"] = df.lrg_violt_1_dc.apply(rp)
        df["road_stle_dc"] = df.road_stle_dc.apply(rp)

        dc_list = []
        code_list = []
        for columns in df.columns:
            if "dc" in columns:
                dc_list.append(columns)
            elif "code" in columns:
                code_list.append(columns)

        dc_list.remove('acdnt_dd_dc')
        dc_list.insert(15, "legaldong_name")
        df['dfk_dc'] = df.dfk_code.astype(int).map(dict(zip(range(1, 8), ["월", "화", "수", "목", "금", "토", "일"])))

        sido = pd.Series([
            '강원도', '경기도', '경상남도', '경상북도', '광주광역시', '대구광역시', '대전광역시', '부산광역시',
            '서울특별시', '세종특별자치시', '울산광역시', '인천광역시', '전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도'
        ])
        sido_dict = dict(zip(sido.str.slice(start=1), sido))
        sido = pd.Series([x[0] for x in df.legaldong_name.str.split(" ")]).replace(sido_dict)
        df = df.assign(legaldong_name=sido + " " + df.legaldong_name.str.split(" ").apply(lambda x: " ".join(x[1:])))
        del sido
        del sido_dict

        tmp_dict = {"포장 - 젖음/습기": "포장 - 습기", '포장 - 서리/결빙': "포장 - 결빙", "비포장 - 젖음/습기": "비포장 - 습기"}

        df["rdse_sttus_dc"] = df.rdse_sttus_dc.replace(tmp_dict)

        df['acdnt_age_1_dc'] = df.acdnt_age_1_dc.replace({
            "미분류": "0세",
            "기타불명": "0세",
            None: "0세"
        }).str.replace("\D", "").astype(int)
        df['acdnt_age_2_dc'] = df.acdnt_age_2_dc.replace({
            "미분류": "0세",
            "기타불명": "0세",
            None: "0세"
        }).str.replace("\D", "").astype(int)
        df = df.assign(kids_acdnt=((df.acdnt_age_2_dc < 14) & (df.acdnt_age_2_dc > 0)).astype(int))

        gdf = gpd.GeoDataFrame(
            df[['acdnt_no']],
            geometry=gpd.points_from_xy(df.x_crdnt, df.y_crdnt),
        )
        gdf.crs = {"init": "EPSG:5179"}
        gdf = gdf.to_crs({"init": "epsg:4326"})

        df = df.drop(code_list + [
            "acdnt_hdc",
            "acdnt_dc",  # acdnt_hdc + acdnt_mdc
            "wrngdo_vhcle_asort_hdc",
            "dmge_vhcle_asort_hdc",  # "dmge_vhcle_asort_code" 와 사실상 중복
            "injury_dgree_1_hdc",
            "injury_dgree_2_hdc",
            "x_crdnt",
            "y_crdnt"
        ], axis=1).assign(
            acdnt_dd_dc=pd.to_datetime(df.acdnt_dd_dc, format="%Y년 %m월 %d일").astype(str),
            occrrnc_time_dc=df.occrrnc_time_dc.str.slice(0, -1).astype(int),
            road_div=df.road_div.fillna(0).astype(int)
        )

        if kids:
            df_output_path = "data/kids-accident-pp.json"
            gdf_output_path = "data/kids-accident-pp.geojson"
        else:
            df_output_path = "data/accident-total-pp.json"
            gdf_output_path = "data/accident-total-pp.geojson"
        print(f"Saving data...")
        df.to_json(df_output_path)
        gdf.to_file(gdf_output_path, driver="GeoJSON")
        print("Saved data")


if __name__ == "__main__":
    fire.Fire(Preprocess)
