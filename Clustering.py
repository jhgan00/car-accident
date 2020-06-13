import logging
import os
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from itertools import product
from tqdm import tqdm

gdf = gpd.read_file("data/geometry.geojson")
df = pd.read_json("data/kids-accident-pp.json")
df = df.assign(
    sido=[x.split(" ")[0] for x in df.legaldong_name]
)[['acdnt_no', 'sido']]

data = pd.merge(
    pd.DataFrame({"acdnt_no":gdf.acdnt_no.values, "X":gdf.geometry.x, "Y":gdf.geometry.y}),
    df
)
del(df)
if not os.path.exists("figs"):
    os.mkdir("figs")
if not os.path.exists("logs"):
    os.mkdir("logs")

for (sido, df) in data.groupby("sido"):
    print(f"{sido} 지역 클러스터링")
    tmp = gdf[gdf.acdnt_no.isin(df.acdnt_no)]
    std_coords = StandardScaler().fit_transform(df[["X", "Y"]])

    if not os.path.exists(f"figs/{sido}"):
        os.mkdir(f"figs/{sido}")
        print(f"mkdir: figs/{sido}")
    logfile = open(f"logs/{sido}.csv", "a")
    logfile.write("eps,min_samples,ncluster,mean_cluster_size,outliers\n")
    prod = product(np.arange(0.002, 0.2, 0.002), np.arange(2,10))
    with tqdm(total=sum([1 for x in prod])) as progress_bar:
        for (eps, min_samples) in product(np.arange(0.002, 0.2, 0.002), np.arange(2,10)):
            eps = round(eps, 4)
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            dbscan.fit(std_coords)
            labels = dbscan.labels_
            ncluster = np.unique(labels).size
            outliers = round(((dbscan.labels_ == -1).sum() / df.shape[0])*100, 2)
            geo = tmp.copy()
            geo = geo.assign(labels = labels)[labels!=-1]
            if geo.shape[0] == 0:
                continue
            geo.plot(column="labels", markersize=1.5)
            mean_cluster_size = int(pd.Series(labels).value_counts().mean())

            record = f"{eps},{min_samples},{ncluster},{mean_cluster_size},{outliers}"
            logfile.write(
                f"{record}\n"
            )
            plt.title(f"eps:{eps}, ms:{min_samples},\nncluster:{ncluster}, mean_cluster_size:{mean_cluster_size}, outliers:{outliers}%", fontdict={"fontsize":13})
            plt.savefig(f"figs/{sido}/eps:{eps}_ms:{min_samples}.png")
            plt.close()
            progress_bar.update(1)
        logfile.close()