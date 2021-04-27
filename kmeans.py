import logic
from sklearn.cluster import KMeans
import numpy as np


def KMeansClustering(clusterAmount,line_id,language):
    sents = logic.SQLQuery(f"select line_text from {language}_corpus where line_id in ({line_id});")
    vectors = logic.SQLQuery(f"select vector from {language}_corpus where line_id in ({line_id});")
    vectors = np.array(vectors).reshape(-1,1)
    vectordic = dict()
    kmeans = KMeans(n_clusters=clusterAmount).fit(vectors)
    clusters = kmeans.predict(vectors.reshape(-1,1))
    for x in range(len(clusters)):
        vectordic[sents[x]] = clusters[x]
    vectorvalue = set(vectordic.values())
    sentenceVectordic = {vec:[keys for keys in vectordic.keys() if vectordic[keys] == vec] for vec in set(vectordic.values())}
    MasterSentanceList = list()
    for x in range(clusterAmount):
        clusterlist = list(sentenceVectordic[x])
        MasterSentanceList.append(clusterlist)
    return MasterSentanceList