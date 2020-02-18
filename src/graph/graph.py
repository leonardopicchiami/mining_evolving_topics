#############################################################################################################
#                                                                                                           #
# FileName    [graph.py]                                                                                    #
#                                                                                                           #
# PackageName [graph]                                                                                       #
#                                                                                                           #
# Synopsis    [This file contains a class for modeling and managing datasets as graphs:                     #
#             models the two datasets ds-1 and ds-2 as graphs, calculates the weights for the graph         #
#             relative to a given year of the ds-1 dataset for both the strategies proposed and finally     #
#             plots both the graphs of a specific year and the distribution of the calculated weights.]     #
#                                                                                                           #  
# Author      [Leonardo Picchiami]                                                                          #
#                                                                                                           #
#############################################################################################################


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import networkx as nx

import json


class YearGraph(object):
    """
    Class for modeling and managing datasets as graphs: models the two datasets ds-1 and ds-2 as graphs, 
    calculates the weights for the graph relative to a given year of the ds-1 dataset for both the strategies proposed and finally plots
    both the graphs of a specific year and the distribution of the calculated weights.


    Attributes
    ----------
    ds1_path : str
        The path of ds-1 dataset.

    ds2_path : str
        The path of ds-2 dataset.

    ds1_dataset : DataFrame
        Pandas dataframe object related to the ds-1 dataset.

    ds1_dataset : DataFrame
        Pandas dataframe object related to the ds-2 dataset.

    ds1_graph : Graph
        Networkx graph object related to the ds-1 dataset. (default None)

    ds2_graph : Graph
        Networkx graph object related to the ds-1 dataset. (default None)

    year : str
        String representation of the year relative to both the respective graphs of the two datasets.

    ds1_weights : dict
        Dictionary of the weights of the graph ds-1 where the key is a pair of nodes, an edge, is the value is the weight of the edge. 
        (default None)

    label_weights : str
        Label indicating the weight calculation strategy. (default None)
    """

     
    def __init__(self, ds1_path, ds2_path, year):
        """
        Parameters
        ----------
        ds1_path : str
            The path of the ds-1 dataset.
        
        ds1_path : str
            The path of the ds-2 dataset.

        year : str
            The string representation of the year.
        """
        
        self.__ds1_path = ds1_path
        self.__ds2_path = ds2_path
        self.__ds1_graph = None
        self.__ds2_graph = None
        self.__year = year
        self.__ds1_weights = None
        self.__label_weights = None


        
    def read(self):
        '''
        Reads the tsv files related to the path used in the constructor.
        '''
        
        self.__ds1_dataset = pd.read_csv(self.__ds1_path, delimiter = '\t', names = ['Year', 'Key1', 'Key2', 'Author-Value'])
        self.__ds2_dataset = pd.read_csv(self.__ds2_path, delimiter = '\t', names = ['Year', 'Author1', 'Author2', 'N.Collaborations'])


        
    def build_ds1_graph(self):
       '''
       Creates the graph relative to the ds-1 dataset of the chosen year.

       If the weights have been calculated, assign the relative weight to each edge.
       '''
       
       self.__ds1_graph = nx.Graph()
       self.__ds1_dataset = self.__ds1_dataset.query("Year  == {0}".format(self.__year))
       key1 = self.__ds1_dataset['Key1'].drop_duplicates()
       key2 = self.__ds1_dataset['Key2'].drop_duplicates()
       
       for element in key1:
           self.__ds1_graph.add_node(element)

       for element in key2:
           if element not in self.__ds1_graph.nodes:
               self.__ds1_graph.add_node(element)        

       if self.__ds1_weights == None:
           for index, element in self.__ds1_dataset[['Key1', 'Key2', 'Author-Value']].iterrows():
               self.__ds1_graph.add_edge(element[0], element[1])
       else:
           for index, element in self.__ds1_dataset[['Key1', 'Key2', 'Author-Value']].iterrows():
               self.__ds1_graph.add_edge(element[0], element[1], weight = self.__ds1_weights[(element[0], element[1])])


               
    def build_ds2_graph(self):
        '''
        Creates the graph relative to the ds-2 dataset of the chosen year.

        In this case the dataset provides the weight for each edge, so each edge with its relative weight is added.        
        '''
        
        self.__ds2_graph = nx.Graph()
        self.__ds2_dataset = self.__ds2_dataset.query("Year == {0}".format(self.__year))
        key1 = self.__ds2_dataset['Author1'].drop_duplicates()
        key2 = self.__ds2_dataset['Author2'].drop_duplicates()

        for element in key1:
            self.__ds2_graph.add_node(element)

        for element in key2:
            if element not in self.__ds2_graph.nodes:
                 self.__ds2_graph.add_node(element)

        for index, element in self.__ds2_dataset[['Author1', 'Author2', 'N.Collaborations']].iterrows():
            self.__ds2_graph.add_edge(element[0], element[1], weight = element[2])



           
    def get_ds1_graph(self):
        '''
        Returns the networkx graph object of ds-1 dataset.

        Returns
        -------
        ds1_graph : Graph
            the networkx graph object of ds-1 dataset.
        '''
        
        return self.__ds1_graph

    
    
   
    def get_ds2_graph(self):
        '''
        Returns the networkx graph object of ds-2 dataset.
        
        Returns
        -------
        ds1_graph : Graph
            the networkx graph object of ds-2 dataset.
        '''
        
        return self.__ds2_graph

    
    
    
    def get_year(self):
        '''
        Returns the string representation of the chosen year.
        
        Returns
        -------
        year : str
            the string representation of the year
        '''
        
        return self.__year


    
    def plot_ds1_graph(self, save_fig = False, save_path = None):
        '''
        Plots the entire graph of ds-1 dataset relative to the chosen year. 

        If the flag save_fig is True and the path is valid, the plotted graph is saved.

        Parameters
        ----------
        save_fig : bool, optional
            Flag used to save the plot figure.

        save_path : str, optional
            Path used where save the plot figure.
        '''
        
        pos = nx.spring_layout(self.__ds1_graph, scale = 3) 
        nx.draw_networkx_nodes(self.__ds1_graph, pos,  node_size = 250, font_weight = 'bold')
        nx.draw_networkx_edges(self.__ds1_graph, pos, width = 1.5)
        plt.axis('off')
        if save_fig:
            if save_path[-1] != '/':
                save_path += '/'
            save = save_path + "tot_graph_{0}".format(self.__year)
            plt.savefig(save)
            plt.clf()
        else:
            plt.show()

            
        
    def plot_ds1_components(self, save_fig = False, save_path = None):
        '''
        Plot all the connected components from which the graph of the ds-1 dataset relative to the chosen year is formed.
        
        If the flag save_fig is True and the path is valid, the plotted connected components are saved.

        Parameters
        ----------
        save_fig : bool, optional
            Flag used to save the plot figure.

        save_path : str, optional
            Path used where save the plot figure.
        '''
        
        count = 0
        for c in nx.connected_components(self.__ds1_graph):
            sub = self.__ds1_graph.subgraph(c)
            nx.draw_networkx(sub, with_labels = False, font_weight = 'bold')
            plt.axis('off')
            if save_fig:
                if save_path[-1] != '/':
                    save_path += '/'
                save = save_path + "comp{0}_graph_{1}".format(count, self.__year)
                plt.savefig(save)
                plt.clf()
            else:
                plt.show()
            count += 1

            
            
    def plot_ds2_graph(self, save_fig = False, save_path = None):
        '''
        Plots the entire graph of ds-2 dataset relative to the chosen year. 

        If the flag save_fig is True and the path is valid, the plotted graph is saved.

        Parameters
        ----------
        save_fig : bool, optional
            Flag used to save the plot figure.

        save_path : str, optional
            Path used where save the plot figure.
        '''
        
        pos = nx.spring_layout(self.__ds2_graph) 
        nx.draw_networkx_nodes(self.__ds2_graph, pos, node_size = 150)
        nx.draw_networkx_edges(self.__ds2_graph, pos, width = 2)
        plt.axis('off')
        if save_fig:
            if save_path[-1] != '/':
                save_path += '/'
            save = save_path + "tot_graph_{0}".format(self.__year)
            plt.savefig(save)
            plt.clf()
        else:
            plt.show()

            
    
    def plot_ds2_components(self, save_fig = False, save_path = None):
        '''
        Plot all the connected components from which the graph of the ds-2 dataset relative to the chosen year is formed. 

        If the flag save_fig is True and the path is valid, the plotted connected components are saved.

        Parameters
        ----------
        save_fig : bool, optional
            Flag used to save the plot figure.

        save_path : str, optional
            Path used where save the plot figure.
        '''
        
        count = 0
        for c in nx.connected_components(self.__ds2_graph):
            sub = self.__ds2_graph.subgraph(c)
            pos = nx.spring_layout(sub)
            nx.draw_networkx(sub, pos = pos,  with_labels = False, font_weight = 'bold')
            plt.axis('off')
            if save_fig:
                if save_path[-1] != '/':
                    save_path += '/'
                save = save_path + "comp{0}_graph_{1}".format(count, self.__year)
                plt.savefig(save)
                plt.clf()
            else:
                plt.show()
            count += 1


            
    def weights_fraction_cocitations(self):
        '''
        Calculate the weighting strategy as a co-citation fraction made by authors who have all worked together at least once.

        In the ds-2 dataset each edge represents two authors who have collaborated, 
        so to see if n authors have all worked together we need to check if the subgraph formed by those authors is a clique.
        '''
        
        tmp_ds1_dataset = self.__ds1_dataset.query("Year  == {0}".format(self.__year))
        tmp_ds2_dataset = self.__ds2_dataset.query("Year  == {0}".format(self.__year))
        weights = dict()
        authors_collaborations = []

        for index, element in tmp_ds2_dataset[['Author1', 'Author2', 'N.Collaborations']].iterrows():
            authors_collaborations.append((element[0], element[1]))
 
        for index, element in tmp_ds1_dataset[['Key1', 'Key2', 'Author-Value']].iterrows():
            json_acceptable_string = element[2].replace("'", "\"")
            diz = json.loads(json_acceptable_string)
            
            total_cocit = 0
            for value in diz.values():
                total_cocit += value
            
            co_authored_cocit = 0
            graph = nx.Graph()
            for pair in authors_collaborations:
                if pair[0] in diz and pair[0] not in graph.nodes:
                   graph.add_node(pair[0])
                if pair[1] in diz and pair[1] not in graph.nodes:
                    graph.add_node(pair[1])
                if pair[0] in graph.nodes and pair[1] in graph.nodes and (pair[0], pair[1]) not in graph.edges:
                    graph.add_edge(pair[0], pair[1])

            clique = list(nx.find_cliques(graph.subgraph(diz.keys())))
            
            if len(clique) > 0:
                for i in clique[0]:
                    co_authored_cocit += diz[i]
            else:
                co_authored_cocit = 0
                
            weights[(element[0], element[1])] = (co_authored_cocit / total_cocit)

            self.__ds1_weights =  weights
            self.__label_weights = "fraction"


            
    def weights_number_cocitations(self):
        '''
        Calculate the weighting strategy as a number of co-citation relative to pair of keywords.

        The calculation is the sum of the values of the dictionary of each edge where the key is an author 
        and the value is the number of times that co-cited that pair of keywords.
        '''
        
        tmp_ds1_dataset = self.__ds1_dataset.query("Year  == {0}".format(self.__year))
        weights = dict()
        
        for index, element in tmp_ds1_dataset[['Key1', 'Key2', 'Author-Value']].iterrows():
            json_acceptable_string = element[2].replace("'", "\"")
            diz = json.loads(json_acceptable_string)

            count = 0
            for value in diz.values():
                count += int(value)
        
            weights[(element[0], element[1])] = count

        self.__ds1_weights = weights
        self.__label_weights = "number"
        

    
       
    def get_weights(self):
        '''
        Returns the dictionary of weights: the key is the edge and the value is the value of the weight.

        Returns
        -------
        ds1_weights : dict
            Dictionary of the weights
        '''
        
        return self.__ds1_weights


    
       
    def get_label_weights(self):
        '''
        Returns the label indicating the weights calculation strategy.

        Returns
        -------
        label_weights : str
            Label indicating the weights calculation strategy
        '''
        
        return self.__label_weights


    
    def plot_weights(self, save_fig = False, save_path = None):
        '''
        Plots a histogram relative to one of the two calculation strategies depending on which one was calculated. 

        If the flag save_fig è True and the path is valid, the histogram is saved.

        Parameters
        ----------
        save_fig : bool, optional
            Flag used to save the plot figure.

        save_path : str, optional
            Path used where save the plot figure.
        '''
        
        fig, ax = plt.subplots(1, 1)
        if type(max(self.__ds1_weights.values())) == float:
            bins = [i for i in np.arange(0, max(self.__ds1_weights.values()) + 0.2, 0.1)]
            ax.set_title("Histogram of weights fraction strategy distribution")
        else:
            bins = [i for i in range(0, max(self.__ds1_weights.values()) + 2)]
            ax.set_title("Histogram of weights number strategy distribution")
        ax.hist(self.__ds1_weights.values(), bins = bins, align = 'left')
        ax.set_xticks(bins[:-1])
        
        if save_fig:
            if save_path[-1] != '/':
                save_path += '/'
            save = save_path + "histogram_{0}_{1}".format(self.__label_weights, self.__year)
            plt.savefig(save)
            plt.clf()
        else:
            plt.show()
    
