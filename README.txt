--------------------------------------------------------------------------------------------
Plugins-
Software: No software needed. Just python3 is enough.

Environments: conda 4.10.3, python 3.8.5

Dependencies-
Python Libraries: pandas 1.1.3, numpy 1.19.2, nltk==3.5

"""please run these interminal IF your machine does not have needed nltk data"""
nltk.download('punkt')
nltk.download('stopwords')
--------------------------------------------------------------------------------------------
Things to note:
On TIME:
Pre-processing for whole corpus takes about 20 mins on my machine.

Time taken on 40 test-queries on different IR systems:
Boolean: 30-40 secs
TF-IDF: 2-5 secs 
BM25: 2-5 secs

On MEMORY:
Inverted index data(postings lists) size is 90MB. To save re-running time I have stored this in memory for re-use.
I have not included english-corpora files as sir said in class. Please give path to your data-directory where necessary.
--------------------------------------------------------------------------------------------
NOTE1: 
    I have implemented all ir systems assuming that query input file is a TAB seperated file as specified in Q5 of the Assignment. 
    format: Qid<TAB>free-text

    Exa:
        Q01    what is information retrieval
        Q02    battle between Rama and Ravana
        ...
NOTE2:
    All code files for ir systems and Makefile are in 17817735-ir-systems.zip
    Only README.txt file is not in zip. It contains how to run scripts and input-output structure of scripts. 
--------------------------------------------------------------------------------------------
How to run:
---------
For Que1:
To get pre processing done pre_process.py script needs path to the directory where english-corpora files are stored.
Exa:
    ```py
    >>> python pre_process.py Downloads/CS657A/asgn1/english-corpora/
    ```
Points:
    - it takes about 20 mins to run.
    - and to save time when evaluating next steps. I have stored inverted index data that this script generates.
---------
For Que2:

Part-a:
To get relevant documents from boolean ir system, it needs mainly 2 parameters. They are:
query-file-path in your system
english-corpora-dir-path in your system
Exa:
    ```py
    >>> python boolean.py Downloads/CS657A/asgn1/test-queries.txt Downloads/CS657A/asgn1/english-corpora/
    ```

Points:
    - for 40 queries takes about 30-40 secs on my machine. per query less than one sec.
    - IF you want to pre-process corpora again then only set pre_process variable to True
    - this script uses inverted index data obtained from Que1

Part-b:
To get relevant documents from tf-idf ir system, it needs mainly 2 parameters. They are:
query-file-path in your system
english-corpora-dir-path in your system
Exa:
    ```py
    >>> python tf_idf.py Downloads/CS657A/asgn1/test-queries.txt Downloads/CS657A/asgn1/english-corpora/
    ```

Points:
    - for 40 queries takes about 5 secs on my machine.
    - IF you want to pre-process corpora again then only set pre_process variable to True
    - this script uses inverted index data obtained from Que1

Part-c:
To get relevant documents from bm25 ir system, it needs mainly 2 parameters. They are:
query-file-path in your system
english-corpora-dir-path in your system
Exa:
    ```py
    >>> python bm25.py Downloads/CS657A/asgn1/test-queries.txt Downloads/CS657A/asgn1/english-corpora/
    ```

Points:
    - for 40 queries takes about 5 secs on my machine.
    - IF you want to pre-process corpora again then only set pre_process variable to True
    - this script uses inverted index data obtained from Que1
---------
For Que3:
queries.txt and qrels.txt files are given in 17817735-qrels.zip file, as asked.
---------
For Que4:
I have implemented map but sir said in class that we only need to output three output files(in qrels format specified in Q3) for different ir systems,
for your systems to automatically check and get scores.
To get different ir systems retrived documents in qrels, you need to run

    ```bash
    bash map.sh
    ```
this requires two inputs. They are
- query-file-path in your system
- english-corpora-dir-path in your system

NOTE-1: 
output file names are as follows, though they can be changed in individual scripts.
- for boolean: qrels-boolean.txt
- for tfidf: qrels-tfidf.txt
- for bm25: qrels-bm25.txt

