import numpy as np

class DecisionTree():

    def __init__(self):
        self.tree = {}

    def fit(self, train_feature, train_label):#无后剪枝
        self.tree = self.ID3(train_feature, train_label)

    def fit(self, train_feature, train_label, test_feature, test_label):#有后剪枝
        self.tree = self.ID3(train_feature, train_label)
        self.tree=self.cut_branch(self.tree,train_feature, train_label, test_feature, test_label)

    def predict(self, feature):
        result = []
        for i in feature:
            result.append(self.ID3_predict(self.tree, i))
        return np.array(result)

    def calcInfoGain(self, feature, label, index):# 三个关键性的数字，特征的总数以及每个特征的个数，还有每个特征中对应标签的个数
        feature_count={i:np.sum(feature[:,index]==i) for i in set(feature[:,index])}#统计关键数据,feature类别:此类个数
        label_count={i:{}for i in set(feature[:,index])}
        for i, j in enumerate(feature[:, index]):
            if label[i] not in label_count[j].keys():
                label_count[j][label[i]]=0
            label_count[j][label[i]]+=1
        percent = {i:[] for i in set(feature[:,index])}  # 单个特征的所占比例
        for i in set(feature[:,index]):
            percent[i].extend([j/feature_count[i] for j in label_count[i].values()])
        result={i:0.0for i in set(feature[:,index])}#记录结果，即单个特征的信息熵
        for i in set(feature[:,index]):
            for j in percent[i]:
                if j != 0 and j != 1:
                    result[i] += (-1) * j * np.log2(j) - (1 - j) * np.log2(1 - j)
        all=(-1)*sum([np.sum(label==i)/len(label)*np.log2(np.sum(label==i)/len(label)) for i in set(label)])#总熵
        answer=all-sum([i/len(label)*j for i,j in zip(feature_count.values(),result.values())])
        return answer

    def ID3_predict(self,tree, feature):
        first_feature = list(tree.keys())[0]  # 获取树的第一特征属性
        second_dict = tree[first_feature]  # 树的子树，子集合Dict
        for key in second_dict.keys():
            if feature[first_feature] == key:
                if isinstance(second_dict[key], dict):
                    class_label = self.ID3_predict(second_dict[key], feature)
                else:
                    class_label = second_dict[key]
                return class_label

    def testing(self,myTree, feature, label):
        error = 0.0
        for i, j in enumerate(feature):
            if self.ID3_predict(myTree, j) != label[i]:
                error += 1
        return error

    def testingMajor(self,major, sub_test_label):
        error = 0.0
        for i in sub_test_label:
            if major != i:
                error += 1
        return error

    def split_feature(self,feature, label, index, value):
        sub_feture = []
        sub_label = []
        for i, j in enumerate(feature):
            if j[index] == value:
                sub_feture.append(j)
                sub_label.append(label[i])
        return np.array(sub_feture), np.array(sub_label)

    def majorityCount(self,label):
        count = []
        for i in set(label):
            count.append((np.sum(label == i), i))
        best = count[0]
        for i in count:
            if best[0] < i[0]:
                best = i
        return best[1]

    def ID3(self,feature, label):
        if len(set(label)) == 1:
            return label[0]
        if len(feature[0]) == 1 or len(np.unique(feature, axis=0)) == 1:
            class_count = {}
            for vote in label:
                if vote not in class_count.keys():
                    class_count[vote] = 0
                class_count[vote] += 1
            sorted_class_count = sorted(class_count.items(), key=lambda x: x[1], reverse=True)
            return sorted_class_count[0][0]
        result = []
        for i in range(len(feature[0])):
            result.append((self.calcInfoGain(feature, label, i), i))
        result.sort()#整理增益熵的顺序，找出最大的
        my_tree = {result[-1][1]: {}}
        feature_values = [example[result[-1][1]] for example in feature]
        unique_feature_values = set(feature_values)
        for feature_value in unique_feature_values:
            sub_feature, sub_label = self.split_feature(feature, label, result[-1][1],feature_value)
            my_tree[result[-1][1]][feature_value] = self.ID3(np.array(sub_feature), np.array(sub_label))
        return my_tree

    def cut_branch(self,tree, feature, label, test_feature, test_label):
        first_feature = list(tree.keys())[0]  # 获取树的第一特征属性
        second_dict = tree[first_feature]  # 树的分子，子集合Dict
        for key in second_dict.keys():
            if isinstance(second_dict[key], dict):
                sub_feature, sub_label = self.split_feature(feature, label, first_feature, key)
                sub_test_feature, sub_test_label = self.split_feature(test_feature, test_label, first_feature, key)
                tree[first_feature][key] = self.cut_branch(second_dict[key], sub_feature, sub_label, sub_test_feature,sub_test_label)
        if self.testing(tree, feature, label) <= self.testingMajor(self.majorityCount(label), test_label):
            return tree
        return (self.majorityCount(label))