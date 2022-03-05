#QUERY: test-queries.txt is the queries file on my system
#DIR: english-corpora/ is the corpus files dir on my system
#change them appropriatly below
#also uncomment pre-processing lines to re-do pre-processing; takes about 20 mins
QUERY := test-queries.txt
DIR := english-corpora/
run:
	pip install -r requirements.txt
#	@echo "Pre processing corpora files ..."
#	python pre_process.py $(DIR)
	@echo "Running boolean ..."
	python boolean.py $(QUERY) $(DIR)
	@echo "Running tfidf ..."
	python tf_idf.py $(QUERY) $(DIR)
	@echo "Running bm25 ..."
	python bm25.py $(QUERY) $(DIR)
clean:
	rm -rf __pycache__
