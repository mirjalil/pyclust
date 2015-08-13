import scipy, scipy.spatial
import numpy as np

def _cal_silhouette_score(X, y, sample_size, metric):
    """
    """
    n_samples = X.shape[0]
    if sample_size is not None:
       assert(1 < sample_size < n_samples)
       rand_inx = np.random.choice(X.shape[0], size=sample_size)
       X_samp, y_samp = X[rand_inx], y[rand_inx]

    else:
       X_samp, y_samp = X, y

    n_clust_samp = len(np.unique(y_samp))
    pair_dist = scipy.spatial.distance.pdist(X_samp, metric=metric)

    pair_dist_matrix = scipy.spatial.distance.squareform(pair_dist)

    ## Compute average intra-cluster distances 
    ## for each of the selected samples
    a_arr = _intra_cluster_distances(pair_dist_matrix, y_samp, np.arange(y_samp.shape[0]))


    return(a_arr)


def _intra_cluster_distances(dist_matrix, y, ilist):
    """
    """
    n_samples = y.shape[0]
    if type(ilist) == type(list()):
        n_inx = len(ilist)
    elif type(ilist) == type(np.array([])):
        n_inx = ilist.shape[0]
    else:
        raise Exception("ilist must be iterable!")


    mean_intra_distances = np.empty(shape=n_inx, dtype=float)

    for i,inx in enumerate(ilist):
        mask = y == y[inx]
        if np.sum(mask)>0:
            mean_intra_distances[i] = np.mean(dist_matrix[mask].T[inx])
        else:
            mean_intra_distances[i] = 0.0

    return(mean_intra_distances) 

class Silhouette(object):
    """
    """
    def __init__(self):
        self.n_labels_ = None

    def score(self, X, labels, sample_size=None, metric='euclidean'):
        self.score = _cal_silhouette_score(X, labels, sample_size, metric)

        return(self.score)