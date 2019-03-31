from os.path import isfile
import pandas
import praw
from time import sleep
reddit = praw.Reddit('DEFAULT')
import json
import os.path

def get_comments(post_id, submission):
    # Create the post object and get all comments
    submission.comments.replace_more(limit=None)

    # dictionaries to store id:comment and hierarchies of comments
    comment_dict = dict()
    comment_dict[submission.fullname] = dict()
    comment_dict[submission.fullname]['body'] = submission.title
    comment_dict[submission.fullname]['replies'] = list()

    # Root = submisison fullname
    # Immediate children = first-level comment fullnames
    for cmt in submission.comments:
        comment_dict[submission.fullname]['replies'].append(cmt.fullname)

    # BFS on comments
    comment_queue = submission.comments[:]
    while comment_queue:
        comment = comment_queue.pop(0)
        comment_dict[comment.fullname] = dict()
        comment_dict[comment.fullname]['body'] = comment.body
        comment_dict[comment.fullname]['timestamp'] = comment.created
        comment_dict[comment.fullname]['replies'] = list()

        # queue current comment's replies
        comment_queue.extend(comment.replies)
        for reply in comment.replies:
            comment_dict[comment.fullname]['replies'].append(reply.fullname)

    return comment_dict

def get_comments_JSON(post_id):
    submission = reddit.submission(id=post_id)
    comment_dict = get_comments(post_id, submission)

    submission_dict = dict()
    submission_dict['fullname'] = submission.fullname
    submission_dict['subreddit'] = submission.subreddit.display_name
    submission_dict['title'] = submission.title
    submission_dict['author'] = submission.author.name
    submission_dict['timestamp'] = submission.created

    return submission_dict, comment_dict

def extract_comment_id(url):
    tokens = url.split("/")
    return tokens[6]

import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def clean_text(text, stop=False, lemmatize=False, stem=False):
    """
    Cleans the input text.
    Args:
        text (str): raw text body

    Returns:
        text (str): cleaned text
        tokens (list): list of lemmatized tokens of the cleaned text
    """
    # lower case
    text = text.lower()

    # remove numbers
    text = re.sub(r'\d+', '', text)

    # remove punctuations
    text = re.sub(r'[^\w\s]','',text)

    # remove '\n', '\t'
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = ' '.join(text.split())

    # remove stop words
    if stop:
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text)
        tokens = [i for i in tokens if i not in stop_words]

    # lemmatize tokens
    if lemmatize:
        tokens = [lemmatizer.lemmatize(i) for i in tokens]

    # stemming tokens
    if stem:
        tokens = [stemmer.stem(i) for i in tokens]

    return text, tokens

import operator
import collections

def sort_dict(dictionary, by_value=False, reverse=False):
    """
    Sorts the input dictionary

    Args:
        dictionary (dict): input dictionary to be sorted
        by_value (bool): sort by value defaults to False
        reverse (bool): reverse sort defaults to False

    Returns:
        sorted_dict(dict): sorted dictionary with the input dict
    """
    index = 1 if by_value else 0
    sorted_list = sorted(dictionary.items(), key=lambda kv: kv[index], reverse=reverse)
    sorted_dict = collections.OrderedDict(sorted_list)
    return sorted_dict

def term_frequency(tokens):
    """
    Calculates term frequencies of the given tokens

    Args:
        tokens (list): list of tokens

    Returns:
        dict: a dictionary sorted by the value.
              key = tokens, value = frequency of key in tokens
    """
    freq_dict = dict()
    for token in tokens:
        if token not in freq_dict:
            freq_dict[token] = 1
        else:
            freq_dict[token] += 1

    return sort_dict(freq_dict, by_value=True, reverse=True)

import math
def pmi(text, a, b, text_len=0):
    """
    Calculates the Pointwise Mutual Information of two words

    Args:
        text(str): input text body
        a(str): word 1
        b(str): word 2
        text_len = number of words in text, defaults to 0
    """
    if len(text) != 0 and text_len == 0:
        text_len = len(text.split(' '))
    ab = a + ' ' + b
    ab_count = text.count(ab)
    if ab_count == 0:
        return 0
    a_count = text.count(a)
    b_count = text.count(b)
    p_ab = ab_count / (text_len-1)
    p_a = a_count / text_len
    p_b = b_count / text_len
    ratio = p_ab / (p_a * p_b)
    return math.log(ratio, 2), p_ab, p_a, p_b

def mutual_info(text):
    """
    Calculates the mutual information of the input text body

    Args:
        text(str): input text body

    Returns:
        mutual_info (float): mutual information of the input text body
        pmi_dict (dict): keys = word pairs, value = pmi of the key
    """
    word_list = text.split(' ')
    len_list = len(word_list)
    pmi_dict = dict()
    mutual_info = 0
    for i in range(0, len(word_list)-1):
        word1 = word_list[i]
        word2 = word_list[i+1]
        curr_pmi, p_ab, p_a, p_b = pmi(text, word1, word2, len_list)
        word_pair = word1 + ' ' + word2
        if word_pair not in pmi_dict:
            pmi_dict[word_pair] = curr_pmi
            mutual_info += curr_pmi * p_ab
    pmi_dict = sort_dict(pmi_dict, by_value=True, reverse=True)
    return mutual_info, pmi_dict
