"""
meta info:
    script to pre-process text corpora data files
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
# helper funtion
def get_unique_word_freq(word_list):
    '''
    takes word list and returns unique-words with their freq in dict
    '''
    unqiue_words=list()
    words_freq={}
    # store unqiue words in list
    for word in word_list:
        if word not in unqiue_words:
            unqiue_words.append(word)
    # get unique words freq from all words list using count
    for unqiue_word in unqiue_words:
        # NOTE: this same method can be used to get freq of a particular word in given document
        words_freq[unqiue_word]=word_list.count(unqiue_word) # used count method of lists
    
    return words_freq
#===============================
# helper funtion
def create_folder(folder_name):
    '''
    create folder with name given
    '''
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        pass
#===============================
def pre_processor(test_corpora_dir,store_processed=False):
    '''
    Input:
        test_corpora_dir: dir path that stores corpora files
        store_processed: bool to indicate whether to store files or not; default is false
    Output:
        inverted-index-data.txt: stores postings lists in dict format
        index-data.txt: stores document unique word count and document length
    '''
    
    """init variables that are used"""
    # indexed_files={} # to store doc_id and their file_names
    inverted_index_dict={} # rather than using linked list we use easy to understand dicts
    """
    to use in pivot length normalization we store # of unique terms in a doc
    doc lengths are stored for use in BM25
    that is why we store this index data
    """
    unique_words_in_doc={}

    folder_name='processed-corpora'
    if store_processed:
        create_folder(folder_name)

    """main processing with sub steps explained"""
    
    for i,file in enumerate(os.listdir(test_corpora_dir)):

        doc_id=file.split('.')[0]
        # indexed_files[doc_id]=file

        with open(test_corpora_dir+'/'+file,'r') as f:
            corpora_file_str=f.read() # text str

        """remove css code lines"""
        css_regex=re.compile(r'.mw.*}')
        # substitue regex expression by ''
        corpora_file_str=css_regex.sub('',corpora_file_str)

        """remove html tag lines"""
        html_regex=re.compile(r'<.*>')
        # substitue regex expression by ''
        corpora_file_str=html_regex.sub('',corpora_file_str)

        """remove special characters and only keep a-z;A-Z;0-9;space"""
        '''
        to avoid deprecation warning used one more backslash to escape backslash
        so \s -> \\s
        '''
        special_regex=re.compile('[^a-zA-Z0-9\\s]')
        # substitue regex expression by ''
        corpora_file_str=special_regex.sub('',corpora_file_str)

        """remove digits for file"""
        digit_regex=re.compile('\d')
        # substitue regex expression by ''
        corpora_file_str=digit_regex.sub('',corpora_file_str)

        sentence_tokens=sent_tokenize(corpora_file_str)
        # print(len(sentence_tokens))
        word_tokens=word_tokenize(corpora_file_str)
        # print(len(word_tokens))

        """avoid single characters and lower them and remove stopwords"""
        # TODO: what about special cases like UP > up or PIN > pin 
        # TODO: incase of tf-idf stopwords do not matter. 
        # for this should keep them? for cases "like to be or not to be"
        word_tokens=[porter.stem(word.lower()) for word in word_tokens if len(word)>1] # and word not in Stopwords]
        # print(len(word_tokens))

        tmp_word_freq_of_doc=get_unique_word_freq(word_tokens)
        unique_words_in_doc[doc_id]={
            'unique_terms_count':len(tmp_word_freq_of_doc),
            'dl':sum(tmp_word_freq_of_doc.values())
        }

        for word in tmp_word_freq_of_doc.keys():
            does_word_exists=inverted_index_dict.get(word,None)
            if does_word_exists is not None:
                # if ele is already there then just update dictinory
                inverted_index_dict[word][doc_id]=tmp_word_freq_of_doc[word]
            else:
                # here first we create a new element in parent dict
                inverted_index_dict[word]={}
                inverted_index_dict[word][doc_id]=tmp_word_freq_of_doc[word]

        # store processed text data into files only is explicitly mentioned
        if store_processed:
            with open(f'{folder_name}/{file}','w') as processed_file:
                processed_file.write(' '.join(word_tokens))
    
    """store processed data that is used in ir systems"""
    with open('inverted-index-data.json','w') as file:
        json.dump(inverted_index_dict,file)

    with open('index-data.json','w') as file:
        json.dump(unique_words_in_doc,file)
#===============================
if __name__=='__main__':
    if len(sys.argv)>1:
        data_dir_name=sys.argv[1]
    else:
        print('To process particular corpora files; please give path to the directory that contains files as argument to "sys.argv".')
        print('To process default directory enter y or yes. Else quits.')
        default_=input('> ')
        if default_.lower().startswith('y'):
            print('Processing files from default directory.')
            data_dir_name='test-corpora'
        else:
            print('Exiting')
            sys.exit()
    tic=time()
    pre_processor(data_dir_name)
    toc=time()
    print(f'takes about {round(toc-tic)} seconds to pre-process {len(os.listdir(data_dir_name))} files.')


'''
TODO: there are some urls in some files that are not into html tags; how to remove them 
TODO: to improve results can implement multiple zone tags version of inverted index; needs weights for zones: might learn or fix with domain knowledge or intuitions
TODO: can be improved using lemmatization or different algorithm for stemming itself
'''