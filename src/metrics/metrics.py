############################################################################################
#                                                                                          #
#  FileName    [metrics.py]                                                                #
#                                                                                          #
#  PackageName [metrics]                                                                   #
#                                                                                          #
#  Synopsis    [This file contains the class for the application of the selected metrics   #
#              and returns the top k nodes, with k chosen, of the rank obtained            #
#              from the metrics.]                                                          #
#                                                                                          #
#  Author      [Leonardo Picchiami]                                                        #
#                                                                                          #
############################################################################################


import networkx as nx



class Metrics(object):
    '''
    Class for the application of the metrics of the graph of the ds-1 dataset of a specific year, 
    the creation of the rank and the selection of the top k nodes.
    

    Attributes
    ----------
    year_graph : YearGraph or networkx.Graph
        - YearGraph object to get the graph of the ds-1 dataset on which to apply the metrics. 
        - Graph object of the networkx library representing the graph of the ds1 dataset for a specific year.

    top_k_nodes : list
        First k nodes retrivied by a metric whose rank was obtained by ordering the scores in descending order.
         
    '''


    def __init__(self, year_graph):
        '''
        Parameters
        ----------
        year_graph : YearGraph
            YearGraph object to get the graph of the ds-1 dataset on which to apply the metrics. 
        '''

        self.__year_graph = year_graph
        self.__top_k_nodes = None

        
        
    def metrics_preprocessing(self):
        '''
        Metric preprocessing method. 
        The networkx object relating to the graph of a given year of the ds-1 dataset is saved in the year_graph attribute.
        '''
        
        self.__year_graph = self.__year_graph.get_ds1_graph()



    def get_top_k_nodes(self):
        '''
        Return the top k node calculated.

        Returns 
        -------
        top_nodes : list
            the top k nodes perfomed by a metric.
        '''

        return self.__top_k_nodes
    

    
    def pagerank(self, k, alpha = 0.85, max_iter = 100, dangling = None):
        '''
        Apply the pagerank metric returning a dictionaryof tuples where each contains a node with its own score, 
        sort the nodes from the score in descending order so as to have a rank and select the first k nodes.

        Parameters
        ----------
        k : int 
            Number of top nodes obtained from the application of the metric.

        alpha : float
            Alpha value for pagerank algorithm.

        max_iter : int
            Maximum number of iterations of the pagerank algorithm.

        dandling : dict
            Dictionary of nodes without any outedges.
        '''
        
        pagerank_dict = nx.pagerank(G = self.__year_graph,
                                    alpha = alpha,
                                    max_iter = max_iter,
                                    dangling = dangling)

        pagerank_tuple = [pair for pair in pagerank_dict.items()]
        pagerank_tuple.sort(key = lambda i : i[1], reverse = True)
        self.__top_k_nodes = pagerank_tuple[:k]
    


    def node_betweenness(self, k, k_samples = None, normalized = True, weight = None, endpoints = False, seed = None):
        '''
        Apply the betweenness (node betweenness) metric returning a dictionary of tuples where each contains a node with its own score, 
        sort the nodes from the score in descending order so as to have a rank and select the first k nodes.

        Parameters
        ----------
        k : int
            Number of top nodes obtained from the application of the metric. 

        k_samples : int, optional
            k node samples to estimate betweenness. k_samples must be <= graph's number of nodes.

        normalized : bool, optional
            If True the betweenness values are normalized by 2/(n(n-1)) for graphs, 
            and 1/(n(n-1)) for directed graphs where n is the number of nodes in G.

        weight : None or string, optional (default = None)
            If None, all edge weights are considered equal. Otherwise holds the name of the edge attribute used as weight.

        endpoints : bool, optional
            If True include the endpoints in the shortest path counts.

        seed : integer, random_state, or None (default = None), optional
            Indicator of random number generation state. Note that this is only used if k is not None.
        '''
        
        between_dict = nx.betweenness_centrality(G = self.__year_graph,
                                                 k = k_samples,
                                                 normalized = normalized,
                                                 weight = weight,
                                                 endpoints = endpoints,
                                                 seed = seed)

        between_tuple = [pair for pair in between_dict.items()]
        between_tuple.sort(key = lambda i : i[1], reverse = True)
        self.__top_k_nodes = between_tuple[:k]

        
    
    def degree_centrality(self, k):
        '''
        Apply the degree centrality metric returning a dictionary where each contains a node with its own score, 
        sort the nodes from the score in descending order so as to have a rank and select the first k nodes.

        Parameters
        ----------
        k : int
            Number of top nodes obtained from the application of the metric.
        '''
        
        degree_nodes = nx.degree_centrality(G = self.__year_graph)
    
        degree_tuple = [pair for pair in degree_nodes.items()]
        degree_tuple.sort(key = lambda i : i[1], reverse = True)
        self.__top_k_nodes = degree_tuple[:k]
    

                                                    

