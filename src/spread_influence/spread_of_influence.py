#####################################################################################################
#                                                                                                   #
# FileName    [spread_of_influence.py]                                                              #
#                                                                                                   #
# PackageName [spread_influence]                                                                    #
#                                                                                                   #
# Synopsis    [This file contains the class to apply the spread of influence algorithms selected    #
#              by returning the influenced nodes iteration by iteration. The different algorithms   #
#              are executed according to the calculation method of the chosen threhold.]            #
#                                                                                                   #
# Author      [Leonardo Picchiami]                                                                  #
#                                                                                                   #
#####################################################################################################




import networkx as nx
import random
import copy

import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ids

import future.utils


class SpreadOfInfluenceModels(object):
    '''
    Class for the use of the two spread of influence models chosen through the application of all three threshold calculation strategies devised.

    Attributes
    ----------
    year_graph : YearGraph or networkx.Graph
        - YearGraph object to get the graph of the ds-1 dataset on which to apply the spread of influence model. 
        - Graph object of the networkx library representing the graph of the ds1 dataset for a specific year.

    seed : list of tuples or list of strings. 
        - List of tuples where each tuple contains the node and the score obtained through the applied metric.
        - List of strings where each object is a node of the graph previously presented in a tuple.

    influenced : dict
        Dictionary where each key is an iteration and each value is the list of nodes recovered in that iteration
        by a spread of influence algorithm.

    threshold : int
        Threshold calculation mode.
        - If the spread of influence model is Tipping Model:
          - 0: 1 / year_graph.degree(n) (n is the node)
          - 1: 0.5
          - 2: 1 - (1 / year_graph.degree(n) (n is the node)
        - If the spread of influence models is Indipendent Cascade Model:
          - 0: 1 / ((year_graph.degree(e[0]) + year_graph.degree(e[0])) / 2)
          - 1: 0.5
          - 2: 1 - (1 / ((year_graph.degree(e[0]) + year_graph.degree(e[0])) / 2))  
    '''

    
    def __init__(self, year_graph, seed):
        '''
        Parameters
        ----------
        year_graph : YearGraph
            YearGraph object to get the graph of the ds-1 dataset on which to apply the spread of influence model.

        seed : list of tuples
            List of tuples that contains all the nodes to be used as seed where each node has its own score.
        '''
        
        self.__year_graph = year_graph
        self.__seed = seed
        self.__influenced = None

        
        
    def spread_preprocessing(self):
        '''
        Preprocessing method which saves the specific networkx graph of the ds-1 dataset in year_graph.
        It extrapolates also the list of nodes from the list of tuples for the seed set of spread of influence algorithms.
        '''
        
        self.__year_graph = self.__year_graph.get_ds1_graph()
        seed_nodes = [node[0] for node in self.__seed]
        self.__seed = list(seed_nodes)


        
    
    def get_influenced_nodes(self):
        '''
        Returns the influenced nodes iteration by iteration.

        Returns 
        -------
        influenced : dict
            Dictionary where each key is an iteration and each value is the list of nodes recovered in that iteration 
            by a spread of influence algorithm.
        '''
        
        return self.__influenced

    
    
    def threshold_deg(self):
        '''
        Set the threshold mode to 0
        '''

        self.__threshold = 0


        
    def threshold_half(self):
        '''
        Set the threshold mode to 1
        '''
        
        self.__threshold = 1

        

    def threshold_deg_neg(self):
        '''
        Set the threshold mode to 2
        '''
        
        self.__threshold = 2


      
    def tipping_threshold(self, n):
        '''
        Calculation of the threhsold according to the mode value set for the Tipping Model.

        Parameters
        ----------
        n : node (string)
            Node of networkx ds-1 graph
        '''
        
        if self.__threshold == 0:
            return 1 / self.__year_graph.degree(n)

        if self.__threshold == 1:
            return 0.5

        if self.__threshold == 2:
            return 1 - (1 / self.__year_graph.degree(n))
  

            
    def tipping_model(self):
        '''
        Configuration and execution of the Tipping Model algorithm, iteration is performed by iteration.
        
        Model execution is stopped when nodes are no longer influenced.
        '''
        
        model = ids.ThresholdModel(self.__year_graph)

        config = mc.Configuration()
        config.add_model_initial_configuration("Infected", self.__seed)

        for n in self.__year_graph.nodes():
            threshold = self.tipping_threshold(n)
            config.add_node_configuration('threshold', n, threshold)

        model.set_initial_status(config)

        self.__influenced = dict()
        while True:
            iteration = model.iteration()
            if len(iteration.get('status')) == 0:
                break

            self.__influenced['iteration {0}'.format(iteration.get('iteration'))] = []
            for k in iteration.get('status'):
                if iteration.get('status')[k] == 1:
                    self.__influenced['iteration {0}'.format(iteration.get('iteration'))].append(k)

        

    def cascade_threshold(self, e):
        '''
        Calculation of the threhsold according to the mode value set for the Indipendent Cascade Model.

        Parameters
        ----------
        e : edge (tuple of nodes)
            Edge of networkx ds-1 graph
        '''
        
        if self.__threshold == 0:
            return 1 / ((self.__year_graph.degree(e[0]) + self.__year_graph.degree(e[1])) / 2)

        if self.__threshold == 1:
            return 0.5

        if self.__threshold == 2:
            return 1 - (1 / ((self.__year_graph.degree(e[0]) + self.__year_graph.degree(e[1])) / 2))
  

    
    def indipendent_cascade_model(self):
        '''
        Configuration and execution of the Indipendent Cascade Model algorithm, iteration is performed by itetration.

        Model execution is stopped when nodes are no longer influenced.
        '''
        
        model = ids.IndependentCascadesModel(self.__year_graph)
        
        config = mc.Configuration()
        config.add_model_initial_configuration("Infected", self.__seed)
               
        for e in self.__year_graph.edges():
            threshold = self.cascade_threshold(e)
            config.add_edge_configuration('threshold', e, threshold)

        model.set_initial_status(config)
    
        self.__influenced = dict()
        while True:
            iteration = model.iteration()
            if len(iteration.get('status')) == 0:
                break
    
            lst = []
            for k in iteration.get('status'):
                if iteration.get('status')[k] == 1:
                    lst.append(k)
                    
            if len(lst) == 0:
                break
                    
            self.__influenced['iteration {0}'.format(iteration.get('iteration'))] = lst
    
     

                      
            
            
        
        
