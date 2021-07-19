#coding:utf-8
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
from flask import Flask, request, jsonify
from flask import Blueprint
import json
import copy

class StockCluster():
    '''
    对基金进行聚类
    '''
    def __init__(self, path="data/stock.xlsx", k=120, iter=1000, interval=0.01):
        self.path = path
        self.k = k
        self.iter = iter
        self.interval = interval
        self.result, self.item2itemSim = self.get_sim()

    def get_sim(self):
        data = pd.read_excel(self.path)
        valid_column = ['基金简称', '日增长率', '近1周', '近1月', '近3月', '近6月', '近1年', '近2年', '近3年', '今年来', '成立来',
                        '2020-02-10至2021-03-09', '2020-03-11至2021-06-15']
        data = data[valid_column]
        result = {}
        for row in data.iterrows():
            name = row[1]['基金简称']
            result[name] = []
            for col in valid_column[1:]:
                result[name].append(row[1][col])

        sort_result = {}
        save_sort_result = {}
        for item in list(result.keys()):
            my_item = result[item]
            sort_result[item] = {}
            for meti in list(result.keys()):
                other_item = result[meti]
                score = self.eur_distance(my_item, other_item)
                sort_result[item][meti] = score
            save_sort_result[item] = sorted(sort_result[item].items(), key=lambda x: x[1], reverse=False)
        with open('data/相似度.txt', 'w') as fw:
            fw.write(str(save_sort_result))
        return result, sort_result

    def rm_nan(self, x_val, y_val):
        '''
        将x，y处理成可以做比较的向量，将x和y中的nan部分替换为相等的值
        '''
        x = copy.deepcopy(x_val)
        y = copy.deepcopy(y_val)
        for i, val in enumerate(x):
            if x[i] == y[i] and x[i] == '---':
                x[i] = 0
                y[i] = 0
            elif x[i] == '---':
                x[i] = y[i]
            elif y[i] == '---':
                y[i] = x[i]
        return x, y

    def eur_distance(self, x, y):
        '''
        计算欧式距离
        '''
        x, y = self.rm_nan(x, y)
        diff = []
        for i in range(len(x)):
            diff.append(x[i] - y[i])
        min_val = min(diff)
        max_val = max(diff)

        min_dist = 9999
        while min_val <= max_val:

            vector1 = np.array(x)
            vector2 = np.array(y)
            dist = np.linalg.norm(vector1 - vector2 - min_val)
            if dist < min_dist:
                min_dist = dist
            min_val = min_val + self.interval
        return min_dist

    def rm_empty(self):
        del_col = []
        for name in self.result:
            item = self.result[name]
            for i in item:
                try:
                    float(i)
                except:
                    del_col.append(name)
                    break
        for name in del_col:
            self.result.pop(name)
        print(len(self.result))
        return self.result

    def sample_k(self):
        samples = random.sample(list(self.item2itemSim.keys()), self.k)
        return samples

    def calc_sum(self, samples, total_items):
        '''
        给所有应用分配到以sample为中心的类内
        '''
        clusters = {}
        for item in total_items:
            min_val = 99999999
            for sample in samples:
                if self.item2itemSim[item][sample] < min_val:
                    min_val = self.item2itemSim[item][sample]
                    center = sample
            if center not in clusters:
                clusters[center]=[item]
            else:
                clusters[center].append(item)
        return clusters

    def calc_center(self, items):
        '''
        计算类内的中心
        :return:
        '''
        min_sum = 9999999
        for item_a in items:
            tmp_sum = 0
            for item_b in items:
                val = self.item2itemSim[item_a][item_b]
                tmp_sum += val
            if tmp_sum < min_sum:
                min_sum = tmp_sum
                center = item_a
        return center

    def calc_class(self, centers):
        '''
        计算所有类别内的相似度和
        :return:
        '''
        value = 0
        for item in centers:
            fuck = centers[item]
            for j in fuck:
                value += self.item2itemSim[item][j]
            # 类内距离距离减去类间距离
            # for other_item in centers:
            #     if other_item != item:
            #         fuckj = centers[other_item]
            #         for ij in fuckj:
            #             value -= self.item2itemSim[item][ij]
        return value

    def main(self, plot=True):
        '''
        要不要打印出来图
        :param plot:
        :return:
        '''
        min_value = 9999
        count = 0
        while count < self.iter:
            samples = self.sample_k()
            total_items = list(self.item2itemSim.keys())
            clusters = self.calc_sum(samples, total_items)
            for i in range(self.iter):
                samples = []
                for cluster in clusters:
                    items = clusters[cluster]
                    center = self.calc_center(items)
                    samples.append(center)
                clusters = self.calc_sum(samples, total_items)
                value = self.calc_class(clusters)
                if value < min_value:
                    min_value = value
                    print(samples)
                    print(min_value)
            count += 1

        if plot:
            for cluster in clusters:
                names = clusters[cluster]
                plot_result = []
                for item in names:
                    # print(item)
                    tmp = copy.deepcopy(self.result[item])
                    for j, val in enumerate(tmp):
                        if val == '---':
                            tmp[j] = 0
                    plot_result.append(tmp)
                self.plot_pic(plot_result, names, cluster)
        return clusters, self.item2itemSim

    def plot_pic(self, y_list, names, cluster):
        x = ['日增长率', '近1周', '近1月', '近3月', '近6月', '近1年', '近2年', '近3年', '今年来', '成立来', '2020-02-10至2021-03-09', '2020-03-11至2021-06-15']
        plt.title('指数型')  # 折线图标题
        plt.xlabel('指标')  # x轴标题
        plt.ylabel('值')  # y轴标题
        for item in y_list:
            plt.plot(x, item, marker='o', markersize=3, linewidth=0.4)  # 绘制折线图，添加数据点，设置点的大小
            for a, b in zip(x, item):
                plt.text(a, b, b, ha='center', va='bottom', fontsize=5)  # 设置数据标签位置及大小
        plt.legend(names, bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
        # plt.legend(names,loc='best')  # 设置折线名称
        # plt.show()  # 显示折线图
        plt.savefig('picture/'+cluster+'.png',dpi=600, bbox_inches='tight')
        # plt.savefig('picture/' + cluster + '.png', dpi=600)
        # plt.savefig('picture/'+cluster+'.pdf')
        plt.close()

if __name__=='__main__':
    clusters, sim_result = StockCluster(path="data/stock.xlsx", k=120, iter=100, interval=0.1).main(plot=False)
    print(clusters)
    print(sim_result)
    print("聚类结束！")
    with open('data/聚类结果.txt','w') as fw:
        fw.write(str(clusters))
