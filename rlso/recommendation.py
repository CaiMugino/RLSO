#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import random
import print_to_file as p2f
import math
import csv
import copy
from evaluation import Evaluation
#from evaluation_alldata_03 import EvaluationAllData
#注释掉不敢删除，EvaluationAllData只在注释中出现，但我不能判断注释掉的内容是否有用。

# 原始：对每个session，对所有点击商品计算一遍各个商品的购买概率，然后从高到低排序。



class Recommendation:

    item_ICR_dic = {}
    @staticmethod
    def generate(U, V, theta, aspects_num, session_item_data, dic, item_session_times_dic,
                              res_dir):

        # calculate favorite aspect of each session in test data
        session_aspect_dic = calc_favorite_aspect(V, aspects_num, session_item_data)

        # session_aspect_dic = calc_favorite_aspect2(U, session_item_data)
        # 加入item ICR
        click_file_path = '..\\data\\yoochoose-selected\\yoochoose-clicks-selected.dat'
        buy_file_path = '..\\data\\yoochoose-selected\\yoochoose-buys-selected.dat'
        click_file_path2 = '..\\data\\yoochoose-selected\\yoochoose-test-selected.dat'

        #item_list = get_item_list(click_file_path)
        #self.item_ICR_dic = get_item_ICR(click_file_path, buy_file_path, 1, item_list)
        #item_ICR_dic = get_item_ICR(click_file_path, buy_file_path, item_list)

        # 计算各个session里浏览商品的购买概率，并进行排序
        # session_item_prob_dic = calc_item_prob(V, theta, aspects_num, session_item_data, session_aspect_dic)
        # 说明：calc_item_prob2：在结对比较的时候，如果一个商品在session里出现了超过两次，他的结对也是都需要出现的
        # 说明：calc_item_prob3：计算商品为skyline object概率的时候，每个项目的值前面都乘以 1+exp(商品在该session里出现次数)

        # 将结果输出到文件中
        res_file_path = res_dir + r'\Recommendation11.csv'
        file = open(res_file_path, 'a', newline='')
        writer = csv.writer(file)
        data = list()
        try:
            # # 原始预测方法 calc_item_prob


            session_item_prob_dic1 = calc_item_prob(V, theta, aspects_num, dic, session_aspect_dic,
                                                   item_session_times_dic)


            # precision = EvaluationAllData.calc_precision_at_n(session_item_data, session_item_prob_dic)
            # MRR = EvaluationAllData.calc_MRR(session_item_data, session_item_prob_dic)
            #         data += ["",str('%.4f' % precision), "", ""]
            # data += [str('%.4f' % part_num), str('%.4f' % precision), str('%.4f' % MRR), ""]

            session_item_prob_dic2 = calc_item_prob2(V, theta, aspects_num, dic, session_aspect_dic,
                                                   item_session_times_dic)


            # # # calc_item_prob2：在结对比较的时候，如果一个商品在session里出现了超过两次，他的结对也是都需要出现的
            # session_item_prob_dic = calc_item_prob2(V, theta, aspects_num, dic, session_aspect_dic,
            #                                     item_session_times_dic)
            # precision = EvaluationAllData.calc_precision_at_n(session_item_data, session_item_prob_dic)
            # MRR = EvaluationAllData.calc_MRR(session_item_data, session_item_prob_dic)
            # data += ["",str('%.4f' % precision), str('%.4f' % MRR), ""]
            #
            # # # calc_item_prob3：计算商品为skyline object概率的时候，每个项目的值前面都乘以 1+exp(商品在该session里出现次数)
            session_item_prob_dic3 = calc_item_prob3(V, theta, aspects_num, dic, session_aspect_dic,
                                                   item_session_times_dic)

            for cur_data in session_item_data:
                precision1 = 0.0
                MRR1 = 0.0
                precision2 = 0.0
                MRR2 = 0.0
                precision3 = 0.0
                MRR3 = 0.0

                session = cur_data[0]
                n = len(cur_data[1])
                cur_buy_items = cur_data[1]
                #print("计算购买个数:", n)
                # def calc_precision(session_item_prob_dic):
                #     precision=0.0
                #     cur_item_prob = session_item_prob_dic[session]
                #     for i in range(n):
                #         if cur_item_prob[i][0] in cur_buy_items:
                #             precision += 1 / n
                #             return precision
                # def calc_mrr(session_item_prob_dic):
                #     MRR=0.0
                #     cur_item_prob = session_item_prob_dic[session]
                #     for i in range(len(cur_item_prob)):
                #         if cur_item_prob[i][0] in cur_buy_items:
                #             MRR += 1.0 / (i + 1)
                #             break
                #         return  MRR
                cur_item_prob = session_item_prob_dic1[session]

                for i in range(n):
                    if cur_item_prob[i][0] in cur_buy_items:
                        precision1 += 1 / n
                for i in range(len(cur_item_prob)):
                    if cur_item_prob[i][0] in cur_buy_items:
                        MRR1 += 1.0 / (i + 1)
                        break

                cur_item_prob = session_item_prob_dic2[session]
                for i in range(n):
                    if cur_item_prob[i][0] in cur_buy_items:
                        precision2 += 1 / n
                for i in range(len(cur_item_prob)):
                    if cur_item_prob[i][0] in cur_buy_items:
                        MRR2 += 1.0 / (i + 1)
                        break

                cur_item_prob = session_item_prob_dic3[session]
                for i in range(n):
                    if cur_item_prob[i][0] in cur_buy_items:
                        precision3 += 1 / n
                for i in range(len(cur_item_prob)):
                    if cur_item_prob[i][0] in cur_buy_items:
                        MRR3 += 1.0 / (i + 1)
                        break
                # precision1 = calc_precision(session_item_prob_dic1)
                # MRR1 = calc_mrr(session_item_prob_dic1)
                #
                # precision2 = calc_precision(session_item_prob_dic2)
                # MRR2 = calc_mrr(session_item_prob_dic2)
                #
                # precision3 = calc_precision(session_item_prob_dic3)
                # MRR3 = calc_mrr(session_item_prob_dic3)

                data = [str('%.4f' % session), str('%.4f' % precision1), str('%.4f' % MRR1), "",
                        "", str('%.4f' % precision2), str('%.4f' % MRR2),
                        "", str('%.4f' % precision3), str('%.4f' % MRR3)]
                writer.writerow(data)


                # # 后面的不要了
                # session = cur_data[0]
                # n = len(cur_data[1])
                # cur_buy_items = cur_data[1]
                # cur_item_prob = session_item_prob_dic[session]
                #
                # print("计算precision中的购买个数:", n)
                # for i in range(n):
                #     if cur_item_prob[i][0] in cur_buy_items:
                #         precision += 1 / n
                #
                # for i in range(len(cur_item_prob)):
                #     if cur_item_prob[i][0] in cur_buy_items:
                #         MRR += 1.0 / (i + 1)
                #         break
                # data = ["", str('%.4f' % precision), str('%.4f' % MRR), ""]
                #
                # writer.writerow(data)
            # precision = EvaluationAllData.calc_precision_at_n(session_item_data, session_item_prob_dic)
            # MRR = EvaluationAllData.calc_MRR(session_item_data, session_item_prob_dic)
            # data += ["",str('%.4f' % precision), str('%.4f' % MRR),""]

        except Exception as e:
            print(e)
        finally:
            file.close()


