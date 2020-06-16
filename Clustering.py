import warnings
import fire
import pyproj
import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.cluster import DBSCAN
from functools import partial
from shapely.ops import transform
from shapely.geometry import Point

warnings.filterwarnings(action="ignore")

proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')


def geodesic_point_buffer(point, meter):
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=point.y, lon=point.x)),
        proj_wgs84
    )
    buf = Point(0, 0).buffer(meter)  # distance in metres
    return transform(project, buf)


def calc_meter_area(polygon):
    proj = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),
        pyproj.Proj(init='epsg:3857')
    )
    s_new = transform(proj, polygon)
    return s_new.area


class Clustering:
    @staticmethod
    def run():
        data = pd.read_json("data/kids-accident-pp.json")
        data = data.assign(
            sido=[x.split()[0] for x in data.legaldong_name],
            gugun=[x.split()[1] for x in data.legaldong_name],
            acdnt_dd_dc=pd.to_datetime(data.acdnt_dd_dc, format="%Y-%m-%d")
        )

        gdf = gpd.read_file("data/kids-accident-pp.geojson")
        gdf = gdf.assign(rad_X=np.radians(gdf.geometry.x), rad_Y=np.radians(gdf.geometry.y))

        # 2건 X 13년 = 26
        criterion = 26 / (300 * 300 * np.pi)

        seoul = data.query("sido=='서울특별시'").drop("sido", axis=1)

        earth_radius_km = 6371
        epsilon = 0.1 / earth_radius_km  # calculate 150 meter epsilon threshold
        min_samples = int(26 / 9)

        result = []
        for gu in seoul.gugun.unique():
            print(gu)
            # 클러스터 모델 적합
            df = seoul[seoul.gugun == gu]
            geo = gdf[gdf.acdnt_no.isin(df.acdnt_no)].drop("acdnt_no", axis=1)
            model = DBSCAN(
                eps=epsilon,
                min_samples=min_samples,
                n_jobs=6
            )
            model.fit(geo[["rad_X", "rad_Y"]])
            if model.labels_.max() == -1:
                print("-----------------------------------")
                print("클러스터 없음")
                print("-----------------------------------\n")
                continue
            before = pd.Series(model.labels_).value_counts().sort_index().reset_index().rename(
                columns={"index": "cluster", 0: "count"})

            # 밀도 계산
            geo = geo.assign(
                labels=model.labels_
            ).query("labels!=-1").assign(geometry=geo.geometry.apply(geodesic_point_buffer, meter=100))

            geo = pd.merge(
                geo.dissolve(by="labels").reset_index(),
                geo.labels.value_counts().reset_index().rename(columns={"labels": "cls_size", "index": "labels"})
            )
            geo = geo.assign(meter_area=geo.geometry.apply(calc_meter_area))
            geo = geo.assign(density=geo.cls_size / geo.meter_area)

            print("-----------------------------------")
            print(
                before.assign(
                    survived=before.cluster.isin(geo[geo.density > criterion].labels),
                    density=[0] + list(geo.sort_values("labels").density)
                )
            )
            print("-----------------------------------\n")
            result.append(geo.copy())

        cluster = pd.concat(result).query(f"density > {criterion}")
        acdnt_cls = gpd.sjoin(gdf[['geometry', 'acdnt_no']], cluster[['labels', 'geometry']], op="within")
        acdnt_cls = pd.merge(acdnt_cls, data)
        acdnt_cls = acdnt_cls.assign(acdnt_dd_dc=acdnt_cls.acdnt_dd_dc.astype(str))

        cluster.to_file("data/cluster.geojson", driver="GeoJSON")
        acdnt_cls.to_file("data/acdnt-cls.geojson", driver="GeoJSON")


if __name__ == "__main__":
    fire.Fire(Clustering)
