""" En este módulo se crean los modelos de clustering para los datos
recolectados y se comparan.
"""

import sys
from dataframe import PARTIDOS
from pickle import load
import numpy as np
from scipy.spatial import distance
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.cluster import (KMeans, SpectralClustering,
                             AgglomerativeClustering, OPTICS)


def get_closest_centroid(obs, centroids):
    """ gets the centroid that's closest to the given datum,
    using euclidean distance."""
    min_distance = sys.float_info.max
    min_centroid = 0

    print(obs)
    print(centroids)

    for c in centroids:
        dist = distance.euclidean(obs, c)
        if dist < min_distance:
            min_distance = dist
            min_centroid = c
    return min_centroid


def get_prediction_strength(k, train_centroids, x_test, test_labels):
    """ calcula la 'fuerza de predicción' de un coeficiente dado para
    un dataset."""
    n_test = len(x_test)

    # llena la matriz de comparación
    D = np.zeros(shape=(n_test, n_test))
    for x1, l1, c1 in zip(x_test.values, test_labels, list(range(n_test))):
        for x2, l2, c2 in zip(x_test.values, test_labels, list(range(n_test))):
            if tuple(x1) != tuple(x2):
                if tuple(get_closest_centroid(
                        x1, train_centroids
                )) == tuple(
                    get_closest_centroid(
                        x2, train_centroids)):
                    D[c1, c2] = 1.0

    # calcula la fuerza de predicción de cada cluster
    ss = []
    for j in range(k):
        s = 0
        examples_j = x_test[test_labels == j, :].tolist()
        n_examples_j = len(examples_j)
        for x1, l1, c1 in zip(x_test, test_labels, list(range(n_test))):
            for x2, l2, c2 in zip(x_test, test_labels, list(range(n_test))):
                if tuple(x1) != tuple(x2) and l1 == l2 and l1 == j:
                    s += D[c1, c2]
        ss.append(s / (n_examples_j * (n_examples_j - 1)))

    prediction_strength = min(ss)
    return prediction_strength


def one_party_clusters(party: str):
    """ generate clusters based on the sentimental data from a single party's
    followers."""
    with open('dataframes/' + party + '.pkl', 'rb') as archivo:
        frame = load(archivo)
    kmeans = KMeans(n_clusters=10, random_state=0)
    clusters = kmeans.fit_predict(frame)


def elbow_kmeans(frame):
    """ genera los resultados de 10 clusters para verificación manual."""
    lista = []
    for k in range(1, 11):
        model = KMeans(n_clusters=k)
        model.fit(frame)
        lista.append(model.inertia_)
    return lista


def frame(party: str):
    """ retorna el dataframe con los datos de un solo partido."""
    with open('dataframes/' + party + '.pkl', 'rb') as arch:
        frame = load(arch)
    return frame


def all_party_frames():
    """ Retorna todos los tweets en un solo dataframe."""
    allframes = pd.DataFrame({"author": [], "rts": [], "links": [],
                              "punctuation": [], "hashtags": [], "tags": [],
                              "positive": [], "neutral": [],
                              "negative": [], "compound": []})
    for p, c, s in PARTIDOS:
        with open('dataframes/' + p + '.pkl', 'rb') as archivo:
            frame = load(archivo)
        frame["partido"] = [p for _ in range(0, len(frame))]
        allframes = allframes.merge(frame, how="outer")
    return allframes


def prediction_strength(frame):
    strengths = []
    # separando en train y test
    X_train, X_test = train_test_split(frame, test_size=0.2)
    for k in range(1, 11):
        modelX = KMeans(n_clusters=k)
        modelY = KMeans(n_clusters=k)
        modelX.fit(X_train)
        modelY.fit(X_test)
        strengths.append(
            get_prediction_strength(
                k, modelX.cluster_centers_,
                X_test, modelY.labels_))
    return strengths
