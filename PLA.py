# -*- coding: utf-8 -*-
"""
获取当前py源程序文件的位置，并将用到的mlxtend包加入系统目录
"""
import sys, os

currentPath = os.getcwd()
sys.path.append(os.path.join(currentPath, 'mlxtend'))

import numpy as np


class Perceptron(object):

    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.w = np.random.rand(1 + self.X.shape[1])
        print('分割线w:{}'.format(self.w))
        # self.w = np.zeros(1 + X.shape[1])
        # self.w = np.ones(1 + X.shape[1])

        self.error_xi = []
        self.error_yi = []

    def check_error(self):
        foundError = False
        error = 0
        for xi, yi in zip(X, y):
            if self.predict(xi) != yi:
                self.error_xi = xi
                self.error_yi = yi
                error += 1
                foundError = True
        print("error=%s/%s" % (error, len(X)))
        return foundError

    def run(self):

        while self.check_error() == True:
            xi = self.error_xi
            yi = self.error_yi
            yi = -1 if yi == 0 else 1
            self.w[1:] += yi * xi
            self.w[0] += yi

    def net_input(self, X):
        return np.dot(X, self.w[1:]) + self.w[0]

    def predict(self, X):
        return np.where(self.net_input(X) < 0.0, 0, 1)


if __name__ == '__main__':
    """
    Loading Data
    """
    from mlxtend.data import iris_data

    X, y = iris_data()
    X = X[:, [0, 3]]  # sepal length and petal width
    X = X[0:100]  # class 0 and class 1
    y = y[0:100]  # class 0 and class 1

    ## standardize
    # X[:,0] = (X[:,0] - X[:,0].mean()) / X[:,0].std()
    # X[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()

    """
    Plotting Decision Regions
    """
    import matplotlib.pyplot as plt
    from mlxtend.plotting import plot_decision_regions

    print('x 是{}'.format(X))
    print('y 是{}'.format(y))
    ppn = Perceptron(X, y)
    ppn.run()
    print('Weights: %s' % ppn.w)

    plot_decision_regions(X, y, clf=ppn)
    plt.title('Perceptron')

    plt.xlabel('sepal length [cm]')
    plt.ylabel('petal length [cm]')
    plt.show()




