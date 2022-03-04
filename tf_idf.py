"""
meta info:
    search query ir system with tf_idf and cosine similarity ranking
    @sunil-dhaka
"""
#===============================
# import every module from project imports that is used
from imports import *
from pre_process import pre_processor
#===============================
# to keep these words unchangable we use python set
# as our docs are in english we use english stopwords
Stopwords = set(stopwords.words('english'))
# create stemmer instance
porter=PorterStemmer()
#===============================
def tf_idf_system(query_file,test_corpora_dir,inverted_index_data,index_data,output_file_path='qrels-tfidf.txt',top_k=5,pre_process=False):
    # TODO: which scores system to use for ranking in tf-idf ir system
    '''
    Input:
        query_file: file that contains query free texts\\
        test_corpora_dir: corpus directory\\
        inverted_index_data: inverted index data from pre-processing\\
        index_data: index data from pre-processing\\
        output_file_path: path where to store output qrels\\
        top_k: to return top k relevent docs -- default is 5\\
        pre_process: if want to re-run pre-processing steps that creats inverted index -- default to False(for good) 
    Output:
        return: file is stored in qurels format
    '''

    # NOTE: here I have assumed that queries are in Qid<TAB>query-free-text format; meaning TAB seperated

    with open(query_file,'r') as file:
        query_lines=file.readlines()
        query_inputs=[query.split('    ')[1].strip() for query in query_lines]
    total_queries=len(query_inputs)

    # NOTE: if you have half hour then only set pre_process to True and pre_processor will update inverted_index_data
    # it is set to False by default for that only reason
    if pre_process:
        pre_processor(test_corpora_dir)

    files=os.listdir(test_corpora_dir)
    total_documents=len(files)
    rel_docs=[]
    for i,query_input in enumerate(query_inputs):
        """pre-process boolean search query"""
        tokenized_query=query_processor(query_input).split(' ')

        doc_scores={}
        for doc in files:
            doc_id=doc.split('.')[0]
            doc_tf_idfs=[]
            unique_terms_count=index_data[doc_id]['unique_terms_count']
            for word in tokenized_query:
                # if word or doc_id in a wrod's postings list is not present then tf_idf is 0
                # so using try we handle that exception and append 0
                try:
                    # natural version
                    tf_count=inverted_index_data[word][doc_id]
                    # natural log version
                    # tf_count=1+np.log(inverted_index_data[word][doc_id])
                    idf_value=np.log(total_documents/len(inverted_index_data[word]))
                    doc_tf_idfs.append(idf_value*tf_count)
                except KeyError:
                    doc_tf_idfs.append(0)

            """using pivot length normalization that means we normalize document by # of unique words in it"""
            doc_scores[doc_id]=sum(doc_tf_idfs)/unique_terms_count

        score_df=pd.DataFrame({'doc_id':doc_scores.keys(),'scores':doc_scores.values()})
        score_df.sort_values(by=['scores'],inplace=True,ascending=False)
        score_df.reset_index(inplace=True,drop=True)
        doc_ids=score_df.iloc[:top_k,:]['doc_id'].values
        scores=score_df.iloc[:top_k,:]['scores'].values
        rel_docs.append({'qid':'Q'+str(i+1).zfill(2),'doc_ids':doc_ids,'scores':scores})


    qrels_list=[]
    for i in range(total_queries):
        for j in range(top_k):
            if rel_docs[i]['scores'][j]>0:
                qrels_list.append(f"Q{str(i+1).zfill(2)},1,{rel_docs[i]['doc_ids'][j]},1")
            else:
                qrels_list.append(f"Q{str(i+1).zfill(2)},1,{rel_docs[i]['doc_ids'][j]},0")
    with open(output_file_path,'w') as file:
        file.write('\n'.join(qrels_list))

#===============================
if __name__=='__main__':
    if len(sys.argv)>4:
        query_input=sys.argv[1]
        data_dir_name=sys.argv[2]
        inverted_index_json_file=sys.argv[3]
        index_json_file=sys.argv[4]
    else:
        print('Input format: <query_inputs_file> <data_dir_name> <inverted_index_json_file> <index_json_file>')
        sys.exit()

    with open(inverted_index_json_file,'r') as file:
        inverted_index_data=json.load(file)
    with open(index_json_file,'r') as file:
        index_data=json.load(file)
        
    tic=time()
    relevent_files=tf_idf_system(query_input,data_dir_name,inverted_index_data,index_data)
    toc=time()
    print(f'Time taken {round(toc-tic)} secs.')
#===============================