# 按照老师session推荐里favorite aspect的计算方式
def calc_favorite_aspect(V, aspects_num, session_item_data):
    session_aspect_dic = dict()
    for cur_data in session_item_data:
        session = cur_data[0]
        cur_items = list()
        for v in cur_data[1]:
            cur_items.append(v)
        for v in cur_data[2]:
            cur_items.append(v)

        sum_of_vk = list()
        for k in range(aspects_num):
            s = 0
            for item in cur_items:
                s += V[item][k]
            sum_of_vk.append(s)

        max_val = max(sum_of_vk)
        favorite_aspect = sum_of_vk.index(max_val)

        session_aspect_dic[session] = favorite_aspect

    return session_aspect_dic


def calc_item_prob(V, theta, aspects_num, dic, session_aspect_dic, item_session_times_dic):
    session_item_prob_dic = dict()
    session_item_prob_list = list()


    for session in dic.keys():
        cur_items = dic[session]

        # # 随机扰动session中各个item的位置（以便后续的排序更合理）
        # random.shuffle(cur_items)

        favorite_aspect = session_aspect_dic[session]

        session_item_prob_dic[session] = list()
        for w in cur_items:
            if sum(V[w]) == 0:
                prob = 0.0
                session_item_prob_dic[session].append([w, prob])
            else:
                temp_product = 1
                for v in cur_items:
                    if v != w:
                        for k in range(aspects_num):
                            if k == favorite_aspect:
                                if (V[w][k] + theta * V[v][k]) == 0:
                                    print('division error')
                                temp_product *= V[w][k] / (V[w][k] + theta * V[v][k])
                            else:
                                temp_product *= (theta * V[w][k]) / (V[v][k] + theta * V[w][k])
                # 加入item ICR
                #item_ICR = self.item_ICR_dic[w]
                #temp_product *= item_ICR
                # 该session中商品w为skyline object的概率
                session_item_prob_dic[session].append([w, temp_product])

        cur_item_prob = session_item_prob_dic[session]
        # 当当前session各个商品的分数不全为0时，对各个商品分数进行归一化
        s = 0
        for i in range(len(cur_item_prob)):
            s += cur_item_prob[i][1]
        if s != 0:
            normalize(cur_item_prob)
        cur_session_prob = copy.deepcopy(session_item_prob_dic[session])
        for flag in cur_session_prob:
            flag.insert(0,session)
            session_item_prob_list.append(flag)
        # 对当前session中各个商品的分数进行排序
        cur_item_prob.sort(key=lambda x: x[1], reverse=True)


    # prob_file_path = r'E:\ranking aggregation\code\result\yoochoose\Full\sampling@0.01@partition\train\prob.txt'
    # p2f.print_list_dict_to_file()

    # for cur_data in session_item_data:
    #     session = cur_data[0]
    #     cur_item_prob = session_item_prob_dic[session]
    #     print(cur_item_prob)
    session_item_prob_ndarray = np.array(session_item_prob_list)
    print(session_item_prob_ndarray)
    np.savetxt('predict_1.csv',session_item_prob_ndarray,delimiter=',',header='sessionID,itemID,prob',comments='',fmt="%.8f")
    #print(session_item_prob_dic)
    return session_item_prob_dic


