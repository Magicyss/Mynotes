import numpy as np

class Kmeans():
    def __init__(self, k=2, max_iterations=500, error=0.0001):
        self.k = k
        self.max_iterations = max_iterations # 迭代次数
        self.error = error # 两次迭代之间的误差值
        self.centroids = None # 中心点
        np.random.seed(1)

    def random_centroids(self, X):  # 随机生成中心
        point_index_lst = np.arange(len(X))
        np.random.shuffle(point_index_lst)
        self.centroids = X[point_index_lst[:self.k]]

    def _cal_distance(self, sample):  # 计算样本对于中心的距离
        one_sample = sample.reshape(1, -1)
        distance = np.power(np.tile(one_sample, (self.centroids.shape[0], 1)) - self.centroids, 2).sum(axis=1)
        return distance

    def _closest_centroid(self, sample):  # 生成单个样本最近的中心点的下标
        distance = self._cal_distance(sample)
        closest_i = np.argmin(distance)
        return closest_i

    def create_clusters(self, X):  # 生成多个样本最近的中心点的下标的集合
        clusters = [[] for _ in range(self.k)]
        for sample_i, sample in enumerate(X):
            centroid_i = self._closest_centroid(sample)
            clusters[centroid_i].append(sample_i)
        return clusters

    def update_centroids(self, clusters, X):  # 对中心进行更新
        centroids = np.zeros((self.k, X.shape[1]))
        for i, cluster in enumerate(clusters):
            centroid = np.mean(X[cluster], axis=0)
            centroids[i] = centroid
        return centroids

    def fit(self, X):  # 学习训练集
        self.random_centroids(X)
        for i in range(self.max_iterations):
            clusters = self.create_clusters(X)
            new = self.update_centroids(clusters, X)
            if (np.max(np.fabs(new - self.centroids)) < self.error):
                break
            self.centroids = new

    def predict(self, X):  # 预测
        results = np.zeros(X.shape[0])
        for i, sample in enumerate(X):
            centroid = self._closest_centroid(sample)
            results[i] = centroid
        return results

