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

def clean_text(text):
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
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    tokens = [i for i in tokens if i not in stop_words]

    # lemmatize tokens
    tokens = [lemmatizer.lemmatize(i) for i in tokens]

    return text, tokens

import operator
import collections
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

    sorted_list = sorted(freq_dict.items(), key=lambda kv: kv[1], reverse=True)
    sorted_dict = collections.OrderedDict(sorted_list)
    return sorted_dict
