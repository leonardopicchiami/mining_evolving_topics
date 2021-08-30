# MINING-EVOLVING-TOPICS

This is a Python repository about the Web And Social Information Extraction Project 2018/2019 in the Computer Science Master's Degree course of La Sapienza University of Rome.

## Goal Description ##

The goal is to identify and trace macro-topics along a predefined timeline that runs from 2000 to 2018. Each topic is a list or set of keywords that are taken from the ds-1 dataset. Each record of the ds-1 dataset contains:

* the year (between 2000 and 2018).
* a pair of keywords that have been co-cited in the given year.
* a dictionary where each key is an author who co-cited the given keywords and, the value is the number of co-citations.

The specifications also provide an additional dataset, ds-2, where each record contains:

* the year of the timeline
* a pair of authors who published in a given year and represents the co-authorship between two authors. 
* the number of collaborations between the two authors.

The ds-2 dataset was used to exstract additional informations to solve the problem, but the main dataset is the ds-1. 

We performed an empirical study on information provided by the two datasets. Firstly, we modelled records of each year from ds-1 as a graph. Secondly, through graph-dependent metrics such as PageRank, betweenness centrality, degree centrality, we identified the most representative keywords for k topics. Thirdly, we used the spread of influence methods and graph algorithms to identify all keywords for each topic. Finally, we exploited the ratio of common words between two topics to trace and decide whether to merge the two topics.

The complete specifications are [here](./doc/.project_specifications.pdf).

More detailed information is in the [report](./doc/report.pdf).


## Description and Requirements ##

We used Python 3 to develop the whole project. In particular, we developed it through 32-bit Python 3.6 and 64-bit Python 3.7 on Linux systems: Linux Mint and Ubuntu. We carried out all experiments using both python versions on both Linux Systems. 

The script named main, sited in the src folder, runs the complete task. To execute it, move with the terminal to the src folder and run the command:

```sh
python -k k_val -ds1_path path -ds2_path path
```

`k_val` is in `[5, 10, 20, 100]`. Using the `-h` option, the script shows all possible uses of the software. For each sub-task, we provided a python script that executes the experimental study up to that point. Again, using the `-h` option, every script shows all possible uses to test such sub-task. 

Along with each script, there is an ipython-notebook that shows the experiments up to that point. Every notebook is also available in the Html version. 

In addition, we developed an ipython-notebook that shows complete tests across the timeline. 

Finally, there are log files that show some tests of each part and the tests carried out through the main.

### Requirements 

To run the program, you need the following Python 3 libraries: 

* *pandas*
* *matplotlib*
* *networkx*
* *ndlib*
* *numpy*


## License ##

The license for this software is: GPLv3
