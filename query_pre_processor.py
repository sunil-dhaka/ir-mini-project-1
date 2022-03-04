"""
meta info:
    to process query input for  
    @sunil-dhaka
"""
#===============================
# import every module from project imports that is used
from imports import *
#===============================
def query_processor(query):
    # to keep these words unchangable we use python set
    # as our docs are in english we use english stopwords
    Stopwords = set(stopwords.words('english'))
    # create stemmer instance
    porter=PorterStemmer()
    
    """remove css code lines"""
    css_regex=re.compile(r'.mw.*}')
    # substitue regex expression by ''
    query=css_regex.sub('',query)

    """remove html tag lines"""
    html_regex=re.compile(r'<.*>')
    # substitue regex expression by ''
    query=html_regex.sub('',query)

    """remove special characters and only keep a-z;A-Z;0-9;space"""
    '''
    to avoid deprecation warning used one more backslash to escape backslash
    so \s -> \\s
    '''
    special_regex=re.compile('[^a-zA-Z0-9\\s]')
    # substitue regex expression by ''
    query=special_regex.sub('',query)

    """remove digits for file"""
    digit_regex=re.compile('\d')
    # substitue regex expression by ''
    query=digit_regex.sub('',query)

    word_tokens=word_tokenize(query)
    # print(len(word_tokens))

    """avoid single characters and lower them and remove stopwords"""
    # for this should keep them? for cases "like to be or not to be"
    word_tokens=[porter.stem(word.lower()) for word in word_tokens if len(word)>1] #and word not in Stopwords]
    # print(len(word_tokens))

    processed_query=' '.join(word_tokens)
    return processed_query
