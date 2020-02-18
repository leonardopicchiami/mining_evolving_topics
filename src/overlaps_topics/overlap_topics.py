###############################################################################################################
#                                                                                                             #
# FileName    [overlap_topics.py]                                                                             #
#                                                                                                             #
# PackageName [overlaps_topics]                                                                               #
#                                                                                                             #
# Synopsis    [This file contains the class to apply the Clique Percolation Method to the subgraph            #
#              relative to the keywords retrieved through the application of the spread of influence model,   #
#              identifying the topics of a given year.]                                                       #
#                                                                                                             #
# Author      [Leonardo Picchiami]                                                                            #
#                                                                                                             #
###############################################################################################################



import networkx as nx
from networkx.algorithms.community import k_clique_communities

import overlap_exception as excpt


class OverlapTopics(object):
    '''
    Class to apply the Clique Percolation Method (k_clique_communities) to the subgraph relative to the keywords recovered through 
    the application of the spread of influence model.
    In this way the topics of a given year are identified, however it must be checked that they maintain certain properties.

    Attributes
    ----------
    year_graph : YearGraph or networkx.Graph
        - YearGraph object to get the graph of the ds-1 dataset on which to extract the subgraph relative to nodes in all topics. 
        - Graph object of the networkx library representing the graph of the ds1 dataset for a given year.

    year_sub_graph : networkx.Graph
        Subgraph of the networkx graph relative to the ds-1 dataset containing all the nodes of topics.

    all_topics : dict
        Dictionary where each key is an iteration and each value is the list of nodes recovered in that iteration by a spread of influence algorithm.
    topics : list
        List containing all the topics of a given year. Each topic is a list of keywords, so it is a list of lists.

    k : int
        Number of generated topics.        
    '''

    
    def __init__(self, year_graph = None, all_topics = None, k = None):
        '''
        Parameters
        ----------
        year_graph : YearGraph, optional
            YearGraph object to get the graph of the ds-1 dataset on which to extract the subgraph relative to nodes in all topics.

        all_topics : list, optional
            Dictionary where each key is an iteration and each value is the list of nodes recovered in that iteration by a spread of influence algorithm.
        
        k : int, optional      
            Number of generated topics.
        '''
        self.__year_graph = year_graph
        self.__year_sub_graph = None
        self.__all_topics = all_topics
        self.__topics = []
        self.__k = k


        
    def get_topics(self):
        '''
        Returns the list of all the topics.

        Returns
        -------
        topics : list
            List containing all the topics of a given year. 
        '''
        
        return self.__topics

    
        
    def overlap_preprocessing(self):
        '''
        Preprocessing necessary to apply the Clique Percolation Method. 
        The dataset ds-1 graph is obtained from the YearGraph object and the subgraph relative to the nodes in all_topics is retrieved.
        '''
    
        self.__year_graph = self.__year_graph.get_ds1_graph()
        list_all_key = []
        for it in self.__all_topics:
            list_all_key += self.__all_topics[it] 

        self.__year_sub_graph = self.__year_graph.subgraph(list_all_key)


        
    def check_keywords(self, topic):
        '''
        Check if at least one of the keywords retrieved through the chosen metric is in the topic passed in input.

        Parameters
        ----------
        topic : list
            List of keywords representing a traced topic.

        Raises
        ------
        TopicMalFormedException : exception
            Exception indicating that a topic is not well formed. 
            It does not contain any representative keywords of the generated k topics: it cannot happen.
        '''
        
        regular = False
        for keyword in topic:
            if keyword in self.__all_topics['iteration 0']:
                regular = True
                break

        if not regular:
            raise excpt.TopicMalFormedException("Topic bad formed.")


        
    def clique_percolation_method(self):
        '''
        Application of the clique percolation method to find k communities. In this case the k topics.

        The smallest clique that the method can identify is large 2.
        '''
        
        communities = k_clique_communities(G = self.__year_sub_graph, k = 2)
        for topic in communities:
            self.check_keywords(topic)
            self.__topics.append(list(topic))

            

    def check_spread_topics(self):
        '''
        Check if the topics found by the clique percolation method contain all the keywords in all_topics.

        Raises
        ------
        TopicNotAllKeywordsUsedException : exception
            Exceptions indicating that at least one of the keywords recovered is not part of any topic.
        '''
        
        size_iteration = 0
        size_topics = 0
        for k in self.__all_topics:
            size_iteration += len(self.__all_topics[k])

        for topic in self.__topics:
            size_topics += len(topic)

        if size_iteration != size_topics:
            raise excpt.TopicNotAllKeywordsUsedException("To perfom all topics not all keywords have been used.")

        

    def check_number_topics(self):
        '''
        Check if the number of arguments generated by the Clique percolation method is at most the arguments generated.

        Raises
        ------
        TopicTooManyException : exception
            Exception indicating whether the number of topics generated by the clique percolation method is greater than k.
        '''
        
        if len(self.__topics) > self.__k:
            raise TopicTooManyException("Many topics have been formed.")

            
        
