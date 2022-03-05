#!/bin/bash

echo "Checking whether system has required modules ..."
pip install -r requirements.txt

echo ""

echo "Please give path to the query file that contains queries in Qid<TAB>free-text format"
echo "INPUT NEEDED"
read query_file

echo "Please give path to english-corpora directory"
echo "INPUT NEEDED"
read test_corpora_dir

# uncomment these lines to eun pre processing again; takes about 20 mins
# echo "Pre processing corpus ..."
# python pre_procees.py $test_corpora_dir

echo "Running boolean ir system on corpora ..."
python boolean.py $query_file $test_corpora_dir

echo "Running tf_idf ir system on corpora ..."
python tf_idf.py $query_file $test_corpora_dir

echo "Running bm25 ir system on corpora ..."
python bm25.py $query_file $test_corpora_dir