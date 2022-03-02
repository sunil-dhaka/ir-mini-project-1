"""
meta info:
    simplest boolean search query ir system using inverted index and postings lists
"""
#===============================
# import every module from project imports that is used
from imports import *
#===============================
# to keep these words unchangable we use python set
# as our docs are in english we use english stopwords
Stopwords = set(stopwords.words('english'))
# create stemmer instance
porter=PorterStemmer()
#===============================
def tf_idf_system(query_input,test_corpora_dir,inverted_index_data,index_data,top_k=10):
    # TODO: which scores system to use for ranking in tf-idf ir system
    '''
    Input:
        boolean query to search\\
        corpus directory\\
        inverted index data from pre-processin\\
    Output:
        score dataframe with doc_id and scores
    '''

    files=os.listdir(test_corpora_dir)
    total_documents=len(files)

    """pre-process boolean search query"""
    tokenized_query=[porter.stem(word.lower()) for word in word_tokenize(query_input)]

    doc_scores={}
    for doc in files:
        doc_id=doc.split('.')[0]
        doc_tf_idfs=[]
        doc_index_data=index_data[doc_id]
        for word in tokenized_query:
            # if word or doc_id in a wrod's postings list is not present then tf_idf is 0
            # so using try we handle that exception and append 0
            try:
                tf_count=inverted_index_data[word][doc_id]
                idf_value=np.log(total_documents/len(inverted_index_data[word]))
                doc_tf_idfs.append(idf_value*tf_count)
            except KeyError:
                doc_tf_idfs.append(0)

        """using pivot length normalization that means we normalize document by # of unique words in it"""
        doc_scores[doc]=sum(doc_tf_idfs)/len(doc_index_data)

        """using tf-idf weights to normalize"""
        # TODO

    score_df=pd.DataFrame({'doc_id':doc_scores.keys(),'scores':doc_scores.values()})
    score_df.sort_values(by=['scores'],inplace=True,ascending=False)
    score_df.reset_index(inplace=True,drop=True)

    return score_df

#===============================
if __name__=='__main__':
    if len(sys.argv)>4:
        data_dir_name=sys.argv[1]
        inverted_index_json_file=sys.argv[2]
        index_json_file=sys.argv[3]
        query_input=' '.join(sys.argv[4:])
    else:
        print('Input format: <data_dir_name> <inverted_index_json_file> <index_json_file> <query_input>')
        sys.exit()

    with open(inverted_index_json_file,'r') as file:
        inverted_index_data=json.load(file)
    with open(index_json_file,'r') as file:
        index_data=json.load(file)
        
    tic=time()
    relevent_files=tf_idf_system(query_input,data_dir_name,inverted_index_data,index_data)
    toc=time()
    print(f'Takes about {round(toc-tic)} seconds to get relevent files for query >> "{query_input}", if any are there.')
    if relevent_files.shape[0]==0:
        print(f'No files found for query >> "{query_input}"')
    else:
        print(relevent_files)
#===============================