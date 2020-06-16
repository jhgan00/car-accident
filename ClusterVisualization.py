import folium
import geopandas as gpd
from folium import plugins
from folium.map import FeatureGroup, LayerControl

schoolzone = gpd.read_file("data/maps/schoolzone-seoul.geojson")
cluster = gpd.read_file("data/cluster.geojson")
acdnt_cls = gpd.read_file("data/acdnt-cls.geojson")

featuregroup1 = FeatureGroup(name="사고발생좌표")
featuregroup2 = FeatureGroup(name="어린이보호구역추천")
featuregroup3 = FeatureGroup(name="스쿨존")


def cluster_style(feature):
    style = {
        "color": "red",
        "fillcolor": "red",
        "opacity": 0.9
    }
    return style


def schoolzone_style(feature):
    style = {
        "color": "green",
        "fillcolor": "green",
        "opacity": 0.6
    }
    return style


m = folium.Map(location=[37.53, 126.97], zoom_start=12)

folium.features.GeoJson(acdnt_cls).add_to(featuregroup1)
folium.features.GeoJson(cluster, cluster_style).add_to(featuregroup2)
folium.features.GeoJson(schoolzone, schoolzone_style).add_to(featuregroup3)

featuregroup1.add_to(m)
featuregroup2.add_to(m)
featuregroup3.add_to(m)

LayerControl().add_to(m)
plugins.ScrollZoomToggler().add_to(m)

m.save("docs/cluster.html")