NOTE-2:
IF you want to re-run pre-processing that can be done easily. Takes about 20 mins. Just uncomment these lines in map.sh
    ```bash
    echo "Pre processing corpus ..."
    python pre_procees.py $test_corpora_dir
    ```

To run for map score your script can take output files as input against ground truth files that your have.
Please keep in mind that queries file should as specified in Q5. and should not have empty lines in it without any query, otherwise my script might produce error.
---------
For Que5:
This is the README file.
And makefile for the project is also there. Please read comments in Makefile.
Also you can uncomment pre-processing lines to re-run Que1. Takes 20 mins.
IMP NOTE:
    You need to edit Makefile variable values to run on your system without error.
    How to edit:
    change QUERY and DIR variables.
    here QUERY is path to the query txt file on your system
    here DIR is path to english-corpora directory on your system 
--------------------------------------------------------------------------------------------
Input and Output structure of scripts:

Assignment Level(used in all other scripts):   
imports.py 
    Input: None
    Output: None
    
query_pre_processor.py  
query_processor() function ->
    Input: 
        query: query string from user
    Output: 
        processed_query: returns processed query string

Question-1   
pre_process.py
    Input: 
        test_corpora_dir: data-directory path that contains corpus that is to be processed
        store_processed: boolean input whether want to store processed corpora files or not; default is False 
    Output: 
        None

    This script files that are stored as output:
        inverted-index-data.json: contains inverted index data in JSON object
        index-data.json: certain useful data about each file(unique-word-count and document-length) that is 
                         used in tf_idf and bm25 systems to avoid time consuming runs. this is also in JSON object format


Question-2 IR systems
Part-a:
boolean.py
    Input:
        query_file: file that contains query free texts
        test_corpora_dir: corpus directory
        inverted_index_json_file: inverted index data from pre-processing; default to inverted-index-data.json
        index_json_file: index data from pre-processing ; default to index-data.json
        output_file_path: path where to store output qrels; default is qrels-boolean.txt
        top_k: to return top k relevent docs -- default is 5
        pre_process: if want to re-run pre-processing steps that creates inverted index -- default to False(for good) 
    Output:
        return: file is stored in qurels format

Part-b:
tf_idf.py
    Input:
        query_file: file that contains query free texts
        test_corpora_dir: corpus directory
        inverted_index_json_file: inverted index data from pre-processing; default to inverted-index-data.json
        index_json_file: index data from pre-processing; default to index-data.json
        output_file_path: path where to store output qrels; default is qrels-tfidf.txt
        top_k: to return top k relevent docs -- default is 5
        pre_process: if want to re-run pre-processing steps that creates inverted index -- default to False(for good) 
    Output:
        return: file is stored in qurels format

Part-c:
bm25.py
    Input:
        query_file: file that contains query free texts
        test_corpora_dir: corpus directory
        inverted_index_json_file: inverted index data from pre-processing; default to inverted-index-data.json
        index_json_file: index data from pre-processing; default to index-data.json
        output_file_path: path where to store output qrels; default is qrels-bm25.txt
        k1: model parameter set to 1.5(default)
        b: model parameter set to 0.75(default)
        top_k: to return top k relevent docs -- default is 5
        pre_process: if want to re-run pre-processing steps that creates inverted index -- default to False(for good) 
    Output:
        return: file is stored in qurels format

Question-4
map.sh
    Input:
        query_file: file that contains query free texts(from Q01 to Q40, for example)
        test_corpora_dir: english-corpora-directory-path
    Output:
        qrels-boolean.txt
        qrels-tfidf.txt
        qrels-bm25.txt

Question-5
Makefile
    NEEDS TO BE EDITED FILE PATHS BEFORE HAND. PLEASE READ Makefile COMMENTS.
    Input:
        query_file: file that contains query free texts(from Q01 to Q40, for example)
        test_corpora_dir: english-corpora-directory-path
    Output:
        Executes whole project
--------------------------------------------------------------------------------------------