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
        comment_dict[comment.fullname]['replies'] = list()
        
        # queue current comment's replies
        comment_queue.extend(comment.replies)
        for reply in comment.replies:
            comment_dict[comment.fullname]['replies'].append(reply.fullname)
            
    return comment_dict
    
def write_comments_JSON(post_id, save_dir='./'):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    
    submission = reddit.submission(id=post_id)
    comment_dict = get_comments(post_id, submission)
    
    submission_dict = dict()
    submission_dict['fullname'] = submission.fullname
    submission_dict['subreddit'] = submission.subreddit.display_name
    submission_dict['title'] = submission.title
    submission_dict['author'] = submission.author.name
    submission_dict['timestamp'] = submission.created
    
    submission_dict = json.dumps(submission_dict)
    submission_json = json.loads(submission_dict)
    with open(save_dir+'post.json', 'a') as outfile: # write the output file
        json.dump(submission_json, outfile, indent=4)
    
    comment_dict = json.dumps(comment_dict)
    comment_json = json.loads(comment_dict)
    with open(save_dir + 'comment.json', 'a') as outfile:
        json.dump(comment_json, outfile, indent=4)
        
def extract_comment_id(url):
    tokens = url.split("/")
    return tokens[6]
