"""
seperate script to import modlues that are needed in other scripts of project
can add additional module here also to make it available project wide
"""
# import modules
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize , word_tokenize
import re
import os
import sys
import json
from time import time
import numpy as np
import pandas as pd
from query_pre_processor import query_processor