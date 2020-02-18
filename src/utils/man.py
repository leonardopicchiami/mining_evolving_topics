##############################################################################################
#                                                                                            #
# FileName    [man.py]                                                                       #
#                                                                                            #
# PackageName [utils]                                                                        #
#                                                                                            #
# Synopsis    [File that contains the man pages of each script and the main file.            #
#             Each man contains the script name, script description synopsis and options.]   #
#                                                                                            #
# Author      [Leonardo Picchiami]                                                           #
#                                                                                            #
##############################################################################################





import textwrap


'''
Man page for options and use of the script: sample_graph_analysis.py
'''
man_graphs_exploration = textwrap.dedent('''
                           NAME

                               sample_graph_analysis.py

                           
                           DESCRIPTION
      
                               Python script to analyze both the weights calculation strategies on ds-1 dataset graph of a given year of the timeline.


                           SYNOPSIS

                               python sample_graph_analysis.py -h
                               python sample_graph_analysis.py -y Y {-t|-c|-a} [--ds1|--ds1 --show_ds1|--ds2|--ds2 --show_ds2|--show_ds1|--show_ds2|--show_ds1 --show_ds2] [-ds1_p path] [-ds2_path path] [-o path]

                                
                           OPTIONS

                                -h               usage option
                                -y Y             year of the timeline. Value must be in [2000 - 2018]
                                --ds1            flag to compute the ds-1 dataset
                                --ds2            flag to compute the ds-2 dataset
                                -c               flag to compute only connected components of the graph
                                -t               flag to compute only entire graph 
                                -a               flag to compute both the connected components and the entire graph
                                -ds1_p path      path of the ds-1 dataset
                                -ds2_p path      path of the ds-2 dataset
                                -o path          path of the output
                                --show_ds1       flag to show the ds-1 computation; by default is saved
                                --show_ds2       flag to show the ds-2 computation; by default is saved

                          ''')




'''
Man page for options and use of the script: sample_weights_analysis.py
'''
man_weights_analysis = textwrap.dedent('''
                         NAME
  
                             sample_weights_analysis.py


                         DESCRIPTION

                             Python script to analyze the entire structure and all the connected components of the ds-1 and ds-2 dataset
                             graphs of a given year of the timeline.                             


                         SYNOPSIS
                             
                             python sample_weights_analysis.py -h
                             python sample_weights_analysis.py -y Y {-w frac|-w num} [--plot] [-ds1_p path] [-ds2_p path] [-o path]


                         OPTIONS

                             -h             usage option
                             -y Y           year of the timeline. Value must be in [2000 - 2018]
                             -ds1_p path    path path of the ds-1 dataset
                             -ds2_p path    path path of the ds-2 dataset
                             -o path        path of the output
                             --plot         flag to show the weights distribution
                             -w mode        weights strategy mode: 
                                            -  frac fraction calculation strategy
                                            -  num  number calculation strategy
       
                         ''')



'''
Man page for options and use of the script: sample_metrics_analysis.py
'''
usage_pagerank_analysis = textwrap.dedent('''
                            NAME
                           
                                sample_metrics_analysis.py


                            DESCRIPTION

                                Python script to analyze the metrics taken into account on the graph of the ds-1 dataset of a given year. 
                                For the metrics that use weights, it is analyzed with both weighting strategies.

 
                           SYNOPSIS

                                python sample_metrics_analysis.py -h
                                python sample_metrics_analysis.py -y Y -k K {-m 0 -w frac|-m 0 -w num|-m 1|-m 2} [-ds1_p path] [-ds2_p path] [-s|-s -o path]

                           
                           OPTIONS

                                -h             usage option
                                -y Y           year of the timeline. Value must be in [2000 - 2018]
                                -ds1_p path    path path of the ds-1 dataset
                                -ds2_p path    path path of the ds-2 dataset
                                -o path        path of the output
                                -s             flag to save the results
                                -k K           number of top nodes retrivied from the rank obtained through a metric. Must be between: [5, 10, 20, 100]
                                -w mode        weights strategy mode:
                                               -  frac fraction calculation strategy
                                               -  num  number calculation strategy
                                -m mode        metric mode:
                                               -  0 pagerank metric
                                               -  1 betweenness (node betweenness) metric
                                               -  2 degree centrality metric
                                
                                  
                           ''')



