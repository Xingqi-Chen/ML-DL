import pandas as pd
import numpy as np
import math
import jieba

#计算TF-IDF
def getIDF(word):
    dataNum = len(dataDict) #语料库文档总数
    hasNum = 0 #容纳该词的文档数数目
    for dataSet in dataDict:
        if word in dataSet:
            hasNum += 1
    return math.log(dataNum/(hasNum+1))

def getTF(wordList,word):
    wordNum = len(wordList)
    num = 0
    for one in wordList:
        if one == word:
            num += 1
    return num/wordNum
    
def TF_IDF(wordsA,wordsB):
    #判断A与B的相似度,A与B皆为list
    wordSet = set() #A与B的词汇包
    tf_idf_A = []
    tf_idf_B = []
    for word in wordsA:
        if word not in wordSet:
            wordSet.add(word)
    for word in wordsB:
        if word not in wordSet:
            wordSet.add(word)
    for word in wordSet:
        #计算A
        tf = getTF(wordsA,word) #A的word的tf
        idf = getIDF(word) #word的idf
        tf_idf = tf * idf
        tf_idf_A.append(tf_idf)
        
        #计算B
        tf = getTF(wordsB,word)
        tf_idf = tf * idf
        tf_idf = tf * idf
        tf_idf_B.append(tf_idf)
    sim = np.sqrt(np.sum(np.square(np.array(tf_idf_A) - np.array(tf_idf_B))))
    return sim
    
#分词
def tokenizer(s):
    words = []
    cut = jieba.cut(s)
    for word in cut:
        if word not in stopwords:
            words.append(word)
    return words
 
def sentence2words(filePath):
    f = open(filePath)
    with open('chinsesstoptxt.txt', 'r', encoding='utf-8') as d:
        for line in d:
            if len(line)>0:
                stopwords.append(line.strip())
    result = ''
    for line in f:
        s = tokenizer(line.strip())
        result += " ".join(s)+"\n"
    return result.split('\n')

#建立语料库
reader = pd.read_csv('result1.csv',delimiter='\t',encoding='gb18030',header=None)
datalist = np.array(reader).tolist()
dataDict = [] #语料库
for line in datalist:
    words = line[0].split(',')
    wordSet = set()
    for word in words:
        wordSet.add(word)
    dataDict.append(wordSet)
    
stopwords = []
examplePara = []
words = sentence2words('csdn.txt')
for word in words:
    wordList = list(filter(None,word.split(' ')))
    if wordList != [] and len(wordList)>5:
        examplePara.append(wordList)
reader = pd.read_csv('result1.csv',delimiter='\t',encoding='gb18030',header=None)
datalist = np.array(reader).tolist()
simCount = 0 #判断为参考百度的篇章数
for line in datalist:
    words = line[0].split(',')
    sims = []
    for paph in examplePara:
        sim = TF_IDF(words,paph)
        sims.append(sim)
    if min(sims) > 0.6:
        continue
    simCount += 1
    index = sims.index(min(sims))
    #print(index,min(sims))
    #print(examplePara[index])
    #print(line)

print('参考此篇文章的答案数:',simCount)
print('所占比例:',simCount/len(datalist))