# 在结对比较的时候，如果一个商品在session里出现了超过两次，他的结对也是都需要出现的
def calc_item_prob2(V, theta, aspects_num, dic, session_aspect_dic, item_session_times_dic):
    session_item_prob_dic = dict()
    session_item_prob_list = list()

    for session in dic.keys():
        cur_items = dic[session]

        # # 随机扰动session中各个item的位置（以便后续的排序更合理）
        # random.shuffle(cur_items)

        favorite_aspect = session_aspect_dic[session]

        session_item_prob_dic[session] = list()
        for w in cur_items:
            w_times = item_session_times_dic[(w, session)]
            if sum(V[w]) == 0:
                prob = 0.0
                session_item_prob_dic[session].append([w, prob])
            else:
                temp = 1
                for v in cur_items:
                    if v != w:
                        v_times = item_session_times_dic[(v, session)]
                        temp2 = 1
                        for k in range(aspects_num):
                            if k == favorite_aspect:
                                if (V[w][k] + theta * V[v][k]) == 0:
                                    print('division error')
                                temp2 *= V[w][k] / (V[w][k] + theta * V[v][k])
                            else:
                                temp2 *= (theta * V[w][k]) / (V[v][k] + theta * V[w][k])
                            temp2 *= (w_times * v_times)
                        temp *= temp2
                # 加入item ICR
                #item_ICR = self.item_ICR_dic[w]
                #temp_product *= item_ICR
                # 该session中商品w为skyline object的概率
                session_item_prob_dic[session].append([w, temp])

        cur_item_prob = session_item_prob_dic[session]
        # 当当前session各个商品的分数不全为0时，对各个商品分数进行归一化
        s = 0
        for i in range(len(cur_item_prob)):
            s += cur_item_prob[i][1]
        if s != 0:
            normalize(cur_item_prob)
        cur_session_prob = copy.deepcopy(session_item_prob_dic[session])
        for flag in cur_session_prob:
            flag.insert(0,session)
            session_item_prob_list.append(flag)
        # 对当前session中各个商品的分数进行排序
        cur_item_prob.sort(key=lambda x: x[1], reverse=True)


    # prob_file_path = r'E:\ranking aggregation\code\result\yoochoose\Full\sampling@0.01@partition\train\prob.txt'
    # p2f.print_list_dict_to_file()

    # for cur_data in session_item_data:
    #     session = cur_data[0]
    #     cur_item_prob = session_item_prob_dic[session]
    #     print(cur_item_prob)
    session_item_prob_ndarray = np.array(session_item_prob_list)
    print(session_item_prob_ndarray)
    np.savetxt('predict_2.csv',session_item_prob_ndarray,delimiter=',',header='sessionID,itemID,prob',comments='',fmt="%.8f")
    #print(session_item_prob_dic)
    return session_item_prob_dic


