# MINING-EVOLVING-TOPICS

This is a Python repository about the Web And Social Information Extraction Project 2018/2019 in the Computer Science Master's Degree course of La Sapienza University of Rome.

## Goal Description ##

The goal is to identify and trace macro-topics along a predefined timeline that runs from 2000 to 2018. Each topic is a list or set of keywords that is taken from the ds-1 dataset. More precisely, each record of the ds-1 dataset contains:

* the year of the timeline.
* a pair of keywords that have been co-cited in the given year.
* a dictionary where each key is an author who co-cited those keywords and the number of co-citations as a value.

There is also an additional dataset, ds-2, which where each record contains:

* the year of the timeline
* a pair of authors who published in a given year and represents the co-authorship between two authors. 
* the number of collaborations between the two authors.

The ds-2 dataset was used as an additional dataset to resolve the problem, but the main dataset is the ds-1. To solve the problem and carry out an empirical study on it, the information extrapolated from the datasets were modeled as graphs. Graph-dependent metrics such as pagerank, betweenness centrality, degree centraility were used to identify the most representative keywords for k topics, spread of influence algorithms and graph algorithms were used to identify topic keywords. Finally, the proportion of common words between topics was used to trace and decide whether to merge two topics. 

More detailed information on the [report](./doc/report.pdf).


## Description and Requirements ##

Python 3 was used for the development of the entire project. The system was developed and tested using 32-bit Python 3.6 and 64-bit Python 3.7 on Linux systems. It has been developed and tested on Linux distros: Linux Mint and Ubuntu. The complete task is calculated by the main present in the src folder. To execute it, move with the terminal to the src folder and run the command:

```sh
python main.py -k k_val -ds1_path path -ds2_path path
```

`k_val` is in `[5, 10, 20, 100]`. Using the `-h` option, the possible uses of the main program are shown. For each part, there is a python script that tests only that part, an ipython-notebook that shows complete tests across the timeline. The notebook is also available in the html version. Using the `-h` option, all possible uses of python scripts to test various parts are shown.

Finally, there are log files that show some tests of each part and the tests carried out through the main.

Moreoever, to run the program, you need the following Python 3 libraries: 

* *pandas*
* *matplotlib*
* *networkx*
* *ndlib*
* *numpy*


## License ##

The license for this software is: GPLv3
