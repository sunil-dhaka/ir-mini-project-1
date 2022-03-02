"""
meta info:
    implementation of BM25 ir system
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
def bm25_system(query_input,test_corpora_dir,inverted_index_data,index_data,k1=1.5,b=0.75):
    
    '''
    Input:
        query free text\\
        corpus directory\\
        inverted index data from pre-processing\\
        index data from pre-processing\\
    Output:
        score dataframe with doc_id and scores
    '''

    files=os.listdir(test_corpora_dir)
    total_documents=len(files)

    """pre-process boolean search query"""
    tokenized_query=[porter.stem(word.lower()) for word in word_tokenize(query_input)]

    doc_lengths={}
    avdl=0
    # NOTE: this loop although not time consuming can be avoided with some extra memory being stored and that approach complicates things
    for doc in files:
        doc_id=doc.split('.')[0]
        tmp_dl=len(index_data[doc_id])
        avdl+=tmp_dl
        doc_lengths[doc_id]=tmp_dl
    
    avdl=avdl/total_documents

    doc_scores={}
    for doc in files:
        doc_id=doc.split('.')[0]
        doc_tf_idfs=[]
        term_tfs=[]
        
        for word in tokenized_query:
            # if word or doc_id in a wrod's postings list is not present then tf_idf is 0
            # so using try we handle that exception and append 0
            # this takes care of terms that are not present in a document or entire corpora
            try:
                tf_count=inverted_index_data[word][doc_id]
                idf_value=np.log(total_documents/len(inverted_index_data[word]))
                doc_tf_idfs.append(idf_value*tf_count)
                term_tfs.append(tf_count)
            except KeyError:
                doc_tf_idfs.append(0)
                term_tfs.append(0)

        """standard BM25 RSV formula is used with k1=1.5 and b=0.75 as default; can be changed"""
        doc_scores[doc]=sum([((k1+1)*i)/((k1*(1-b+(b*(doc_lengths[doc_id]/avdl))))+j) for i,j in zip(doc_tf_idfs,term_tfs)]) 

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
    relevent_files=bm25_system(query_input,data_dir_name,inverted_index_data,index_data)
    toc=time()
    print(f'Takes about {round(toc-tic)} seconds to get relevent files for query >> "{query_input}", if any are there.')
    if relevent_files.shape[0]==0:
        print(f'No files found for query >> "{query_input}"')
    else:
        print(relevent_files)
#===============================