# 计算商品为skyline object概率的时候，每个项目的值前面都乘以 1+exp(商品在该session里出现次数)
def calc_item_prob3(V, theta, aspects_num, dic, session_aspect_dic, item_session_times_dic):
    session_item_prob_dic = dict()
    session_item_prob_list = list()
    for session in dic.keys():
        cur_items = dic[session]

        # # 随机扰动session中各个item的位置（以便后续的排序更合理）
        # random.shuffle(cur_items)

        favorite_aspect = session_aspect_dic[session]

        session_item_prob_dic[session] = list()
        for w in cur_items:
            w_times = item_session_times_dic[(w, session)]
            w_factor = 1 + math.exp(w_times)
            if sum(V[w]) == 0:
                prob = 0.0
                session_item_prob_dic[session].append([w, prob])
            else:
                temp_product = 1
                for v in cur_items:
                    if v != w:
                        v_times = item_session_times_dic[(v, session)]
                        v_factor = 1 + math.exp(v_times)
                        for k in range(aspects_num):
                            if k == favorite_aspect:
                                if (V[w][k] + theta * V[v][k]) == 0:
                                    print('division error in def calc_item_prob_help ')
                                    exit()
                                temp_product *= (w_factor * V[w][k]) / (w_factor * V[w][k] + theta * v_factor * V[v][k])
                            else:
                                temp_product *= (theta * w_factor * V[w][k]) / (v_factor * V[v][k] + theta * w_factor * V[w][k])
                # # 加入item ICR
                #item_ICR = self.item_ICR_dic[w]
                #temp_product *= item_ICR
                # 该session中商品w为skyline object的概率
                session_item_prob_dic[session].append([w, temp_product])

        cur_item_prob = session_item_prob_dic[session]
        # 当当前session各个商品的分数不全为0时，对各个商品分数进行归一化
        s = 0
        for i in range(len(cur_item_prob)):
            s += cur_item_prob[i][1]
        if s != 0:
            normalize(cur_item_prob)
            
        cur_session_prob = copy.deepcopy(session_item_prob_dic[session])
        for flag in cur_session_prob:
            flag.insert(0,session)
            session_item_prob_list.append(flag)
        # 对当前session中各个商品的分数进行排序
        cur_item_prob.sort(key=lambda x: x[1], reverse=True)

    # prob_file_path = r'E:\ranking aggregation\code\result\yoochoose\Full\sampling@0.01@partition\train\prob.txt'
    # p2f.print_list_dict_to_file()

    # for cur_data in session_item_data:
    #     session = cur_data[0]
    #     cur_item_prob = session_item_prob_dic[session]
    #     print(cur_item_prob)
    session_item_prob_ndarray = np.array(session_item_prob_list)
    print(session_item_prob_ndarray)
    np.savetxt('predict_3.csv',session_item_prob_ndarray,delimiter=',',header='sessionID,itemID,prob',comments='',fmt="%.8f")
    #print(session_item_prob_dic)
    return session_item_prob_dic


# 形如[[1, 0.3], [2, 0.3]]， 归一化为[[1, 0.5], [2, 0.5]]
def normalize(ls):
    s = 0
    for i in range(len(ls)):
        s += ls[i][1]
    for i in range(len(ls)):
        ls[i][1] = ls[i][1]/s


