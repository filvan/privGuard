import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

def run(data_folder, **kwargs):
    df = pd.read_csv('/kaggle/input/german-credit/german_credit_data.csv')
    df.shape
    df.head()
    df.info()
    df.describe()
    df.isnull().sum()
    numerical = ['Credit amount', 'Age', 'Duration']
    categorical = ['Sex', 'Job', 'Housing', 'Saving accounts', 'Checking account', 'Purpose']
    unused = ['Unnamed: 0']
    df = df.drop(columns=unused)
    df.shape
    for cat in categorical:
        df[cat] = df[cat].fillna(df[cat].mode().values[0])

    df.isnull().sum()

    #visualize
    sns.pairplot(df)
    fig = plt.figure(figsize=(20, 15))
    axes = 320
    for cat in categorical:
        axes += 1
        fig.add_subplot(axes)
        sns.countplot(data=df, x=cat)
        plt.xticks(rotation=30)
    plt.show()

    # create correlation
    corr = df.corr(method='pearson')

    # convert correlation to numpy array
    mask = np.array(corr)

    # to mask the repetitive value for each pair
    mask[np.tril_indices_from(mask)] = False
    fig, ax = plt.subplots(figsize=(15, 12))
    fig.set_size_inches(15, 15)
    sns.heatmap(corr, mask=mask, vmax=0.9, square=True, annot=True)

    df_cluster = pd.DataFrame()
    df_cluster['Credit amount'] = df['Credit amount']
    df_cluster['Age'] = df['Age']
    df_cluster['Duration'] = df['Duration']
    df_cluster['Job'] = df['Job']
    df_cluster.head()

    fig = plt.figure(figsize=(15, 10))
    axes = 220
    for num in numerical:
        axes += 1
        fig.add_subplot(axes)
        sns.boxplot(data=df, x=num)
    plt.show()
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1, figsize=(8,8))
    sns.distplot(df["Age"], ax=ax1)
    sns.distplot(df["Credit amount"], ax=ax2)
    sns.distplot(df["Duration"], ax=ax3)
    sns.distplot(df["Job"], ax=ax4)
    plt.tight_layout()
    plt.legend()

    #Feature Engineering

    df_cluster_log = np.log(df_cluster[['Age', 'Credit amount', 'Duration']])

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8))
    sns.distplot(df_cluster_log["Age"], ax=ax1)
    sns.distplot(df_cluster_log["Credit amount"], ax=ax2)
    sns.distplot(df_cluster_log["Duration"], ax=ax3)
    plt.tight_layout()

    df_cluster_log.head()
    scaler = StandardScaler()
    cluster_scaled = scaler.fit_transform(df_cluster_log)

    #models
    Sum_of_squared_distances = []
    K = range(1, 15)
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(cluster_scaled)
        Sum_of_squared_distances.append(km.inertia_)
    plt.figure(figsize=(20, 5))
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()

    model = KMeans(n_clusters=3)
    model.fit(cluster_scaled)
    kmeans_labels = model.labels_

    fig = plt.figure(num=None, figsize=(15, 10), dpi=80, facecolor='w', edgecolor='k')
    ax = plt.axes(projection="3d")

    ax.scatter3D(df_cluster['Age'], df_cluster['Credit amount'], df_cluster['Duration'], c=kmeans_labels,
                 cmap='rainbow')

    xLabel = ax.set_xlabel('Age', linespacing=3.2)
    yLabel = ax.set_ylabel('Credit Amount', linespacing=3.1)
    zLabel = ax.set_zlabel('Duration', linespacing=3.4)
    print("K-Means")

    df_clustered_kmeans = df_cluster.assign(Cluster=kmeans_labels)
    grouped_kmeans = df_clustered_kmeans.groupby(['Cluster']).mean().round(1)
    grouped_kmeans

    plt.figure(figsize=(20, 10))
    dendrogram = sch.dendrogram(sch.linkage(cluster_scaled, method='ward'))
    model = AgglomerativeClustering(n_clusters=4)
    model.fit(cluster_scaled)
    hac_labels = model.labels_

    fig = plt.figure(num=None, figsize=(15, 10), dpi=80, facecolor='w', edgecolor='k')
    ax = plt.axes(projection="3d")

    ax.scatter3D(df_cluster['Age'], df_cluster['Credit amount'], df_cluster['Duration'], c=hac_labels, cmap='rainbow')

    xLabel = ax.set_xlabel('Age', linespacing=3.2)
    yLabel = ax.set_ylabel('Credit Amount', linespacing=3.1)
    zLabel = ax.set_zlabel('Duration', linespacing=3.4)
    print("Hierarchical Agglomerative Clustering")

    df_clustered_hac = df_cluster.assign(Cluster=hac_labels)
    grouped_hac = df_clustered_hac.groupby(['Cluster']).mean().round(1)
    grouped_hac

    model = DBSCAN()
    model.fit(cluster_scaled)
    dbs_labels = model.labels_

    fig = plt.figure(num=None, figsize=(15, 10), dpi=80, facecolor='w', edgecolor='k')
    ax = plt.axes(projection="3d")

    ax.scatter3D(df_cluster['Age'], df_cluster['Credit amount'], df_cluster['Duration'], c=dbs_labels, cmap='rainbow')

    xLabel = ax.set_xlabel('Age', linespacing=3.2)
    yLabel = ax.set_ylabel('Credit Amount', linespacing=3.1)
    zLabel = ax.set_zlabel('Duration', linespacing=3.4)
    print("DBSCAN")

    #result analysis
    grouped_kmeans
    df_clustered = df.assign(Cluster=kmeans_labels)
    df_clustered.head()
    fig = plt.figure(figsize=(20, 15))
    axes = 320
    for cat in categorical:
        axes += 1
        fig.add_subplot(axes)
        sns.countplot(data=df_clustered, hue=df_clustered['Cluster'], x=cat)
        plt.xticks(rotation=30)
    plt.show()