import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AffinityPropagation
from sklearn.metrics import silhouette_samples, silhouette_score
from mpl_toolkits.mplot3d import Axes3D
import warnings
import scipy.stats as stats
warnings.filterwarnings("ignore")

def run(data_folder, **kwargs):
    data = pd.read_csv("../input/german_credit_data.csv")
    data.drop(data.columns[0], inplace=True, axis=1)
    print("Database has {} obserwations (customers) and {} columns (attributes).".format(data.shape[0], data.shape[1]))
    print("Missing values in each column:\n{}".format(data.isnull().sum()))
    print("Columns data types:\n{}".format(data.dtypes))
    n_unique = data.nunique()
    print("Number of unique values:\n{}".format(n_unique))
    print("Unique values in each categorical column:")
    for col in data.select_dtypes(include=[object]):
        print(col, ":", data[col].unique())
    scatters(data, h="Sex")
    r1 = sns.jointplot(x="Credit amount", y="Duration", data=data, kind="reg", height=8)
    r1.annotate(stats.pearsonr)
    plt.show()
    sns.lmplot(x="Credit amount", y="Duration", hue="Sex", data=data, palette="Set1", aspect=2)
    plt.show()
    sns.lmplot(x="Credit amount", y="Duration", hue="Housing", data=data, palette="Set1", aspect=2)
    plt.show()
    sns.jointplot("Credit amount", "Duration", data=data, kind="kde", space=0, color="g", height=8)
    plt.show()
    n_credits = data.groupby("Purpose")["Age"].count().rename("Count").reset_index()
    n_credits.sort_values(by=["Count"], ascending=False, inplace=True)

    plt.figure(figsize=(10, 6))
    bar = sns.barplot(x="Purpose", y="Count", data=n_credits)
    bar.set_xticklabels(bar.get_xticklabels(), rotation=60)
    plt.ylabel("Number of granted credits")
    plt.tight_layout()
    boxes("Purpose", "Credit amount", "Sex")
    boxes("Purpose", "Duration", "Sex")
    boxes("Housing", "Credit amount", "Sex", r=0)
    boxes("Job", "Credit amount", "Sex", r=0)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data["Credit amount"], data["Duration"], data["Age"])
    ax.set_xlabel("Credit amount")
    ax.set_ylabel("Duration")
    ax.set_zlabel("Age")

    selected_cols = ["Age", "Credit amount", "Duration"]
    cluster_data = data.loc[:, selected_cols]
    distributions(cluster_data)
    cluster_log = np.log(cluster_data)
    distributions(cluster_log)
    scaler = StandardScaler()
    cluster_scaled = scaler.fit_transform(cluster_log)
    clusters_range = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    inertias = []

    for c in clusters_range:
        kmeans = KMeans(n_clusters=c, random_state=0).fit(cluster_scaled)
        inertias.append(kmeans.inertia_)

    plt.figure()
    plt.plot(clusters_range, inertias, marker='o')
    clusters_range = range(2, 15)
    random_range = range(0, 20)
    results = []
    for c in clusters_range:
        for r in random_range:
            clusterer = KMeans(n_clusters=c, random_state=r)
            cluster_labels = clusterer.fit_predict(cluster_scaled)
            silhouette_avg = silhouette_score(cluster_scaled, cluster_labels)
            # print("For n_clusters =", c," and seed =", r,  "\nThe average silhouette_score is :", silhouette_avg)
            results.append([c, r, silhouette_avg])

    result = pd.DataFrame(results, columns=["n_clusters", "seed", "silhouette_score"])
    pivot_km = pd.pivot_table(result, index="n_clusters", columns="seed", values="silhouette_score")

    plt.figure(figsize=(15, 6))
    sns.heatmap(pivot_km, annot=True, linewidths=.5, fmt='.3f', cmap=sns.cm.rocket_r)
    plt.tight_layout()

    kmeans_sel = KMeans(n_clusters=3, random_state=1).fit(cluster_scaled)
    labels = pd.DataFrame(kmeans_sel.labels_)
    clustered_data = cluster_data.assign(Cluster=labels)
    scatters(clustered_data, 'Cluster')
    grouped_km = clustered_data.groupby(['Cluster']).mean().round(1)
    grouped_km

    preferences = np.arange(-30, -190, -10)
    clusters = []

    for p in preferences:
        af = AffinityPropagation(preference=p, damping=0.6, max_iter=400, verbose=False).fit(cluster_scaled)
        labels_af = pd.DataFrame(af.labels_)
        clusters.append(len(af.cluster_centers_indices_))

    plt.figure(figsize=(10, 7))
    plt.xlabel("Preference")
    plt.ylabel("Number of clusters")
    plt.plot(preferences, clusters, marker='o')

    af = AffinityPropagation(preference=-140, damping=0.6, verbose=False).fit(cluster_scaled)
    labels_af = pd.DataFrame(af.labels_)
    n_clusters_ = len(af.cluster_centers_indices_)

    clustered_data_af = cluster_data.assign(Cluster=labels_af)
    scatters(clustered_data_af, 'Cluster')

    grouped_af = clustered_data_af.groupby(['Cluster']).mean().round(1)

    grouped_af = clustered_data_af.groupby(['Cluster']).mean().round(1)
    grouped_af



def scatters(data, h=None, pal=None):
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(8,8))
    sns.scatterplot(x="Credit amount",y="Duration", hue=h, palette=pal, data=data, ax=ax1)
    sns.scatterplot(x="Age",y="Credit amount", hue=h, palette=pal, data=data, ax=ax2)
    sns.scatterplot(x="Age",y="Duration", hue=h, palette=pal, data=data, ax=ax3)
    plt.tight_layout()

def boxes(x,y,h,r=45):
    fig, ax = plt.subplots(figsize=(10,6))
    box = sns.boxplot(x=x,y=y, hue=h, data=data)
    box.set_xticklabels(box.get_xticklabels(), rotation=r)
    fig.subplots_adjust(bottom=0.2)
    plt.tight_layout()

def distributions(df):
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(8,8))
    sns.distplot(df["Age"], ax=ax1)
    sns.distplot(df["Credit amount"], ax=ax2)
    sns.distplot(df["Duration"], ax=ax3)
    plt.tight_layout()
