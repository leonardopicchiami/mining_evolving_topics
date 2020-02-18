###############################################################################################
#                                                                                             #
# FileName    [sample_overlapmerge_analysis.py]                                               #
#                                                                                             #
# PackageName [overlaps_topics.analysis]                                                      #
#                                                                                             #
# Synopsis    [Python script to analyze the application of the clique percolation method      #
#              in a given year depending on the spread of influence model and                 #
#              the threshold calculation strategy selected among those chosen.]               #
#                                                                                             #
# Author      [Leonardo Picchiami]                                                            #
#                                                                                             #
###############################################################################################




import warnings
warnings.filterwarnings("ignore")

import sys
import traceback
import argparse as arg

sys.path.append("..")
sys.path.append("../../graph")
sys.path.append("../../metrics")
sys.path.append("../../spread_influence")
sys.path.append("../../utils")

import graph as gr
import metrics as me
import spread_of_influence as sp
import overlap_topics as ov
import overlap_exception as excpt
import utils as ut
import man

ds1_path = "../../../dataset_src/ds-1.tsv"
ds2_path = "../../../dataset_src/ds-2.tsv"

output_sample_path = "../../../output_sample/overlap-merge_analysis/"

save_logs = False


def to_print(models, overlap):
    #for k in models.get_influenced_nodes():
     #   print("{0} : {1}{2}len_iteration: {3}{4}".format(k, models.get_influenced_nodes()[k], '\n', len(models.get_influenced_nodes()[k]), '\n'))
          
    for topic in overlap.get_topics():
        print("{0}{1}len_topic: {2}{3}".format(topic, '\n', len(topic), '\n'))
    

def save_topics(name_file_log, comment, overlap):
    global output_sample_path
    if output_sample_path[-1] != '/':
        output_sample_path += '/'
        
    out_path = output_sample_path + name_file_log
    with open(out_path, 'a') as f:
        f.write("{0}{1}".format(comment, '\n\n'))
        for topic in overlap.get_topics():
            f.write("{0}{1}len_topic: {2}{3}".format(topic, '\n', len(topic), '\n\n'))

    

if __name__ == '__main__':
    parser = arg.ArgumentParser("Analize merge topics based on overlap.", conflict_handler = 'resolve')

    #Usage argument
    parser.add_argument('-h', action = 'store_true', dest = 'h')

    #Year argument
    parser.add_argument('-y', action = 'store', dest = 'y')

    #Paths input and output paths options
    parser.add_argument('-ds1_p', action = 'store', dest = 'ds1_path')
    parser.add_argument('-ds2_p', action = 'store', dest = 'ds2_path')
    parser.add_argument('-o', action = 'store', dest = 'out')
    
    #k value to retrieve top k nodes according metrics method
    parser.add_argument('-k', action = 'store', dest = 'k')

    #Spread of influence models argument
    parser.add_argument('-sp', action = 'store', dest = 'spread')

    #Threshold mode for influence models argument
    parser.add_argument('-t', action = 'store', dest = 'threshold')

    #Store file option
    parser.add_argument('-s', action = 'store_true', dest = 's')

    results = parser.parse_args()


    
    #Usage controls and settings
    if results.h and len(sys.argv) > 2:
        parser.error("With the -h option it is not possible to specify other options.")

    if results.h:
        ut.print_usage(man.usage_overlapmerge_analysis)


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

    
    #Spread value controls and setting
    if not results.spread:
        raise parser.error("Must to specify the spread of influence model: -sp SP")

    try:
        spread = int(results.spread)    
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_value = ValueError("The spread value must be an integer.")
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stderr)
        sys.exit(-1)

    spread_value = [0, 1]
    if spread not in spread_value:
        raise arg.ArgumentTypeError('The value for the sp must be 0 or 1.')

    
    #T value controls and settings
    if not results.threshold:
        raise parser.error("Must to specify the spread of influence model threshol mode: -t T")

    try:
        t = int(results.threshold)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_value = ValueError("The threshold mode  must be an integer.")
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stderr)
        sys.exit(-1)

    threshold_value = [0, 1, 2]
    if t not in threshold_value:
        raise arg.ArgumentTypeError('The value for the t must be 0 or 1.')

    
    #Argument input and output path settings
    if results.ds1_path:
        ds1_path = results.ds1_path

    if results.ds2_path:
        ds2_path = results.ds2_path

    if results.out and not results.s:
        raise parser.error("Must to specify the save flag with the output path: -s.")

    if results.out:
        output_sample_path = results.out
    
    #Save file flag     
    if results.s:
        save_logs = True

    
    #Building graph, with weights calculation strategy or not
    year_graph = gr.YearGraph(ds1_path, ds2_path, y)
    year_graph.read()
    year_graph.weights_fraction_cocitations()
    year_graph.build_ds1_graph()

    metrics = me.Metrics(year_graph)
    metrics.metrics_preprocessing()
    metrics.pagerank(k)

    models = sp.SpreadOfInfluenceModels(year_graph, metrics.get_top_k_nodes())
    models.spread_preprocessing()
 
    if t == 0:
        models.threshold_deg()
        threshold = "degree"

    elif t == 1:
        models.threshold_half()
        threshold = "half"

    else:
        models.threshold_deg_neg()
        threshold = "degree negative"
        

    if spread == 0:
        models.indipendent_cascade_model()
        name = "cascade"

    else:
        models.tipping_model()
        name = "tipping"


    ov_top = ov.OverlapTopics(year_graph, models.get_influenced_nodes(), k)
    ov_top.overlap_preprocessing()
    ov_top.clique_percolation_method()
    ov_top.check_number_topics()
    ov_top.check_spread_topics()
    
    if not save_logs:
        to_print(models, ov_top)

    else:
        out_name = "overlap_topics_{0}_y{1}_k{2}_t{3}.log".format(name, y, k, t)
        comment = "Overlapping topic result with {0} spread of influence model, seed top {1} nodes and {2} threshold calculation strategy.".format(name, k, threshold)
        save_topics(out_name, comment, ov_top)
    
