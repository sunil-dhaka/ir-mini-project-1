run:
	@echo "Please give path to the query file that contains queries in Qid<TAB>free-text format"
	@echo "INPUT NEEDED"
	@read -p "query-txt-file? : " QUERY
	@echo "Please give path to english-corpora directory"
	@echo "INPUT NEEDED"
	@read -p "english-corpora-dir-path? : " DIR
	pip install -r requirements.txt
	@echo "Running boolean ..."
	python boolean.py $(QUERY) $(DIR)
	@echo "Running tfidf ..."
	python tf_idf.py $(QUERY) $(DIR)
	@echo "Running bm25 ..."
	python bm25.py $(QUERY) $(DIR)
clean:
	rm -rf __pycache__/
