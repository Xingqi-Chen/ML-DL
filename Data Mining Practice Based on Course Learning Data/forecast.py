import numpy as np
import pandas as pd
from sklearn import ensemble
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

df = pd.read_excel('format.xls',header=None)
dataArray = np.array(df)

#绘制id-分数散点图
X = dataArray[:,0]
Y = dataArray[:,-1]
plt.scatter(X,Y)
ax=plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(50))
plt.show()

dataArray = np.delete(dataArray, 0, axis=1) #去除id
label = [] #score转换为的label
for score in dataArray[:,-1]:
    if score < 0.2:
        score = 0
    elif score < 0.8:
        score = 1
    else:
        score = 2
    label.append(score)

dataArray[:,-1] = label


dataSize = len(dataArray)
trainDataSize = int(dataSize*0.7)

trainDataSet = dataArray[0:trainDataSize,:]
testDataSet = dataArray[trainDataSize:dataSize,:]


train_x = trainDataSet[:,0:-1]
train_y = trainDataSet[:,-1]

test_x = testDataSet[:,0:-1]
test_y = testDataSet[:,-1]

tree=ensemble.RandomForestClassifier()
tree.fit(train_x,train_y)

print(tree.score(test_x,test_y))