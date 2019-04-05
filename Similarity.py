
# coding: utf-8


# Init
import pandas as pd
# define input and output path and read files into pandas dataframe
input_path = '~/Word-Similarity/Input/'
out_path = '~/Word-Similarity/Output/'
keywords = pd.read_csv(input_path+'title_keyword.csv')[['title','keywords']]
organizations = pd.read_csv(input_path+'organizations.csv')
people = pd.read_csv(input_path+'people.csv')
techniques = pd.read_csv(input_path+'techniques.csv')

# merge all dictionaries into a single file and clean data
entities = pd.concat([organizations['Name'],people['Name'],techniques['Name']])
entities = entities.dropna(axis=0,how='all').drop_duplicates().reset_index(drop=True).str.lower().to_frame('name')

# define keywords match function. Input are keywords and entities, generate output of keywords-matched entities

def keywordsmatch(keywords,entities):
    # same and similar words match by using synonyms
    import synonyms
    keywords['entity']=''
    for i in range(len(keywords)):
        keywords['entity'][i]=[]
        for ii in range(len(keywords['keywords'][i].split(','))):
            for j in range(len(entities)):
                if synonyms.compare(entities['name'][j],keywords['keywords'][i].split(',')[ii],seg=False)>0.6: # if score>0.6, select it as similar word
                    keywords['entity'][i].append(entities['name'][j])

    # use jieba.posseg for name entity recognization match
    import jieba.posseg as pseg
    keywords['flag']=''
    for i in range(len(keywords)):
        keywords['flag'][i]=[]
        for ii in range(len(keywords['keywords'][i].split(','))):
            words = pseg.cut(keywords['keywords'][i].split(',')[ii])
            for word in words:
                keywords['flag'][i].append(word.flag)
            if keywords['flag'][i][ii]=='nt' or keywords['flag'][i][ii]=='nr':
                keywords['entity'][i].append(word.word)    
    return(keywords)

if __name__ == '__main__':
    
    keywords = keywordsmatch(keywords,entities)
    # adjust the output form and save results to output folder
    keywords.drop('flag',axis=1,inplace=True)
    for i in range(len(keywords)):
        keywords['entity'][i]=','.join(keywords['entity'][i])
    keywords.to_excel(out_path+'match.xlsx')

