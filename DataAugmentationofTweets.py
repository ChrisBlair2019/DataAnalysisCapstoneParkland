#!/usr/bin/env python
# coding: utf-8

# In[72]:


import csv, re, csv, ast
from urlextract import URLExtract

index = 0
extractor = URLExtract()

urls = []
hashtags = []
mentions = []

filepath = '/Users/numankhan/numan-workspace/DataAnalysisCapstone/temp.csv'
with open(filepath) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:                
        urls.append(extractor.find_urls(row[9]))
        hashtags.append(re.findall(r"#(\w+)", row[9]))
        mentions.append(re.findall(r"@(\w+)", row[9]))





with open(filepath,'r') as csvinput:
    with open('/Users/numankhan/numan-workspace/DataAnalysisCapstone/output.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput)
        
        for row in csv.reader(csvinput):
            if row[0] == "screen_name":
                writer.writerow(row+["hashtags"])
            else:
                writer.writerow(row+[hashtags[index]])

            index = index + 1


            
index = 0

with open('/Users/numankhan/numan-workspace/DataAnalysisCapstone/output.csv','r') as csvinput:
    with open('/Users/numankhan/numan-workspace/DataAnalysisCapstone/output1.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput)

        for row in csv.reader(csvinput):
            if row[0] == "screen_name":
                writer.writerow(row+["mentions"])
            else:
                writer.writerow(row+[mentions[index]])
                
            index = index + 1
            
            
index = 0

with open('/Users/numankhan/numan-workspace/DataAnalysisCapstone/output1.csv','r') as csvinput:
    with open('/Users/numankhan/numan-workspace/DataAnalysisCapstone/output2.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput)

        for row in csv.reader(csvinput):
            if row[0] == "screen_name":
                writer.writerow(row+["url"])
            else:
                writer.writerow(row+[urls[index]])
                
            index = index + 1
            
            


            
            

            


# In[ ]:





# In[ ]:




