###############################################################################################################
#                                                                                                             #
#  FileName    [tracing_merge.py]                                                                             #
#                                                                                                             #
#  PackageName [tracing_merge]                                                                                #
#                                                                                                             #
#  Synopsis    [This file contains the class whose methods are used to trace the topics on the timeline,      #
#               trace the topics for each topic found in each. During the tracing it allows you to decide     #
#               whether to carry out a chain of consecutive years topics.]                                    #
#                                                                                                             #
#  Author      [Leonardo Picchiami]                                                                           #
#                                                                                                             #
###############################################################################################################



import networkx as nx

import gc


class TraceMergeTimeline(object):
    '''
    Class for tracing topics for each topic of each timeline year. 
    During the tracking it is possible to merge similar topics from consecutive years starting from the topic in question;
    the chain of similar topics is merged starting from the tracer topics (target topic). If the chain is interrupted then the following 
    traced topics are not taken into consideration for merging.


    Attributes
    ----------
    topics_dict : dict 
        Dictionary of topics identified along the timeline.

    threshold : float
        Threshold for similarity between topics.

    traced_topics : list (list of lists)
        List of topics traced starting from a given topic of a given year.

    macro_topics_timeline : list (list of lists)
        List of macro topics retrivied on the 2000 - 2018 timeline

    tracing_save_path : string
        Path to save topic tracing if this mode is chosen.
    '''

    
    def __init__(self, topics_dict, k = None, tracing_save_path = None):
        '''
        Parameters
        ----------
        topics_dict : dict
            Dictionary of topics identified along the timeline.  

        k : int, optional
            Integer value indicating the number of topics initially retrieved.

        tracing_save_path : string, optional
            Path to save topic tracing if this mode is chosen.

        '''
        
        self.__topics_dict = topics_dict
        self.__tracing_save_path = tracing_save_path
        self.__k = k
        self.__threshold = 0.5
        self.__traced_topics = []
        self.__macro_topics_timeline = []


    
    def keywords_fraction(self, topic1, topic2):
        '''
        Calculates the keywords fraction (the similarity) of topic1 that are in topic2.

        Parameters
        ----------
        topic1 : list
            Main topic on which the keywords fraction is calculated.

        topic2 : list
            Topic with respect to which the keywords fraction of the topic1 is calculated.
        '''
        
        count = 0
        for key in topic1:
            if key in topic2:
                count += 1
        return count / len(topic1)


    
    def threshold_similarity_two_topics(self, topic1, topic2):
        '''
        Calculate if there are either at least threshold keywords of topic1 in topic2 or vice versa.

        Parameters
        ----------
        topic1 : list
            Topic on which to calculate the similarity respect to topic2.

        topic2 : list
            Topic on which to calculate the similarity respect to topic1.
        '''
        
        sim_topic1 = self.keywords_fraction(topic1, topic2)
        sim_topic2 = self.keywords_fraction(topic2, topic1)

        if sim_topic1 >= self.__threshold or sim_topic2 >= self.__threshold:
            return True

        return False

    
        
    def similarity_two_topics(self, topic1, topic2,  year):
        '''
        Calculate the similarity between two topics: it is checked if one or the other has threshold keywords in common.

        Parameters
        ----------
        topic1 : list
            List of keywords (topic) on which the similarity is calculated.

        topic2 : list
            List of keywords (topic) on which the similarity is calculated.

        year : int 
            Year of traced topic.
        '''
        
        if self.threshold_similarity_two_topics(topic1, topic2):
            self.__traced_topics.append((year, topic2))
            return True

        else:
            return False

        

    def check_duplicate_topic(self, merge):
        '''
        Exhaustive control on the list of macro-topics identified along the timeline. Macro topics included in other macro-topics are deleted.
        
        Parameters
        ----------
        merge : bool
            boolean flag to set if, during the tracing operation the topics of consecutive years, 
            the chain of traced consecutive topics are merged.
        '''
        
        if merge:
            tmp_macro_topic = list(self.__macro_topics_timeline)
            for topic1 in tmp_macro_topic:
                for topic2 in tmp_macro_topic:
                    if topic1 == topic2:
                        continue
                    topic1_set = set(topic1)
                    topic2_set = set(topic2)
                    if (len(topic1_set - topic2_set) == 0) or (len(topic2_set - topic1_set) == 0):
                        if len(topic1_set) < len(topic2_set):
                            if topic1 in self.__macro_topics_timeline and topic2 in self.__macro_topics_timeline: 
                                self.__macro_topics_timeline.remove(topic1)
                            else:
                                if topic2 in self.__macro_topics_timeline and topic1 in self.__macro_topics_timeline:
                                    self.__macro_topics_timeline.remove(topic2)


                                    
    def print_trace(self, topic_target, year, merge):
        '''
        Prints the tracing.

        If merge flag is True, the method merges the similar traced topics in consecutive years starting from the topic_target.

        Parameters
        ----------
        topic_target : list
            Main topic by which other topics from subsequent years are traced. (and/or merged)

        year : int
            Year of the timeline related to the target topic.

        merge : bool
            boolean flag to set if, during the tracing operation the topics of consecutive years, 
            the chain of traced consecutive topics are merged.
        '''
        
        print("The target topic: {0}{1}{2}{3}{4}".format('\n\nyear: ', year, '\n', topic_target, '\n\n'))

        #Case where no topic has been tracked
        if len(self.__traced_topics) == 0:
            self.__macro_topics_timeline.append(topic_target)         
            print("This topic have not traced any topics.\n\n")
            print("********************* END THIS TOPIC TRACING ***************************************\n\n\n")
            return

        
        #Case where topics has been tracked
        print("The traced topics are:\n\n")
        
        topic_set = set(topic_target)
        year_topic_target = year + 1
        for traced in self.__traced_topics:
            print("year : {0}  \n{1}{2}".format(traced[0], traced[1], '\n\n'))
            if merge:
                if year_topic_target == traced[0]:
                    topic_set = topic_set | set(traced[1])
                    year_topic_target += 1
                    
        print("********************* END THIS TOPIC TRACING ***************************************\n\n\n")

        self.__macro_topics_timeline.append(list(topic_set))


        
    def write_trace(self, topic_target, year, merge):
        '''
        Writes on file tracing.

        If merge flag is True, it merges the similar topics in consecutive years starting from the topic_target.
        
        Parameters
        ----------
        topic_target : list
            Main topic by which other topics from subsequent years are traced. (and/or merged)

        year : int
            Year of the timeline related to the target topic.

        merge : bool
            boolean flag to set if, during the tracing operation the topics of consecutive years, 
            similar traced topics are merged.
        '''
        
        if self.__tracing_save_path[-1] != '/':
           self.__tracing_save_path += '/'
           
        filename = self.__tracing_save_path + "tracing_k{0}_t{1}.log".format(self.__k, self.__threshold)
        f = open(filename, "a")
        f.write("The target topic: {0}{1}{2}{3}{4}".format('\n\nyear: ', year, '\n', topic_target, '\n\n'))

        #Case where no topic has been tracked
        if len(self.__traced_topics) == 0:
            self.__macro_topics_timeline.append(topic_target)         
            f.write("This topic have not traced any topics.\n\n")
            f.write("********************* END THIS TOPIC TRACING ***************************************\n\n\n")
            return

        #Case where topics has been tracked
        f.write("The traced topics are:\n\n")
        
        topic_set = set(topic_target)
        year_topic_target = year + 1
        for traced in self.__traced_topics:
            f.write("year : {0}  \n{1}{2}".format(traced[0], traced[1], '\n\n'))
            if merge:
                if year_topic_target == traced[0]:
                    topic_set = topic_set | set(traced[1])
                    year_topic_target += 1
                    
        f.write("********************* END THIS TOPIC TRACING ***************************************\n\n\n")

        self.__macro_topics_timeline.append(list(topic_set))
        f.close()

        
            
    def no_output(self, topic_target, year):
        '''
        Not prints or writes tracing. 

        Merges the similar topics in consecutive years starting from the topic_target.

        Parameters
        ----------
        topic_target : list
            Main topic by which other topics from subsequent years are traced. (and/or merged)

        year : int
            Year of the timeline related to the target topic.
        '''
        
        #Case where no topic has been tracked
        
        if len(self.__traced_topics) == 0:
            self.__macro_topics_timeline.append(topic_target)
            return
        
        topic_set = set(topic_target)
        year_topic_target = year + 1
        for traced in self.__traced_topics:
            if year_topic_target == traced[0]:
                topic_set = topic_set | set(traced[1])
                year_topic_target += 1
      
        self.__macro_topics_timeline.append(list(topic_set))
        
        
        
    def result_handling(self, topic_target, year, merge, mode):
        '''
        Output management method:
            - Printing of the tracing on the timeline (with or without merging)
            - Writing tracking on a file on the timeline (with or without merging)
            - Print or write the tracing. Merging is mandatory.
        
        Parameters
        ----------
        topic_target : list
            Main topic by which other topics from subsequent years are traced. (and/or merged)

        year : int
            Year of the timeline related to the topic_target.

        merge : bool
            boolean flag to set if, during the tracing operation the topics of consecutive years, 
            similar traced topics are merged.
        
        mode : int
            Mode value to handle the tracking output.
                - 0 Print tracing of topics
                - 1 Write on file tracing of topics 
                - 2 Not print and not write tracing of topics
        '''

        if mode == 0:
            self.print_trace(topic_target, year, merge)

        if mode == 1:
            self.write_trace(topic_target, year, merge)
        
        if mode == 2:
            self.no_output(topic_target, year)
   
        

    def study_behaviour_different_years(self, topic_target, year, merge, mode):
        '''
        For each topic of each year, topics are traced in the years following the year of the tracer topic 
        and the behavior of the tracing is studied to merge those of consecutive years.

        Parameters
        ----------
        topic_target : list
            Main topic by which other topics from subsequent years are traced. (and/or merged)

        year : int
            Year of the timeline related to the topic_target.

        merge : bool
            boolean flag to set if, during the tracing operation the topics of consecutive years, 
            similar traced topics are merged.
        
        mode : int
            Mode value to handle the tracking output.
                - 0 Print tracing of topics
                - 1 Write on file tracing of topics 
                - 2 Not print and not write tracing of topics
        '''
        
        self.__traced_topics = []
        for i in range(year + 1, 2019):
            for other_year_topic in self.__topics_dict[str(i)]:
                result = self.similarity_two_topics(topic_target, other_year_topic, i)
                if result:
                    break
                

        self.result_handling(topic_target, year, merge, mode)        
        

            
    def trace_timeline(self, mode, merge = False):
        '''
        Track the topics along the timeline. If the merge flag is set, it studies the behavior of the topics 
        and merges all the similar topics in consecutive years where the first topic of the chain is the tracer topic.
        (target topic)

        Parameters
        ----------
        merge : bool, optional
            boolean flag to set if, during the tracing operation the topics of consecutive years, 
            the chain of traced consecutive topics are merged.

        mode : int
            Mode value to handle the tracking output.
                - 0 Print tracing of topics
                - 1 Write on file tracing of topics 
                - 2 Not print and not write tracing of topics
        '''

        
        assert mode >= 0 and mode <= 2, "Valid values for mode are 0, 1 or 2."
        
        for i in range(2000, 2018):
            for topic in self.__topics_dict[str(i)]:
                self.study_behaviour_different_years(topic, i, merge, mode)

        if merge:
            for topic in self.__topics_dict["2018"]:
                self.__macro_topics_timeline.append(topic)

            self.check_duplicate_topic(merge)
            
            

    def get_topics_timeline(self):
        '''
        Returns all the macro topics on the timeline.

        Returns
        -------
        macro_topics_timeline : list
            List containing all the macro topics traced on the timeline.
        '''
        
        return self.__macro_topics_timeline
                
            
