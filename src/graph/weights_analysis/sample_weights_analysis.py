##########################################################################################################
#                                                                                                        #
#  FileName    [sample_weights_analysis.py]                                                              #
#                                                                                                        #
#  PackageName [graph.weights_analysis]                                                                  #
#                                                                                                        #
#  Synopsis    [Python script to analyze both the weightscalculation strategies on ds-1 dataset graph    #
#               of a given year of the timeline]                                                         #
#                                                                                                        #
#  Author      [Leonardo Picchiami]                                                                      # 
#                                                                                                        #
#########################################################################################################



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
output_sample_path = "../../../output_sample/weights_analysis/"

plot_show_flag_histogram = True


if __name__ == '__main__':
    parser = arg.ArgumentParser("Plotting histogram of weight distribution", conflict_handler = 'resolve')

    #Usage argument
    parser.add_argument('-h', action = 'store_true', dest = 'h')

    #Argument year option
    parser.add_argument('-y', action = 'store', dest = "y")

    #Path input and output paths options
    parser.add_argument('-ds1_p', action = 'store' , dest = 'ds1_path')
    parser.add_argument('-ds2_p', action = 'store', dest = 'ds2_path')
    parser.add_argument('-o', action = 'store', dest = 'out')

    #Plot flag for drawing or saving the histogram
    parser.add_argument('--plot', action = 'store_true', dest = 'plot')

    #Weights mode option
    parser.add_argument('-w', action = 'store', dest = 'weights')
    
    results = parser.parse_args()

    
    #Usage controls and settings
    if results.h and len(sys.argv) > 2:
        parser.error("With the -h option it is not possible to specify other options.")

    if results.h:
        ut.print_usage(man.man_weights_analysis)

    
    #Year value controls
    if not results.y:
        raise parser.error('Must to specify the year value: -y Y')
    
    try:
        y = int(results.y)
    except ValueError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exc_value = ValueError("The year value must be an integer")
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stderr)
        sys.exit(-1)
    
    if y < 2000 or y > 2018:
        raise arg.ArgumentTypeError('The value for the year must be between 2000 and 2018 inclusive.')


    #Argument input and output path controls and settings
    if results.out and results.plot:
        raise parser.error('Needless to specify the output path if you are showing the plot.')
   
    if results.ds1_path:
        ds1_path = results.ds1_path

    if results.ds2_path:
        ds2_path = results.ds2_path

    if results.out:
        output_sample_path = results.out


    #weights histogram plotting control and setting
    if results.plot:
        plot_show_flag_histogram = False


    #Building and plotting of the histogram 
    year_graph = gr.YearGraph(ds1_path, ds2_path, results.y)
    year_graph.read()

    if results.weights == 'frac':
        year_graph.weights_fraction_cocitations()
        
    elif results.weights == 'num':
        year_graph.weights_number_cocitations()

    elif results.weights == None:
        raise parser.error("The -w WEIGHT options must be specified.")

    else:
        raise arg.ArgumentTypeError("Option value not valid.")

    
    if plot_show_flag_histogram:
        if output_sample_path[-1] != '/':
            output_sample_path += '/'

        out_path = output_sample_path + "weights_{0}".format(y)
        os.makedirs(out_path, exist_ok = True)
        year_graph.plot_weights(save_fig = True, save_path = out_path)

    else:
        year_graph.plot_weights()

    
