"""
meta info:
    implementation of BM25 ir system
    @sunil-dhaka
"""
#===============================
# import every module from project imports that is used
from nbformat import write
from imports import *
from pre_process import *
#===============================
# to keep these words unchangable we use python set
# as our docs are in english we use english stopwords
Stopwords = set(stopwords.words('english'))
# create stemmer instance
porter=PorterStemmer()
#===============================
def bm25_system(query_file,test_corpora_dir,inverted_index_json_file='inverted-index-data.json',index_json_file='index-data.json',output_file_path='qrels-bm25.txt',k1=1.5,b=0.75,top_k=15,pre_process=False)->None:
    '''
    Input:
        query_file: file that contains query free texts\\
        test_corpora_dir: corpus directory\\
        inverted_index_json_file: inverted index data from pre-processing\\
        index_json_file: index data from pre-processing\\
        output_file_path: path where to store output qrels\\
        k1: model parameter set to 1.5\\
        b: model parameter set to 0.75\\
        top_k: to return top k relevent docs -- default is 5\\
        pre_process: if want to re-run pre-processing steps that creats inverted index -- default to False(for good) 
    Output:
        return: file is stored in qurels format
    '''
    # NOTE: if you have half hour then only set pre_process to True and pre_processor will update inverted_index_data
    # it is set to False by default for that only reason
    if pre_process:
        pre_processor(test_corpora_dir)
   
    with open(inverted_index_json_file,'r') as file:
        inverted_index_data=json.load(file)
    with open(index_json_file,'r') as file:
        index_data=json.load(file)

    # NOTE: here I have assumed that queries are in Qid<TAB>query-free-text format; meaning TAB seperated

    with open(query_file,'r') as file:
        query_lines=file.readlines()
        query_inputs=[query.split('    ')[1].strip() for query in query_lines]
    total_queries=len(query_inputs)
    

    files=os.listdir(test_corpora_dir)
    total_documents=len(files)

    doc_lengths={}
    avdl=0
    # NOTE: this loop although not time consuming can be avoided with some extra memory being stored and that approach complicates things
    for doc in files:
        doc_id=doc.split('.')[0]
        tmp_dl=index_data[doc_id]['dl']
        # print(tmp_dl)
        avdl+=tmp_dl
        doc_lengths[doc_id]=tmp_dl
    
    avdl=avdl/total_documents
    
    rel_docs=[]
    for i,query_input in enumerate(query_inputs):
        """pre-process boolean search query"""
        tokenized_query=query_processor(query_input).split(' ')
        # print(tokenized_query)

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
                    # natural version
                    tf_count=inverted_index_data[word][doc_id]
                    # natural log version
                    # tf_count=1+np.log(inverted_index_data[word][doc_id])
                    idf_value=np.log(total_documents/len(inverted_index_data[word]))
                    doc_tf_idfs.append(idf_value*tf_count)
                    term_tfs.append(tf_count)
                except KeyError:
                    doc_tf_idfs.append(0)
                    term_tfs.append(0)

            """standard BM25 RSV formula is used with k1=1.5 and b=0.75 as default; can be changed"""
            doc_scores[doc_id]=sum([((k1+1)*i)/((k1*(1-b+(b*(doc_lengths[doc_id]/avdl))))+j) for i,j in zip(doc_tf_idfs,term_tfs)]) 

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
    if len(sys.argv)>2:
        query_input=sys.argv[1]
        data_dir_name=sys.argv[2]
        # inverted_index_json_file=sys.argv[3]
        # index_json_file=sys.argv[4]
    else:
        print('Input format: <query_inputs_file> <data_dir_name>')
        sys.exit()
        
    tic=time()
    bm25_system(query_input,data_dir_name)
    toc=time()
    print(f'Time taken {round(toc-tic)} secs.')
#===============================