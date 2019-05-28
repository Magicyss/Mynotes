import numpy as np
class LogisticRegression():

    def __init__(self):
        self.w = None

    def _sigmoid(self,x):
        return 1 / (1 + np.exp(-x))

    def fit(self,x, y, eta=1e-3, n_iters=10000):
        self.w = np.array([1 for i in range(x.shape[1])])
        o = np.array([1 for i in range(x.shape[0])])
        p = np.array([1 for i in range(x.shape[0])])
        for i in range(n_iters):
            o = np.dot(x, self.w)
            p = self._sigmoid(o)
            self.w = self.w - eta * np.dot((p - y), x)

    def predict(self,x):
        o = np.array([1 for i in range(x.shape[0])])
        p = np.array([1 for i in range(x.shape[0])])
        o = np.dot(x, self.w)
        p = self._sigmoid(o)
        return p