'''
Man page for options and use of the script: sample_influence_analysis.py
'''
usage_spread_influence_analysis = textwrap.dedent('''
                                                  NAME

                                                      sample_influence_analysis.py


                                                  DESCRIPTION

                                                      Python script to analyze the spread of influce models chosen on the ds-1 dataset graph 
                                                      of a given year by selecting the threhsold calculation strategy.

                                                   
                                                  SYNOPSYS

                                                      python sample_influence_analysis.py -h
                                                      python sample_influence_analysis.py -y Y -k K {-t 0|-t 1|-t 2} {-sp 0|-sp 1} [-ds1_p path] [-ds2_p path] [-s|-s -o path] 

                                                  OPTIONS
                                                      
                                                      -h             usage option
                                                      -y Y           year of the timeline. Value must be in [2000 - 2018]
                                                      -ds1_p path    path path of the ds-1 dataset
                                                      -ds2_p path    path path of the ds-2 dataset
                                                      -o path        path of the output
                                                      -s             flag to save the results
                                                      -k K           number of top nodes retrivied from the rank obtained through a metric. Must be between: [5, 10, 20, 100]
                                                      -t T           threshold strategy mode:
                                                                     -  0 threshold degree value
                                                                     -  1 threshold half value
                                                                     -  2 threshold degree negative value
                                                      -sp SP         spread of influence mode:
                                                                     -  0 indipendent cascade model
                                                                     -  1 tipping model


                                                  ''')



'''
Man page for options and use of the script: sample_overlapmerge_analysis.py
'''
usage_overlapmerge_analysis = textwrap.dedent('''
                                              NAME
                                    
                                                  sample_overlapmerge_analysis.py


                                              DESCRIPTION
                                             
                                                  Python script to analyze the application of the clique percolation method 
                                                  in a given year depending on the spread of influence model and
                                                  the threshold calculation strategy selected among those chosen.

                                            
                                              SYNOPSIS
                       
                                                  python sample_overlapmerge_analysis.py -h
                                                  python sample_overlapmerge_analysis.py -y Y -k K {-t 0|-t 1|-t 2} {-sp 0|-sp 1}  [-ds1_p path] [-ds2_p path] [-s|-s -o path]   
               
                                              OPTIONS
                                                  
                                                  -h             usage option
                                                  -y Y           year of the timeline. Value must be in [2000 - 2018]
                                                  -ds1_p path    path path of the ds-1 dataset
                                                  -ds2_p path    path path of the ds-2 dataset
                                                  -o path        path of the output
                                                  -s             flag to save the results
                                                  -k K           number of top nodes retrivied from the rank obtained through a metric. Must be between: [5, 10, 20, 100]
                                                  -t T           threshold strategy mode:
                                                                 -  0 threshold degree value
                                                                 -  1 threshold half value
                                                                 -  2 threshold degree negative value
                                                  -sp SP         spread of influence mode:
                                                                 -  0 indipendent cascade model
                                                                 -  1 tipping model

                                              ''')



'''
'''
usage_timelinetracing_analysis = textwrap.dedent('''
                                                 NAME

                                                     sample_timelinetracing_analysis.py
                                                    

                                                 DESCRIPTION

                                                     Python script to analyze the tracking system adopted and the chosen tracking metric.
                                                     For the tracking metric the threshold has been set and no other threshold is tested 
                                                     beyond that used; the effect is then analyzed for different values of k with fixed k.


                                                 SYNOPSIS
 
                                                     python sample_timelinetracing_analysis.py -h
                                                     python sample_timelinetracing_analysis.py -k K [-ds1_p path] [-ds2_p path] [-s|-s -o path]


                                                 OPTIONS

                                                     -h               usage option
                                                     -ds1_p path      path path of the ds-1 dataset
                                                     -ds2_p path      path path of the ds-2 dataset
                                                     -o path          path of the output
                                                     -s               flag to save the results
                                                     -k K             number of top nodes retrivied from the rank obtained through a metric. Must be between: [5, 10, 20, 100]
                                                 ''') 


'''
Man page for options and use of the script: main.py
'''
usage_main = textwrap.dedent('''
                             NAME

                                 main.py

                              
                             DESCRIPTION
 
                                 Python script that represents the main project. Performs the complete task of the project: it identifies all the topics on
                                 the timeline by modeling the graphs, retrieves the top k nodes, applies the chosen spread of influence model and combines 
                                 the topics via the clique percolation method. Subsequently for each topic of each year similar topics are traced and 
                                 there are similar topics traced on consecutive years (the first topic must be the initial one) are merged 
                                 into a single macro-topic.


                             SYNOPSIS

                                 python main.py -h
                                 python main.py --test_k5        (with my local paths)
                                 python main.py --test_k5_save   (with my local paths and save the result)
                                 python main.py --test_k10       (with my local paths and save the result)
                                 python main.py --test_k10_save  (with my local paths)
                                 python main.py -k K -ds1_p path -ds2_p path [-s -o path] 


                             OPTIONS

                                 -h               usage option
                                 --test_k5        complete test (with my local path) on k=5 and print the output
                                 --test_k5_save   complete test (with my local path) on k=5 and save the output on file
                                 --test_k10       complete test (with my local path) on k=10 and print the output  
                                 --test_k10_save  complete test (with my local path) on k=10 and save the output on file
                                 -ds1_p path      path path of the ds-1 dataset
                                 -ds2_p path      path path of the ds-2 dataset
                                 -o path          path of the output
                                 -s               flag to save the results
                                 -k K             number of top nodes retrivied from the rank obtained through a metric. Must be between: [5, 10, 20, 100]


                             ''')


