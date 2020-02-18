##############################################################################
#                                                                            #
# FileName    [sample_graph_analysis.py]                                     #
#                                                                            #
# PackageName [graph.exploration]                                            #
#                                                                            #
# Synopsis    [Python script to analyze the entire structure and all the     #
#             connected components of the ds-1 and ds-2 dataset graphs of a  #
#             given year of the timeline.]                                   #
#                                                                            #
# Author      [Leonardo Picchiami]                                           #
#                                                                            #
##############################################################################


import warnings
warnings.filterwarnings("ignore")

import sys
import traceback
import argparse as arg
import textwrap
import os

sys.path.append("..")
sys.path.append("../../utils")

import graph as gr
import utils as ut
import man

ds1_path = "../../../dataset_src/ds-1.tsv"
ds2_path = "../../../dataset_src/ds-2.tsv"
output_sample_path = "../../../output_sample/dataset_exploration/"

plot_show_flag_ds1 = True
plot_show_flag_ds2 = True


def ds1_exploration_sample(year_graph, comp, tot, both):
    '''
    Create the folder where to save the files if the flag to save is true. 
    Computes only the complete graph, only the connected components or both.

    If the flag is active, save the result.
    '''
    
    global output_sample_path
    if output_sample_path[-1] != '/':
        output_sample_path += '/'
        
    ds1_out_path = None
    if plot_show_flag_ds1:
        ds1_out_path = output_sample_path + "ds1_{0}/".format(year_graph.get_year())
        os.makedirs(ds1_out_path, exist_ok = True)
        
    year_graph.build_ds1_graph()

    if comp:
        year_graph.plot_ds1_components(save_fig = plot_show_flag_ds2, save_path = ds1_out_path)

    if tot:
        year_graph.plot_ds1_graph(save_fig = plot_show_flag_ds1, save_path = ds1_out_path)

    if both:
        year_graph.plot_ds1_graph(save_fig = plot_show_flag_ds1, save_path = ds1_out_path)
        year_graph.plot_ds1_components(save_fig = plot_show_flag_ds2, save_path = ds1_out_path)

   
def ds2_exploration_sample(year_graph, comp, tot, both):
    '''
    Create the folder where to save the files if the flag to save is true.
    Computes only the complete graph, only the connected components or both.

    If the flag is active, save the result.
    '''
    
    global output_sample_path
    if output_sample_path[-1] != '/':
        output_sample_path += '/'
        
    ds2_out_path = None
    if plot_show_flag_ds2:
        ds2_out_path = output_sample_path + "ds2_{0}/".format(year_graph.get_year())
        os.makedirs(ds2_out_path, exist_ok = True)
        
    year_graph.build_ds2_graph()

    if comp:
        year_graph.plot_ds2_components(save_fig = plot_show_flag_ds2, save_path = ds2_out_path)

    if tot:
        year_graph.plot_ds2_graph(save_fig = plot_show_flag_ds2, save_path = ds2_out_path)

    if both:
        year_graph.plot_ds2_graph(save_fig = plot_show_flag_ds2, save_path = ds2_out_path)
        year_graph.plot_ds2_components(save_fig = plot_show_flag_ds2, save_path = ds2_out_path)
    

        

if __name__ == '__main__':
    parser = arg.ArgumentParser("Plotting one year graph of dataset/s", conflict_handler = 'resolve')

    #Usage argument
    parser.add_argument('-h', action = 'store_true', dest = 'h')

    #Argument year option
    parser.add_argument('-y', action = 'store', dest = "y")

    #Path input and output paths options
    parser.add_argument('--ds1', action = 'store_true', dest = 'ds1')
    parser.add_argument('--ds2', action = 'store_true', dest = 'ds2')
    parser.add_argument('-o', action = 'store', dest = 'out')
    
    #Plot or save connected components, all graph or togheter
    parser.add_argument('-c', action = 'store_true', dest = 'comp')
    parser.add_argument('-t', action = 'store_true', dest = 'tot')
    parser.add_argument('-a', action = 'store_true', dest = 'both')
    
    #Path input and output paths  options
    parser.add_argument('-ds1_p', action = 'store' , dest = 'ds1_path')
    parser.add_argument('-ds2_p', action = 'store', dest = 'ds2_path')
    
    #Plot flag for plotting or drawing the graph drawings
    parser.add_argument('--show_ds1', action = 'store_true', dest = 'show_ds1')
    parser.add_argument('--show_ds2', action = 'store_true', dest = 'show_ds2')
    
    results = parser.parse_args()


    #Usage controls and settings
    if results.h and len(sys.argv) > 2:
        parser.error("With the -h option it is not possible to specify other options.")

    if results.h:
        ut.print_usage(man.man_graphs_exploration)
    

    #Year value controls
    if not results.y:
        parser.error("Must be specify the the option: -y Y")
    
    try:
        y = int(results.y)
    except ValueError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_value = ValueError("The year value must be an integer.")
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stderr)
        sys.exit(-1)
    
    if y < 2000 or y > 2018:
        raise arg.ArgumentTypeError('The value for the year must be between 2000 and 2018 inclusive.')

    
    #Argument input and output path controls and settings
    if results.out and (results.show_ds1 or results.show_ds2):
        raise parser.error('Needless to specify the output path if you are showing the plot.')
   
    if results.ds1_path:
        ds1_path = results.ds1_path

    if results.ds2_path:
        ds2_path = results.ds2_path

    if results.out:
        output_sample_path = results.out


    #Arguments 
    if not results.comp and not results.tot and not results.both:
        raise parser.error("You can  use -c or -t or -a")
    
    if results.comp and (results.tot or results.both):
        raise parser.error("You can't use -c together with -t or/and -a.")

    if results.tot and (results.comp or results.both):
        raise parser.error("You can't use -t together with -c or/and -a.")

    if results.both and (results.comp or results.tot):
        raise parser.error("You can't use -a together with -c or/and -t.")
    
        
    #ds1 and ds2 plotting graph controls and settings
    if results.ds1 and not results.ds2 and results.show_ds2:
        parser.error("Impossible to show ds2.")

    if not results.ds1 and results.ds2 and results.show_ds1:
        parser.error("Impossible to show ds1.")
        
    if results.show_ds1:
        plot_show_flag_ds1 = False

    if results.show_ds2:
        plot_show_flag_ds2 = False

        
    #Building and plotting of the graphs of a given year of ds1 and ds2 based on the options     
    year_graph = gr.YearGraph(ds1_path, ds2_path, results.y)
    year_graph.read()

    if results.ds1 and not results.ds2:     
        ds1_exploration_sample(year_graph, results.comp, results.tot, results.both)
        
    elif not results.ds1 and results.ds2:
        ds2_exploration_sample(year_graph, results.comp, results.tot, results.both)

    elif not results.ds1 and not results.ds2:
        ds1_exploration_sample(year_graph, results.comp, results.tot, results.both)
        ds2_exploration_sample(year_graph, results.comp, results.tot, results.both)
        
    else:
        raise parser.error('You cannot specify the ds1 and ds2 options together.')

