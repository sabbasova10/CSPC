from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
import pandas as pd
import os

import numpy as np

from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

os.makedirs("results", exist_ok=True)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

wine = load_wine(as_frame=True)
X = wine.data # DataFrame, 178 rows x 13 measurements
cultivar = wine.target # Series of 0/1/2 -- set aside until B6

# B1
print(wine.DESCR)
stats = X.describe().T[["min", "max", "mean", "std"]]
stats["range"] = stats["max"] - stats["min"]
print(stats.sort_values("std", ascending=False))
# largest: propoline, magnesium
# smallest:  Nonflavanoid Phenols, Hue

