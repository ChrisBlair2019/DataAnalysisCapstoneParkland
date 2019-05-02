import json


with open('post.json', 'r') as f:
    postsdict = json.load(f)

print(postsdict)