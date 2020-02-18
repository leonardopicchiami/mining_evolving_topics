###############################################################################################################################
#                                                                                                                             #
# FileName    [sample_timelinetracing_analysis.py]                                                                            #
#                                                                                                                             #
# PackageName [tracing_merge.analysis]                                                                                        #
#                                                                                                                             #
# Synopsis    [Python script to analyze the tracking system adopted and the chosen tracking metric.                           #
#              For the tracking metric the threshold has been set and no other threshold is tested beyond that used;          #
#              the effect is then analyzed for different values of k with fixed k.]                                           #
#                                                                                                                             #
# Author      [Leonardo Picchiami]                                                                                            #
#                                                                                                                             #
###############################################################################################################################



import warnings
warnings.filterwarnings("ignore")

import sys
import traceback
import argparse as arg

sys.path.append("..")
sys.path.append("../../graph")
sys.path.append("../../metrics")
sys.path.append("../../utils") 
sys.path.append("../../spread_influence")
sys.path.append("../../overlaps_topics")

import graph as gr
import metrics as me
import spread_of_influence as sp
import overlap_topics as ov
import tracing_merge as tr
import utils as ut
import man

ds1_path = "../../../dataset_src/ds-1.tsv"
ds2_path = "../../../dataset_src/ds-2.tsv"

output_sample_path = "../../../output_sample/timeline_tracing/"

save_logs = False



def T1(ds1_path, ds2_path, year, k):
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




    
if __name__ == '__main__':
    parser = arg.ArgumentParser("Analize top spread of influence models", conflict_handler = 'resolve')

    #Usage argument
    parser.add_argument('-h', action = 'store_true', dest = 'h')

    #Paths input and output paths options
    parser.add_argument('-ds1_p', action = 'store', dest = 'ds1_path')
    parser.add_argument('-ds2_p', action = 'store', dest = 'ds2_path')
    parser.add_argument('-o', action = 'store', dest = 'out')

    #k value to retrieve top k nodes according metrics method
    parser.add_argument('-k', action = 'store', dest = 'k')

    #Threshold mode for influence models argument
    parser.add_argument('-t', action = 'store', dest = 'threshold')

    #Store file option
    parser.add_argument('-s', action = 'store_true', dest = 's')

    results = parser.parse_args()

   
    #Usage controls and settings
    if results.h and len(sys.argv) > 2:
        parser.error("With the -h option it is not possible to specify other options.")

    if results.h:
        ut.print_usage(man.usage_timelinetracing_analysis)

        
    #K values controls
    if not results.k:
        raise parser.error('Must to specify the k value: -k K.')

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


    timeline_topics = dict()
    timeline = [str(year) for year in range(2000, 2019)]
    
    for year in timeline:
        timeline_topics[year] = T1(ds1_path, ds2_path, year, k)

    timeline_tracer = tr.TraceMergeTimeline(timeline_topics, k = k, tracing_save_path = output_sample_path)

    if save_logs:
        filename = output_sample_path + "tracing_k{0}_t{1}.log".format(k, 0.5)
        with open(filename, 'a') as f:
            f.write("TOPIC CHAINS TRACED ALONG THE TIMELINE\n\n\n")
            
        timeline_tracer.trace_timeline(mode = 1)
        
    else:
        print("TOPIC CHAINS TRACED ALONG THE TIMELINE\n\n\n")
        timeline_tracer.trace_timeline(mode = 0)

    
    


    


    
