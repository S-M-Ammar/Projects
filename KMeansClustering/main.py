import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

df = pd.read_csv('file.csv')
print(df.head(10))


kmeans = KMeans(n_clusters=2)
y_predicted = kmeans.fit_predict(df[['distance','group_size','expenditure','nights']])

cluster_Number_k_2 = y_predicted
df['cluster_Number_k_2'] = cluster_Number_k_2
centroids_k_2 = kmeans.cluster_centers_
print(kmeans.labels_)
print("\n\n\n")
print(df.head(20))

kmeans = KMeans(n_clusters=3)
y_predicted = kmeans.fit_predict(df[['distance','group_size','expenditure','nights']])
cluster_Number_k_3 = y_predicted
centroids_k_3 = kmeans.cluster_centers_
df['cluster_Number_k_3'] = cluster_Number_k_3
print(kmeans.labels_)
print("\n\n\n")
print(df.head(20))

kmeans = KMeans(n_clusters=4)
y_predicted = kmeans.fit_predict(df[['distance','group_size','expenditure','nights']])
cluster_Number_k_4 = y_predicted
centroids_k_4 = kmeans.cluster_centers_
df['cluster_Number_k_4'] = cluster_Number_k_4
print(kmeans.labels_)
print("\n\n\n")
print(df.head(20))

df['-----Space----'] = ""
print(df.head(20))

centroids_k_2_list = []
centroids_k_3_list = []
centroids_k_4_list = []

for x in list(centroids_k_2):
    for y in x:
        centroids_k_2_list.append(y)



for x in list(centroids_k_3):
    for y in x:
        centroids_k_3_list.append(y)

for x in list(centroids_k_4):
    for y in x:
        centroids_k_4_list.append(y)


df['centroid_Number_k_2'] = pd.Series(centroids_k_2_list)
df['centroid_Number_k_3'] = pd.Series(centroids_k_3_list)
df['centroid_Number_k_4'] = pd.Series(centroids_k_4_list)

print(df.head(20))

df.to_csv('output.csv')