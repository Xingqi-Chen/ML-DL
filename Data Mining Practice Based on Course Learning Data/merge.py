import matplotlib.pyplot as plt
import numpy as np
import nltk
import pandas as pd

df = pd.read_excel('format.xls',header=None)
dataArray = np.array(df)

dedata = np.delete(dataArray, 0, axis=1)#去除第一列，即sid的数组
showDx = 0
showDy = 1

#绘制数据分布图
plt.scatter(dedata[:, showDx], dedata[:, showDy], c = "red", marker='o', label='label')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend(loc=2)
plt.show()

def manhattan(point1, point2):
 	dimension = len(point1)
 	result = 0.0
 	for i in range(dimension):
         result += abs(point1[i] - point2[i])
 	return result

def merge(distance):
    emdata = dedata
    num_means = 3
    if distance == nltk.cluster.util.cosine_distance:
        emdata = np.delete(dedata,[6,7],axis=1)
        num_means = 2
        
    estimator = nltk.cluster.kmeans.KMeansClusterer(num_means=num_means,distance=distance)
    estimator.cluster(emdata)#聚类
    label_pred = [] #聚类标签
    for data in emdata:
        label_pred.append(estimator.classify(data))
    label_pred = np.array(label_pred)
    
    #绘制k-means结果
    x0 = emdata[label_pred == 0]
    x1 = emdata[label_pred == 1]
    x2 = emdata[label_pred == 2]
    plt.scatter(x0[:, showDx], x0[:, showDy], c = "red", marker='o', label='label0')
    plt.scatter(x1[:, showDx], x1[:, showDy], c = "green", marker='*', label='label1')
    plt.scatter(x2[:, showDx], x2[:, showDy], c = "blue", marker='+', label='label2')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend(loc=2)
    plt.show()
    
    estimator_center = np.array(estimator.means())
    print('聚类中心:')
    print(estimator_center)
    
merge(nltk.cluster.util.euclidean_distance) #欧式距离
merge(nltk.cluster.util.cosine_distance)  #余弦距离
merge(manhattan) #曼哈顿距离