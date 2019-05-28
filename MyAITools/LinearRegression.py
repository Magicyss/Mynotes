import numpy as np
class LinearRegression():

    def __init__(self):
        self.theta = None

    def fit(self,train_data,train_label):
        x=np.hstack(([[1] for i in range(train_data.shape[0])],train_data))
        xtx=np.dot(np.transpose(x),x)
        xtx_1=np.linalg.inv(xtx)
        self.theta=np.dot(np.dot(xtx_1,np.transpose(x)),train_label)

    def predict(self,test_data):
        x=np.hstack(([[1] for i in range(test_data.shape[0])],test_data))
        return np.dot(x,self.theta)