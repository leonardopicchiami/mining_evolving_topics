#####################################################################
#                                                                   #
# FileName    [utils.py]                                            #
#                                                                   #
# PackageName [utils]                                               #
#                                                                   #
# Synopsis    [File that contains some useful functions.]           #
#                                                                   #
# Author      [Leonardo Picchiami]                                  #
#                                                                   #
#####################################################################



def print_usage(usage):
    '''
    Print the usage string and stop execution with exit code 0

    Parameters
    ----------
    usage : string
        string representing the man page of a script.
    '''

    print(usage)
    exit(0)



def out_main_result(save, path, all_topics, k):
    '''
    Print or write the final result (result of the main.py) of the system. 
    Print or write, therefore, the macro-topics identified along the timeline.

    Parameters
    ----------
    save : boolean
        Flag to save or print the output.

    path : string
        Path to save the result.

    all_topics : list
        List of all macro-topics identified along the timeline.

    k : int
        Number of generated topics.
    '''
    
    if save:
        out_path = str(path)
        if out_path[-1] != '/':
            out_path += '/'
            
        filename = out_path + "main_k{0}.log".format(k)
        with open(filename, 'a') as f:
            f.write("MACRO-TOPIC IDENTIFIED IN THE 2000-2018 TIMETABLE{0}".format('\n\n\n'))
            f.write("Number of macro-topics: {0}{1}".format(len(all_topics), '\n\n'))
            for topic in all_topics:
                f.write("{0}{1}{2}{3}".format(topic, '\nlen_topic: ', len(topic), '\n\n'))

    else:
        print("MACRO-TOPIC IDENTIFIED IN THE 2000-2018 TIMETABLE{0}".format('\n\n\n'))
        print("Number of macro-topics: {0}{1}".format(len(all_topics), '\n\n'))
        for topic in all_topics:
            print("{0}{1}{2}{3}".format(topic, '\nlen_topic: ', len(topic), '\n'))


    
