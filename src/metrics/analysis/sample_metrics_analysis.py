#############################################################################################
#                                                                                           #
# FileName    [sample_metrics_analysis.py]                                                  #
#                                                                                           #
# PackageName [metrics.analysis]                                                            # 
#                                                                                           #
# Synopsis    [Python script to analyze the metrics taken into account on the graph         #
#              of the ds-1 dataset of a given year. For the metrics that use weights,       #
#              it is analyzed with both weighting strategies.]                              #
#                                                                                           #
# Author      [Leonardo Picchiami]                                                          #
#                                                                                           #
#############################################################################################




import warnings
warnings.filterwarnings("ignore")

import sys
import traceback
import argparse as arg

sys.path.append("..")
sys.path.append("../../graph")
sys.path.append("../../utils")

import graph as gr
import metrics as me
import utils as ut
import man

ds1_path = "../../../dataset_src/ds-1.tsv"
ds2_path = "../../../dataset_src/ds-2.tsv"
output_sample_path = "../../../output_sample/metrics_analysis/"

save_logs = False

def save_k_nodes(name_file_log, comment, nodes):
    global output_sample_path
    if output_sample_path[-1] != '/':
        output_sample_path += '/'
        
    out_path = output_sample_path + name_file_log
    with open(out_path, 'a') as f:
        f.write("{0}{1}".format(comment, '\n'))
        for i in nodes:
            f.write("{0}{1}".format(i, '\n'))

            
if __name__ == '__main__':
    parser = arg.ArgumentParser("Analize top k nodes according some metrics", conflict_handler = 'resolve')

    #Usage argument
    parser.add_argument('-h', action = 'store_true', dest = 'h')
    
    #Argument year option
    parser.add_argument('-y', action = 'store', dest = "y")

    #Paths input and output paths options
    parser.add_argument('-ds1_p', action = 'store' , dest = 'ds1_path')
    parser.add_argument('-ds2_p', action = 'store', dest = 'ds2_path')
    parser.add_argument('-o', action = 'store', dest = 'out')

    #save flag option
    parser.add_argument('-s', action = 'store_true', dest = 's')

    #k value to retrieve top k nodes according metrics method
    parser.add_argument('-k', action = 'store', dest = 'k')

    #weights calculation mode useful for some rank metrics 
    parser.add_argument('-w', action = 'store', dest = 'weights')

    #metrics mode useful to retrieve top k nodes
    parser.add_argument('-m', action = 'store', dest = 'm')

    results = parser.parse_args()


    #Usage controls and settings
    if results.h and len(sys.argv) > 2:
        parser.error("With the -h option it is not possible to specify other options.")

    if results.h:
        ut.print_usage(man.usage_pagerank_analysis)


    #Year value controls
    if not results.y:
        raise parser.error('Must to specify the year value: -y Y')

    try:
        y = int(results.y)
    except ValueError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_value = ValueError("The year value must be an integer.")
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stderr)
        sys.exit(-1) 

    if y < 2000 or y > 2018:
        raise arg.ArgumentTypeError('The value for the year must be between 2000 and 2018 inclusive')


    #Argument input and output path settings
    if results.ds1_path:
        ds1_path = results.ds1_path

    if results.ds2_path:
        ds2_path = results.ds2_path

    if results.out and not results.s:
        raise parser.error("Must to specify the save flag with the output path: -s.")

    if results.out:
        output_sample_path = results.out


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
    

    #Flag to save or not log file
    if results.s:
        save_logs = True

        
    #Argument selection controls
    if not results.m:
        raise parser.error('Must to specify the m value: -m M')

    try:
        m = int(results.m)
    except ValueError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_value = ValueError("The metric mode value must be an integer.")
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stderr)
        sys.exit(-1)

    m_values = [0, 1, 2]
    if m not in m_values:
        raise arg.ArgumentTypeError("Option metric mode not valid.")
    
        
    #Building graph, with weights calculation strategy or not, 
    year_graph = gr.YearGraph(ds1_path, ds2_path, y)
    year_graph.read()

    if m == 0: 
        if results.weights == 'frac':
            year_graph.weights_fraction_cocitations()
        
        elif results.weights == 'num':
            year_graph.weights_number_cocitations()

        elif results.weights == None:
            raise parser.error("The -w WEIGHT options must be specified.")

        else:
            raise arg.ArgumentTypeError("Option weights mode not valid.")

    else:
        if results.weights != None:
            raise parser.error("Must not specify weight strategy with betweennes or degre centrality metric.")


    year_graph.build_ds1_graph()
    
    metrics = me.Metrics(year_graph)
    metrics.metrics_preprocessing()
    if m == 0:
        metrics.pagerank(k)
        metric_label = 'pagerank'

    elif m == 1:
        metrics.node_betweenness(k)
        metric_label = 'node_between'

    elif m == 2:
        metrics.degree_centrality(k)
        metric_label = 'degree'
        

    if save_logs:
        if results.weights == None:
            out_name = "{0}_y{1}_k{2}.log".format(metric_label, y,  k)
            comment = "Top {0} nodes with metric {1} in year {2}\n".format(k, metric_label, y)
        else:
            out_name = "{0}_y{1}_k{2}_w{3}.log".format(metric_label, y, k, results.weights)
            comment = "Top {0} nodes with metric {1} and weight {2} calculation mode in year {3}.\n".format(k, metric_label, results.weights, y)
        
        save_k_nodes(out_name, comment, metrics.get_top_k_nodes())
    else:
        print("{0}{1}{2}".format('\n', metrics.get_top_k_nodes(), '\n'))



    
