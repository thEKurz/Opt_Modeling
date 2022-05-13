from sklearn.cluster import AgglomerativeClustering
#These functions are no longer needed now that we the precomputed cluster class

def get_clusters(corr, cluster_number = 45, Thresh = None):
    if Thresh == None:
        cluster = AgglomerativeClustering(n_clusters=cluster_number, affinity='euclidean', linkage='ward')
    else:
        cluster = AgglomerativeClustering(n_clusters=None, affinity='euclidean', linkage='ward',distance_threshold=Thresh) 
    kclusters = cluster.fit_predict(corr)
    stock_clusters=pd.DataFrame(SP_Close.columns.values)
    stock_clusters=stock_clusters.set_index(0)
    stock_clusters['cluster']=kclusters
    return stock_clusters

def constrained_clusters(corr, corr_thresh = .7, stock_pct_thresh = .1,verbose=False, min_clusters = 10):
    ix = -1 #start at highest threshold and move backward
    threshes = np.exp(np.arange(0,5,.05))#need a better system for this to make it not dependant on number of assets, 

    for i in range(len(threshes)):
        thresh = threshes[ix]
        stock_clusters = get_clusters(corr, Thresh = thresh)
        cluster_number = stock_clusters['cluster'].max()+1

        internal_corr_average = np.zeros([cluster_number])
        for n in range(cluster_number):
            cluster_corr = corr.loc[stock_clusters.loc[stock_clusters['cluster']==n].index,stock_clusters.loc[stock_clusters['cluster']==n].index]
            internal_corr_average[n] = cluster_corr.mean().mean()

        clustersWInternalCorrLessThanThreshold = np.argwhere(internal_corr_average<corr_thresh).flatten()
        percent_stocks_in_bad_clusters = len(stock_clusters.loc[stock_clusters['cluster'].isin(clustersWInternalCorrLessThanThreshold)])/len(stock_clusters)
        if percent_stocks_in_bad_clusters > stock_pct_thresh:
            ix-=1
        else:
            break
    if verbose:
        print("# of clusters:", cluster_number)
        print("percent of stocks in clusters with internal corr of less than corr_thresh:", percent_stocks_in_bad_clusters)

    #run clustering with chosen optimal method
    return get_clusters(corr, cluster_number = cluster_number), cluster_number


#test cluster corr

#temp = plt.hist(internal_corr_average,bins=15)
#plt.title("hist of ave of internal correlation matrices")
#plt.show()