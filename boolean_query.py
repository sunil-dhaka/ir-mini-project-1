"""
meta info:
    simplest boolean search query ir system using inverted index and postings lists
    @sunil-dhaka
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
def boolean_query_system(query_input,test_corpora_dir,inverted_index_data,top_k=10):
    # TODO: how to get scores for boolean ir system
    '''
    Input:
        boolean query to search\\
        corpus directory\\
        inverted index data from pre-processin\\
        top k many scored files to be retunred
    Output:
        top k many scored file's names are retunred
    '''

    files=os.listdir(test_corpora_dir)
    total_documents=len(files)

    """pre-process boolean search query"""
    tokenized_query=[porter.stem(word.lower()) for word in word_tokenize(query_input)]

    """seperate logic and search terms"""
    bool_words=list()
    search_words=list()

    """IMPORTANT STEP"""
    for i,word in enumerate(tokenized_query):
        if word != "and" and word != "or":
            # to solve the problem of "not"
            if word == 'not':
                search_words.append(f'not-{tokenized_query[i+1]}')
            else:
                if tokenized_query[i-1]!='not':
                    search_words.append(word)
                # add 'and' in between words that does not have connectorr
                if i!=len(tokenized_query)-1 and tokenized_query[i+1] != 'and' and tokenized_query[i+1]!='or':
                    bool_words.append('and')
        else:   
            bool_words.append(word)
    
    """create binary vector for terms"""
    query_word_zero_one=list()
    for word in search_words:
        if 'not-' in word:
            if word.split('-')[1] in inverted_index_data.keys():
                tmp_zero_one=[1]*total_documents
                present_doc_list=[doc_id+'.txt' for doc_id in inverted_index_data[word.split('-')[1]].keys()]
                for doc in present_doc_list:
                    tmp_zero_one[files.index(doc)]=0
                query_word_zero_one.append(tmp_zero_one)
            else:
                print(f'word > {word.split("-")[1]} < is not found in any document')
                query_word_zero_one.append([0]*total_documents) # add [0]*N list since word is in no document
        else:
            if word in inverted_index_data.keys():
                tmp_zero_one=[0]*total_documents
                present_doc_list=[doc_id+'.txt' for doc_id in inverted_index_data[word].keys()]
                for doc in present_doc_list:
                    tmp_zero_one[files.index(doc)]=1
                query_word_zero_one.append(tmp_zero_one)
            else:
                print(f'word > {word} < is not found in any document')
                query_word_zero_one.append([0]*total_documents) # add [0]*N list since word is in no document

    """create a merged boolean(zero-one) list using bitwise operations"""
    # try:
    for word in bool_words:
        zero_one_list1=query_word_zero_one[0]
        zero_one_list2=query_word_zero_one[1]
        # implement and using '&'
        """simple bitwise operations to get intersections of term docs"""
        if word == 'and':
            bitwise_logic=[l1 & l2 for (l1,l2) in zip(zero_one_list1,zero_one_list2)]
            query_word_zero_one.remove(zero_one_list1)
            query_word_zero_one.remove(zero_one_list2)
            query_word_zero_one.insert(0,bitwise_logic)
        # implement or using '|'
        # simple bitwise operations to get union of term docs
        else:
            bitwise_logic=[l1 | l2 for (l1,l2) in zip(zero_one_list1,zero_one_list2)]
            query_word_zero_one.remove(zero_one_list1)
            query_word_zero_one.remove(zero_one_list2)
            query_word_zero_one.insert(0,bitwise_logic)
    # except IndexError:
        # print()
            
    query_files_result=list()
    try:
        for i,zero_one in enumerate(query_word_zero_one[0]):
            if zero_one==1:
                query_files_result.append(files[i]) # recall indexed_files is a dict
        return query_files_result[:top_k]
    except IndexError:
        return None
#============================== 
if __name__=='__main__':
    if len(sys.argv)>3:
        data_dir_name=sys.argv[1]
        inverted_index_json_file=sys.argv[2]
        query_input=' '.join(sys.argv[3:])
    else:
        print('Input format: <data_dir_name> <inverted_index_json_file> <query_input>')
        sys.exit()

    with open(inverted_index_json_file,'r') as file:
        inverted_index_data=json.load(file)
        
    tic=time()
    relevent_files=boolean_query_system(query_input,data_dir_name,inverted_index_data)
    toc=time()
    if relevent_files is None or len(relevent_files)==0:
        print(f'No files found for query >> "{query_input}"')
    else:
        print(f'Takes about {round(toc-tic)} seconds to get relevent files for query >> "{query_input}"')
        print('Some files that are relevent:')
        for file in relevent_files:
            print(file)
#==============================
"""
TODO[DONE]: for bi-word queries need to have inverted index of bi-words; that needs to be done in pre-processing step
    - one solution is to introduce 'and' between words that don't have connecting boolean words; this way we take intersection
    - if it is not done then system leaves some words and that is no good
"""