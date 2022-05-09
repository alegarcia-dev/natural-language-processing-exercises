'''

    prepare.py

    Description: This file contains functions used for preparing text
        data for the natural language processing exercises.

    Variables:

        None

    Functions:

        basic_clean(text)
        tokenize(text)
        stem(text)
        lemmatize(text)
        remove_stopwords(text, extra_words = None, exclude_words = None)

'''

################################################################################

import re
import unicodedata

import pandas as pd

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

################################################################################

def basic_clean(text: str) -> str:
    '''
        Perform basic cleaning operations on the text provided. This function 
        will convert all alphabetic characters to lowercase, remove non-ascii 
        characters, and remove all special characters except apostrophes.
    
        Parameters
        ----------
        text: str
            The text data that will be cleaned.
    
        Returns
        -------
        str: The cleaned text containing only lowercase alphabetic characters, 
            numbers, apostrophes, and whitespace.
    '''

    text = text.lower()

    # Remove non-ascii characters.
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # Match and replace anything that is not a letter, number, apostrophe, or whitespace.
    regexp = r"[^a-z0-9'\s]"
    text = re.sub(regexp, '', text)

    return text

################################################################################

def tokenize(text: str) -> str:
    '''
        Use NLTK ToktokTokenizer to tokenize the input text.
    
        Parameters
        ----------
        text: str
            The text data that will be tokenized.
    
        Returns
        -------
        str: The tokenized text data.
    '''

    tokenizer = ToktokTokenizer()
    return tokenizer.tokenize(text, return_str = True)

################################################################################

def stem(text: str) -> str:
    '''
        Using an NLTK PorterStemmer object apply stemming to the input and 
        return a text string of all the stems.
    
        Parameters
        ----------
        text: str
            The text data that will be stemmed.
    
        Returns
        -------
        str: A text string containing the stems of the original text.
    '''

    ps = nltk.porter.PorterStemmer()

    # For each word in text get the stem and return the stems joined in a string.
    stems = [ps.stem(word) for word in text.split()]
    return ' '.join(stems)

################################################################################

def lemmatize(text: str) -> str:
    '''
        Using an NLTK WordNetLemmatizer object apply lemmatization to the 
        input text and return a text string of all the lemmas.
    
        Parameters
        ----------
        text: str
            The text data that will be lemmatized.
    
        Returns
        -------
        str: A text string containing the lemmas of the original text.
    '''
    
    wnl = nltk.stem.WordNetLemmatizer()

    # For each word in text get the lemma and return the lemmas joined in a string.
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    return ' '.join(lemmas)

################################################################################

def remove_stopwords(text: str, extra_words: list[str] = None, exclude_words: list[str] = None) -> str:
    '''
        Remove all stopwords from the input text. The list of stopwords provided 
        by nltk.corpus.stopwords is used including any extra words provided by 
        the user and excluding any words provided by the user.
    
        Parameters
        ----------
        text: str
            The text data to remove stopwords from.

        extra_words: list[str]
            A list of words to include in the stopwords list.

        exclude_words: list[str]
            A list of words to remove from the stopwords list.
    
        Returns
        -------
        str: The text string containing the input with all stopwords removed.
    '''

    stopword_list = stopwords.words('english')

    # If any extra words were provided add them to the stopwords list.
    stopword_list = stopword_list + extra_words if extra_words is not None else stopword_list

    # If any exclude words were provided remove them from the stopwords list.
    [stopword_list.remove(word) for word in (exclude_words if exclude_words is not None else [])]
    
    # For each word in text remove the word if it is a stopword and return the joined result in a string.
    text = [word for word in text.split() if word not in stopword_list]
    return ' '.join(text)