
# coding: utf-8


# Init
import pandas as pd
import sys
import time
import synonyms
import flashtext
import time
from flashtext import KeywordProcessor

# define input and output path and read files into pandas dataframe
input_path = '~/Documents/Job/Word-Similarity/Input/'
out_path = '~/Documents/Job/Word-Similarity/Output/'
keywords = pd.read_csv(input_path+'articles1000.csv')[['title','keywords']]
organizations = pd.read_csv(input_path+'organizations.csv')
people = pd.read_csv(input_path+'people.csv')
techniques = pd.read_csv(input_path+'techniques.csv')

# merge all dictionaries into a single file and clean data
entities = pd.concat([organizations['Name'],people['Name'],techniques['Name']])
entities = entities.dropna(axis=0,how='all').drop_duplicates().reset_index(drop=True).str.lower().to_frame('name')

#parameters
testnum = 19
threshold = 0.99

# define keywords match function. Input are keywords and entities, generate output of keywords-matched entities

def samematch(): # same words match
    keywords['entity']=''
    for i in range(len(keywords)):
        keywords['entity'][i]=[]
        for ii in range(len(keywords['keywords'][i].split(','))):
            for j in range(len(entities)):
                if entities['name'][j] ==keywords['keywords'][i].split(',')[ii]:
                    keywords['entity'][i].append(entities['name'][j])
    nermatch()
    return(keywords)

def similarmatch():   # similar words match by using synonyms
    keywords['entity']=''
    for i in range(testnum):
        keywords['entity'][i]=[]
        for ii in range(len(keywords['keywords'][i].split(','))):
            for j in range(len(entities)):
                if synonyms.compare(entities['name'][j],keywords['keywords'][i].split(',')[ii],seg=False)>threshold: # if exceed threshold, select it as similar word
                    keywords['entity'][i].append(entities['name'][j])
    nermatch()
    return(keywords)
    

# match same words using FlashText
def flashmatch():
    lentities = entities['name'].tolist()
    processor = KeywordProcessor()
    processor.add_keywords_from_list(lentities)
    keywords['entity']=''
    for i in range(len(keywords)):
        keywords['entity'][i]=processor.extract_keywords(keywords['keywords'][i])
    nermatch()
    return(keywords)

# name entity recognization match
def nermatch():  
    keywords['flag']=''
    for i in range(len(keywords)):
        keywords['flag'][i]=[]
        for ii in range(len(keywords['keywords'][i].split(','))):
            words = synonyms.seg(keywords['keywords'][i].split(',')[ii])
            keywords['flag'][i].append(words[1])
            if keywords['flag'][i][ii]=='nt' or keywords['flag'][i][ii]=='nr':
                keywords['entity'][i].append(word.word)    

if __name__ == '__main__':
    start = time.time()
    if sys.argv[1] == 'same':
        keywords = samematch()
    elif sys.argv[1] == 'flash':
        keywords = flashmatch()
    else:
    	keywords = similarmatch()
    end = time.time()
    print('Time:',end-start)
    # adjust the output form and save results to output folder
    keywords.drop('flag',axis=1,inplace=True)
    for i in range(len(keywords)):
        keywords['entity'][i]=','.join(keywords['entity'][i])
    keywords.to_csv(out_path+'match.csv')

