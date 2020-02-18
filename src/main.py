#################################################################################################################################
#                                                                                                                               #
# FileName    [main.py]                                                                                                         #
#                                                                                                                               #
# PackageName [main]                                                                                                            #
#                                                                                                                               #
# Synopsis    [Python script that represents the main project. Performs the complete task of the project:                       #
#              it identifies all the topics on the timeline by modeling the graphs, retrieves the top k nodes,                  #
#              applies the chosen spread of influence model and combines the topics via the clique percolation method.          #
#              Subsequently for each topic of each year similar topics are traced and there are similar topics                  #
#              traced on consecutive years (the first topic must be the initial one) are merged into a single macro-topic.]     #
#                                                                                                                               #
# Author      [Leonardo Picchiami]                                                                                              #
#                                                                                                                               #
#################################################################################################################################




import warnings
warnings.filterwarnings("ignore")


import sys
sys.path.append('overlaps_topics')

import argparse as arg
import traceback

import graph.graph as gr
import metrics.metrics as me
import overlaps_topics.overlap_topics as ov
import tracing_merge.tracing_merge as tr
import spread_influence.spread_of_influence as sp
import utils.utils as ut
import utils.man as man



def test_k5(save):
    '''
    Performs a complete test with k = 5.

    Parameters
    ----------
    save : boolean
        Flag to save or print the result.
    '''
    
    ds1_path = '../dataset_src/ds-1.tsv'
    ds2_path = '../dataset_src/ds-2.tsv'
    out_path = '../output_sample/main_output'

    all_topics = T2(ds1_path, ds2_path, 5)
    ut.out_main_result(save, out_path, all_topics, 5)

    

def test_k10(save):
    '''
    Performs a complete test with k = 10.

    Parameters
    ----------
    save : boolean
        Flag to save or print the result.
    '''
    
    
    ds1_path = '../dataset_src/ds-1.tsv'
    ds2_path = '../dataset_src/ds-2.tsv'
    out_path = '../output_sample/main_output'

    all_topics = T2(ds1_path, ds2_path, 10)
    ut.out_main_result(save, out_path, all_topics, 10)

    

def T1(ds1_path, ds2_path, year, k):
    '''
    Performs all operations of T1 task.

    Parameters
    ----------
    ds1_path : str
        Path of the ds-1 dataset.

    ds1_path : str
        Path of the ds-2 dataset

    k : int
        Number of generated topics for every year.
    '''
  
    year_graph = gr.YearGraph(ds1_path, ds2_path, year)
    year_graph.read()
    year_graph.weights_fraction_cocitations()
    year_graph.build_ds1_graph()

    metrics = me.Metrics(year_graph)
    metrics.metrics_preprocessing()
    metrics.pagerank(k)

    models = sp.SpreadOfInfluenceModels(year_graph, metrics.get_top_k_nodes())
    models.spread_preprocessing()
    models.threshold_deg()
    models.tipping_model()
    
    ov_top = ov.OverlapTopics(year_graph, models.get_influenced_nodes(), k)
    ov_top.overlap_preprocessing()
    ov_top.clique_percolation_method()
    ov_top.check_number_topics()
    ov_top.check_spread_topics()

    return ov_top.get_topics()



def T2(ds1_path, ds2_path, k):
    '''
    Performs all operations of T2 task.

    Parameters
    ----------
    ds1_path : str
        Path of the ds-1 dataset.

    ds1_path : str
        Path of the ds-2 dataset

    k : int
        Number of generated topics for every year.
    '''
    
    timeline = [str(i) for i in range(2000, 2019)]
    timeline_topics = dict()

    for year in timeline:
        timeline_topics[year] = T1(ds1_path, ds2_path, year, k) 

    timeline_tracer = tr.TraceMergeTimeline(timeline_topics)
    timeline_tracer.trace_timeline(merge = True, mode = 2)

    return timeline_tracer.get_topics_timeline()

    
    

def main():
    '''
    Main function that manages the script
    '''
    
    parser = arg.ArgumentParser("Main argument parser.", conflict_handler = 'resolve')

    #Usage argument
    parser.add_argument('-h', action = 'store_true', dest = 'h')
    
    #Paths input and output paths options
    parser.add_argument('-ds1_p', action = 'store', dest = 'ds1_path')
    parser.add_argument('-ds2_p', action = 'store', dest = 'ds2_path')
    parser.add_argument('-o', action = 'store', dest = 'out')

    #k value to retrieve top k nodes according metrics method
    parser.add_argument('-k', action = 'store', dest = 'k')
    
    #Store file option
    parser.add_argument('-s', action = 'store_true', dest = 's')

    #Local tests k=5 and k=10 options
    parser.add_argument('--test_k5', action = 'store_true', dest = 'test_k5')
    parser.add_argument('--test_k5_save', action = 'store_true', dest = 'test_k5_save')
    parser.add_argument('--test_k10', action = 'store_true', dest = 'test_k10')
    parser.add_argument('--test_k10_save', action = 'store_true', dest = 'test_k10_save')
    
    results = parser.parse_args()

    
    #Usage controls and settings
    if results.h and len(sys.argv) > 2:
        parser.error("With the -h option it is not possible to specify other options.")

    if results.h:
        ut.print_usage(man.usage_main)


    #Test with k=5 controls and print in stdout the execution
    if results.test_k5 and len(sys.argv) > 2:
        parser.error("With the --test_k5 option it is not possible to specify other options.")
        
    if results.test_k5:
        test_k5(False)
        return

    
    #Test with k=5 controls and save the execution
    if results.test_k5_save and len(sys.argv) > 2:
        parser.error("With the --test_k5 option it is not possible to specify other options.")

    if results.test_k5_save:
        test_k5(True)
        return


    
    #Test with k=10 controls and print in stdout the execution
    if results.test_k10 and len(sys.argv) > 2:
        parser.error("With the --test_k10 option it is not possible to specify other options.")
        
    if results.test_k10:
        test_k10(False)
        return


    #Test with k=10 controls and save the execution
    if results.test_k10_save and len(sys.argv) > 2:
        parser.error("With the --test_k10 option it is not possible to specify other options.")
        
    if results.test_k10_save:
        test_k10(True)
        return


    
    #Paths and flags all test control
    if not results.ds1_path:
        parser.error('Must to specify the ds-1 dataset path: -ds1_p path')

    if not results.ds2_path:
        parser.error('Must to specify the ds-2 dataset path: -ds2_p path')

    if results.s and (not results.out):
        parser.error('Must to specify the out path with save flag: -o path')

    if results.out and not results.s:
        parser.error('Must to specify the save flag with the out path: -s')

            
    #K values controls
    if not results.k:
        raise parser.error('Must to specify the k value: -k K')

    try:
        k = int(results.k)
    except ValueError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_value = ValueError("The k value must be an integer.")
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stderr)
        sys.exit(-1)
        
        top_k_values = [5, 10, 20, 100]
        if k not in top_k_values:
            raise arg.ArgumentTypeError('The value for the k must be 5, 10, 20 or 100.')

        
    all_topics = T2(results.ds1_path, results.ds2_path, k)

    ut.out_main_result(results.s, results.out, all_topics, k)

    

if __name__ == '__main__':
    main()