def evaluate(session_item_data, session_item_prob_dic):
    p1 = calc_precision_at_1(session_item_data, session_item_prob_dic)
    p2 = calc_precision_at_2(session_item_data, session_item_prob_dic)
    MRR = calc_MRR(session_item_data, session_item_prob_dic)
    print('p1: ' + ('%.4f' % p1))
    print('p2: ' + ('%.4f' % p2))
    print('MRR: ' + ('%.4f' % MRR))
    return p1, p2, MRR


def calc_precision_at_1(session_item_data, session_item_prob_dic):
    p = 0.0
    for cur_data in session_item_data:
        session = cur_data[0]
        cur_buy_items = cur_data[1]
        cur_item_prob = session_item_prob_dic[session]
        if cur_item_prob[0][0] in cur_buy_items:
            p += 1.0
    p /= len(session_item_data)
    return p


def calc_precision_at_2(session_item_data, session_item_prob_dic):
    p = 0.0
    for cur_data in session_item_data:
        session = cur_data[0]
        cur_buy_items = cur_data[1]
        cur_item_prob = session_item_prob_dic[session]
        if cur_item_prob[0][0] in cur_buy_items:
            p += 0.5
        if cur_item_prob[1][0] in cur_buy_items:
            p += 0.5
    p /= len(session_item_data)
    return p


def calc_MRR(session_item_data, session_item_prob_dic):
    MRR = 0.0
    for cur_data in session_item_data:
        session = cur_data[0]
        cur_buy_items = cur_data[1]
        cur_item_prob = session_item_prob_dic[session]
        for i in range(len(cur_item_prob)):
            if (cur_item_prob[i][0]) in cur_buy_items:
                MRR += 1.0/(i+1)
                break
    MRR /= len(session_item_data)  #原来也是算平均的……
    return MRR

def get_item_list(file_path1, file_path2= None):
    item_list = list()
    # 训练集里的所有item
    file1 = open(file_path1)
    try:
        for line in file1:
            tmp = line.split(',')
            item_str = tmp[2]
            item = int(item_str)
            if item not in item_list:
                item_list.append(item)
    except Exception as e:
        print(e)
    finally:
        file1.close()
    # 测试集里的所有item
    '''
    file2 = open(file_path2)
    try:
        for line in file2:
            tmp = line.split(',')
            item_str = tmp[2]
            item = int(item_str)
            if item not in item_list:
                item_list.append(item)
    
    except Exception as e:
        print(e)
    finally:
        file2.close()
        '''
    return item_list

def get_item_ICR(click_file_path, buy_file_path, data_para, item_list):
    item_ICR_dic = dict()
    for item in item_list:
        item_ICR_dic[item] = 0
    if data_para == 1:
        # 训练数据的点击数据：每个商品被哪些session点击
        item_session_dic1 = get_item_clicked(click_file_path)
        # 训练数据的购买数据：每个商品被哪些session购买
        item_session_dic2 = get_item_clicked(buy_file_path)
    else:
        # 测试数据的点击数据：每个商品被哪些session点击
        item_session_dic1 = get_item_clicked(click_file_path)
        # 测试数据的购买数据：每个商品被哪些session购买
        item_session_dic2 = get_test_item_bought(buy_file_path)
    for item in item_session_dic2.keys():
        click_num = len(item_session_dic1[item])
        buy_num = len(item_session_dic2[item])
        item_ICR_dic[item] = 1.0 * buy_num / click_num
    return item_ICR_dic


# 每个商品被哪些session点击/购买（训练数据每个商品被哪些session点击/购买、测试数据每个商品被哪些session点击）——借此可求出：每个商品的总出现session次数
def get_item_clicked(file_path):
    item_session_dic = dict()
    item_set = set()
    file = open(file_path)
    try:
        for line in file:
            tmp = line.split(',')
            session_str = tmp[0]
            session = int(session_str)
            item_str = tmp[2]
            item = int(item_str)
            if item not in item_set:
                item_session_dic[item] = list()
                item_session_dic[item].append(session)
            else:
                if session not in item_session_dic[item]:
                    item_session_dic[item].append(session)
            item_set.add(item)
    except Exception as e:
        print(e)
    finally:
        file.close()
    return item_session_dic


if __name__ == '__main__':
    ls = [[1, 0.3], [2, 0.3]]
    normalize(ls)
    print(ls)
