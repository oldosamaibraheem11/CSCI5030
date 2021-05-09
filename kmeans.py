import logic
from sklearn.cluster import KMeans
import numpy as np


def KMeansClustering(clusterAmount,line_id,language):
    sents = logic.SQLQuery(f"select line_text from {language}_corpus where line_id in ({line_id}) AND vector IS NOT NULL;")
    vectors = logic.SQLQuery(f"select vector from {language}_corpus where line_id in ({line_id}) AND vector IS NOT NULL;")
    vectors = np.array(vectors).reshape(-1,1)
    vectordic = dict()
    try:
        kmeans = KMeans(n_clusters=clusterAmount).fit(vectors)
    except:
        return f"Not enough sentences for {clusterAmount} clusters there are only {len(sents)} senetences"
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