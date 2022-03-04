"""
meta info:
    simplest boolean search query ir system using inverted index and postings lists
    connector between free-text is "and" <- modified boolean  
    @sunil-dhaka
"""
#===============================
# import every module from project imports that is used
from imports import *
from pre_process import *
#===============================
# to keep these words unchangable we use python set
# as our docs are in english we use english stopwords
Stopwords = set(stopwords.words('english'))
# create stemmer instance
porter=PorterStemmer()
#===============================
def boolean_system(query_file,test_corpora_dir,inverted_index_json_file='inverted-index-data.json',index_json_file='index-data.json',output_file_path='qrels-boolean.txt',top_k=5,pre_process=False)->None:
    # TODO: how to get scores for boolean ir system
    '''
    Input:
        query_file: file that contains query free texts\\
        test_corpora_dir: corpus directory\\
        inverted_index_json_file: inverted index data from pre-processing\\
        index_json_file: index data from pre-processing\\ 
        output_file_path: path where to store output qrels\\
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
    files_ids=[file.split('.')[0] for file in files]
    total_documents=len(files)

    rel_docs=[]
    for i,query_input in enumerate(query_inputs):
        """pre-process boolean search query"""
        tokenized_query=query_processor(query_input).split(' ')

        """create binary vector for terms"""
        query_word_zero_one=list()
        for word in tokenized_query:
            if word in inverted_index_data.keys():
                tmp_zero_one=[0]*total_documents
                present_doc_list=[doc_id for doc_id in inverted_index_data[word].keys()]
                for doc in present_doc_list:
                    tmp_zero_one[files_ids.index(doc)]=1 # used relation between doc_id and doc_id.txt
                query_word_zero_one.append(tmp_zero_one)
            else:
                # when word is not found means all doc entries are zeros
                # print(f'word > {word} < is not found in any document')
                query_word_zero_one.append([0]*total_documents) # add [0]*N list since word is in no document

        """create a merged boolean(zero-one) list using bitwise operations"""
        # try:
        for i in range(len(tokenized_query)-1):
            zero_one_list1=query_word_zero_one[0]
            zero_one_list2=query_word_zero_one[1]
            # implement and using '&'
            """simple bitwise operations to get intersections of term docs"""
            bitwise_logic=[l1 & l2 for (l1,l2) in zip(zero_one_list1,zero_one_list2)]
            query_word_zero_one.remove(zero_one_list1)
            query_word_zero_one.remove(zero_one_list2)
            query_word_zero_one.insert(0,bitwise_logic)
        
        doc_ids=[]
        is_relevent_list=[]
        
        for i,zero_one in enumerate(query_word_zero_one[0]):
            if zero_one==1:
                is_relevent_list.append(1)
                doc_ids.append(files_ids[i]) # recall indexed_files is a dict
        
        # handle the case when there are less relevent docs than required
        # sol: just append some random docs with relevancy being 0 after checking that it is not already in doc_ids
        total_rel_docs_retrived=len(doc_ids)
        if total_rel_docs_retrived<top_k:
            for j in range(top_k-total_rel_docs_retrived):

                while True:
                    random_irrelevant_doc=files_ids[np.random.randint(0,total_documents)]
                    if random_irrelevant_doc not in doc_ids:
                        doc_ids.append(random_irrelevant_doc)
                        is_relevent_list.append(0)
                        break

        rel_docs.append({'qid':'Q'+str(i+1).zfill(2),'doc_ids':doc_ids[:top_k],'relevant':is_relevent_list[:top_k]})
        # print(rel_docs)
    qrels_list=[]
    for i in range(total_queries):
        for j in range(top_k):
            if rel_docs[i]['relevant'][j]==1:
                qrels_list.append(f"Q{str(i+1).zfill(2)},1,{rel_docs[i]['doc_ids'][j]},1")
            else:
                qrels_list.append(f"Q{str(i+1).zfill(2)},1,{rel_docs[i]['doc_ids'][j]},0")
    with open(output_file_path,'w') as file:
        file.write('\n'.join(qrels_list))
#============================== 
if __name__=='__main__':
    if len(sys.argv)>2:
        query_input=sys.argv[1]
        data_dir_name=sys.argv[2]
    else:
        print('Input format: <query_inputs_file> <data_dir_name>')
        sys.exit()

    tic=time()
    boolean_system(query_input,data_dir_name)
    toc=time()
    print(f'Time taken {round(toc-tic)} secs.')
#==============================
"""
TODO[DONE]: for bi-word queries need to have inverted index of bi-words; that needs to be done in pre-processing step
    - one solution is to introduce 'and' between words that don't have connecting boolean words; this way we take intersection
    - if it is not done then system leaves some words and that is no good
"""