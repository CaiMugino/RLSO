#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import print_to_file as p2f
import feature4
from matplotlib import pyplot
import math
import recommendation
import csv
from evaluation import Evaluation
import aggregation


# 先计算session中每个浏览商品次数下“第一位”商品（非点击流），然后整合这些第一位商品，得出该session最有可能购买的商品。

class Recommendation_aggregate:

    @staticmethod
    def generate(click_file_path, buy_file_path, test_file_path,
                 U, V, theta, aspects_num, session_item_data, dic, item_session_times_dic,
                 res_dir, part_num, aggregate_num):

        # calculate favorite aspect of each session in test data
        session_aspect_dic = recommendation.calc_favorite_aspect(V, aspects_num, session_item_data)
        # session_aspect_dic = calc_favorite_aspect2(U, session_item_data)
        # 加入item ICR
        # item_list = get_item_list(click_file_path)
        # item_ICR_dic = get_item_ICR(click_file_path, buy_file_path, item_list)

        # 计算各个session里浏览商品的购买概率，并进行排序（原始模型的预测方法）
        session_idx_item_prob_dic1 = \
            calc_item_prob(V, theta, aspects_num, dic, session_aspect_dic, dic, item_session_times_dic, 1)

        # 计算各个session里浏览商品的购买概率，并进行排序（模型不变，在结对比较的时候，如果一个商品在session里出现了超过两次，他的结对也是都需要出现的）
        session_idx_item_prob_dic2 = \
            calc_item_prob(V, theta, aspects_num, dic, session_aspect_dic, dic, item_session_times_dic, 2)

        # 计算各个session里浏览商品的购买概率，并进行排序（模型在计算概率v_i/(v_i+v _j)的时候，在每个项目的值前面都乘以1+exp（在该session里出现次数））
        session_idx_item_prob_dic3 = \
            calc_item_prob(V, theta, aspects_num, dic, session_aspect_dic, dic, item_session_times_dic, 3)

        # 分别对aggregate1~aggregate_num+1每种整合方法计算calc_item_prob，calc_item_prob2，calc_item_prob3的结果
        for i in range(1, aggregate_num+1):
            aggregate_method = i
            data = select_aggregate_method(dic, item_session_times_dic, session_item_data,
                            session_idx_item_prob_dic1, session_idx_item_prob_dic2, session_idx_item_prob_dic3,
                                           aggregate_method, part_num)
            # 将实验结果输出到excel中
            print_2_excel(res_dir, aggregate_method, data)


def select_aggregate_method(dic, item_session_times_dic, session_item_data,
                            session_idx_item_prob_dic1, session_idx_item_prob_dic2, session_idx_item_prob_dic3,
                            aggregate_method, part_num):

    # 待输出到excel中的结果
    data = list()

    if aggregate_method == 1:
        print("aggregate1")
        # prob_aggregate1——“整合”每次浏览的结果
        session_item_prob_dic = prob_aggregate1(dic, session_idx_item_prob_dic1, item_session_times_dic)
        # p1 = evaluate(session_item_data, session_item_prob_dic)
        # data += ["", str('%.4f' % p1), ""]
        # 整合策略(整合出一个最有可能购买的商品)的评价指标只能用p@1
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = prob_aggregate1(dic, session_idx_item_prob_dic2, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = prob_aggregate1(dic, session_idx_item_prob_dic3, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]
    elif aggregate_method == 2:
        print("aggregate2")
        # prob_aggregate2——“整合”每次浏览的结果
        session_item_prob_dic = prob_aggregate2(dic, session_idx_item_prob_dic1, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = prob_aggregate2(dic, session_idx_item_prob_dic2, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = prob_aggregate2(dic, session_idx_item_prob_dic3, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]
    elif aggregate_method == 3:
        print("aggregate3")
        # prob_aggregate3——“整合”每次浏览的结果
        session_item_prob_dic = prob_aggregate3(dic, session_idx_item_prob_dic1, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = prob_aggregate3(dic, session_idx_item_prob_dic2, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = prob_aggregate3(dic, session_idx_item_prob_dic3, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]
    elif aggregate_method == 4:
        print("aggregate4")
        # prob_aggregate4——“整合”每次浏览的结果
        session_item_prob_dic = prob_aggregate4(dic, session_idx_item_prob_dic1, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = prob_aggregate4(dic, session_idx_item_prob_dic2, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = prob_aggregate4(dic, session_idx_item_prob_dic3, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]
    elif aggregate_method == 5:
        print("aggregate", str(aggregate_method))
        # prob_aggregate4——“整合”每次浏览的结果
        session_item_prob_dic = aggregation.aggregate5(dic, session_idx_item_prob_dic1, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = aggregation.aggregate5(dic, session_idx_item_prob_dic2, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = aggregation.aggregate5(dic, session_idx_item_prob_dic3, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]
    elif aggregate_method == 6:
        print("aggregate", str(aggregate_method))
        # prob_aggregate4——“整合”每次浏览的结果
        session_item_prob_dic = aggregation.aggregate6(dic, session_idx_item_prob_dic1, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = aggregation.aggregate6(dic, session_idx_item_prob_dic2, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = aggregation.aggregate6(dic, session_idx_item_prob_dic3, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]
    elif aggregate_method == 7:
        print("aggregate", str(aggregate_method))
        # prob_aggregate4——“整合”每次浏览的结果
        session_item_prob_dic = aggregation.aggregate7(dic, session_idx_item_prob_dic1, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = aggregation.aggregate7(dic, session_idx_item_prob_dic2, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = aggregation.aggregate7(dic, session_idx_item_prob_dic3, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]
    elif aggregate_method == 8:
        print("aggregate", str(aggregate_method))
        # prob_aggregate4——“整合”每次浏览的结果
        session_item_prob_dic = aggregation.aggregate8(dic, session_idx_item_prob_dic1, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = aggregation.aggregate8(dic, session_idx_item_prob_dic2, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = aggregation.aggregate8(dic, session_idx_item_prob_dic3, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]
    elif aggregate_method == 9:
        print("aggregate", str(aggregate_method))
        # prob_aggregate4——“整合”每次浏览的结果
        session_item_prob_dic = aggregation.aggregate9(dic, session_idx_item_prob_dic1, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = aggregation.aggregate9(dic, session_idx_item_prob_dic2, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]

        session_item_prob_dic = aggregation.aggregate9(dic, session_idx_item_prob_dic3, item_session_times_dic)
        precision = Evaluation.calc_precision_at_n(session_item_data, session_item_prob_dic, 1)
        data += ["", str('%.4f' % precision), ""]
    else:
        print("select_aggregate_method parameter error!")
        exit()

    return data


# 将结果输出到excel中
def print_2_excel(res_dir, aggregate_method, data):
    res_file_path = res_dir + '\\' + 'Recommendation_aggregate' + str(aggregate_method) + '.csv'
    file = open(res_file_path, 'a', newline='')
    writer = csv.writer(file)
    try:
        writer.writerow(data)
    except Exception as e:
        print(e)
    finally:
        file.close()


def calc_item_prob(V, theta, aspects_num, session_item_data, session_aspect_dic, dic, item_session_times_dic, para):
    session_item_prob_dic = dict()
    session_idx_item_prob_dic = dict()
    for session in dic.keys():

        favorite_aspect = session_aspect_dic[session]
        # 列出当前session所有浏览过的商品，依次计算各个商品为skyline object的概率
        # 当前session所有浏览过的商品(item按点击顺序存放)
        click_items = dic[session]
        click_num = len(click_items)
        key = (session, 1)
        session_idx_item_prob_dic[key] = list()
        # 第一次只有一个点击商品，其概率为1
        session_idx_item_prob_dic[key].append([click_items[0], 1])
        # 有两个、三个...click_num个点击商品，依次类推，依次计算各个点击商品为skyline object的概率
        # 这里的2不可变动
        for i in range(2, click_num+1):
            key = (session, i)
            session_idx_item_prob_dic[key] = list()
            # 计算当前session已浏览i个商品时，各个商品为skyline object的概率
            # calc_item_prob_help(V, theta, aspects_num, click_items[0:i], favorite_aspect, session_idx_item_prob_dic[key])
            # 说明：calc_item_prob_help2: 在结对比较的时候，如果一个商品在session里出现了超过两次，他的结对也是都需要出现的
            # 说明：calc_item_prob_help3: 计算商品为skyline object概率的时候，每个项目的值前面都乘以 1+exp(商品在该session里出现次数)
            if para==1:
                calc_item_prob_help(V, theta, aspects_num, click_items[0:i], favorite_aspect,
                                     session_idx_item_prob_dic[key], session, item_session_times_dic)
            elif para==2:
                calc_item_prob_help2(V, theta, aspects_num, click_items[0:i], favorite_aspect,
                                    session_idx_item_prob_dic[key], session, item_session_times_dic)
            elif para == 3:
                calc_item_prob_help3(V, theta, aspects_num, click_items[0:i], favorite_aspect,
                                     session_idx_item_prob_dic[key], session, item_session_times_dic)

    return session_idx_item_prob_dic


def calc_item_prob_help(V, theta, aspects_num, cur_items, a, cur_item_prob, session, item_session_times_dic):

    favorite_aspect = a

    # 随机扰动session中各个item的位置（以便后续的排序更合理）
    # random.shuffle(cur_items)

    for w in cur_items:
        if sum(V[w]) == 0:
            prob = 0.0
            cur_item_prob.append([w, prob])
        else:
            temp_product = 1
            for v in cur_items:
                if v != w:
                    for k in range(aspects_num):
                        if k == favorite_aspect:
                            if (V[w][k] + theta * V[v][k]) == 0:
                                while True:
                                    print('division error in def calc_item_prob_help ')
                            temp_product *= V[w][k] / (V[w][k] + theta * V[v][k])
                        else:
                            temp_product *= (theta * V[w][k]) / (V[v][k] + theta * V[w][k])

            # 该session中商品w为skyline object的概率
            cur_item_prob.append([w, temp_product])

    # 当当前session各个商品的分数不全为0时，对各个商品分数进行归一化
    s = 0
    for i in range(len(cur_item_prob)):
        s += cur_item_prob[i][1]
    if s != 0:
        normalize(cur_item_prob)
    # 对当前session中各个商品的分数进行排序
    cur_item_prob.sort(key=lambda x: x[1], reverse=True)


# 在结对比较的时候，如果一个商品在session里出现了超过两次，他的结对也是都需要出现的
def calc_item_prob_help2(V, theta, aspects_num, cur_items, a, cur_item_prob, session, item_session_times_dic):

    favorite_aspect = a

    # 随机扰动session中各个item的位置（以便后续的排序更合理）
    # random.shuffle(cur_items)

    for w in cur_items:
        w_times = item_session_times_dic[(w, session)]
        if sum(V[w]) == 0:
            prob = 0.0
            cur_item_prob.append([w, prob])
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

            # 该session中商品w为skyline object的概率
            cur_item_prob.append([w, temp])

    # 当当前session各个商品的分数不全为0时，对各个商品分数进行归一化
    s = 0
    for i in range(len(cur_item_prob)):
        s += cur_item_prob[i][1]
    if s != 0:
        normalize(cur_item_prob)
    # 对当前session中各个商品的分数进行排序
    cur_item_prob.sort(key=lambda x: x[1], reverse=True)


# 计算商品为skyline object概率的时候，每个项目的值前面都乘以 1+exp(商品在该session里出现次数)
def calc_item_prob_help3(V, theta, aspects_num, cur_items, a, cur_item_prob, session, item_session_times_dic):

    favorite_aspect = a

    # 随机扰动session中各个item的位置（以便后续的排序更合理）
    # random.shuffle(cur_items)

    for w in cur_items:
        w_times = item_session_times_dic[(w, session)]
        w_factor = 1 + math.exp(w_times)
        if sum(V[w]) == 0:
            prob = 0.0
            cur_item_prob.append([w, prob])
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

            # 该session中商品w为skyline object的概率
            cur_item_prob.append([w, temp_product])

    # 当当前session各个商品的分数不全为0时，对各个商品分数进行归一化
    s = 0
    for i in range(len(cur_item_prob)):
        s += cur_item_prob[i][1]
    if s != 0:
        normalize(cur_item_prob)
    # 对当前session中各个商品的分数进行排序
    cur_item_prob.sort(key=lambda x: x[1], reverse=True)


# “整合”每次浏览的结果——计算当前session每个商品被列为“第一位”商品的次数
def prob_aggregate1(dic, session_idx_item_prob_dic, item_session_times_dic):
    aim_dic = dict()
    for session in dic.keys():
        # 当前session所有浏览过的商品
        click_items = dic[session]
        click_num = len(click_items)
        item1_count_dic = dict()
        # 这里的1/2可调（算上第一个点击商品/不算上第一个点击商品），取其中效果好的
        for i in range(2, click_num+1):
            key = (session, i)
            # 此时“第一位”的商品及其概率
            [item1, prob1] = session_idx_item_prob_dic[key][0]
            item1_times = item_session_times_dic[(item1, session)]
            if item1 not in item1_count_dic.keys():
                item1_count_dic[item1] = 1
            else:
                item1_count_dic[item1] += 1   # 这里用的是商品在session里面出现的次数作为累计计数值（或换为1/item1_times）
        # 找出当前session最多次位于“第一位”的商品
        aim_item = find_1stValue_key(click_items, item1_count_dic)
        aim_dic[session] = list()
        # 注意这里一个session只有预测的第一个skyline object的商品，并人为设置其概率为1
        aim_dic[session].append([aim_item, 1])
    return aim_dic


# “整合”每次浏览的结果——将商品在session里面出现的次数作为计数值，计算当前session每个商品被列为“第一位”商品的次数
def prob_aggregate2(dic, session_idx_item_prob_dic, item_session_times_dic):
    aim_dic = dict()
    for session in dic.keys():
        # 当前session所有浏览过的商品
        click_items = dic[session]
        click_num = len(click_items)
        item1_count_dic = dict()
        # 这里的1/2可调（算上第一个点击商品/不算上第一个点击商品），取其中效果好的
        for i in range(2, click_num+1):
            key = (session, i)
            # 此时“第一位”的商品及其概率
            [item1, prob1] = session_idx_item_prob_dic[key][0]
            item1_times = item_session_times_dic[(item1, session)]
            if item1 not in item1_count_dic.keys():
                item1_count_dic[item1] = item1_times    # 这里用的是商品在session里面出现的次数作为累计计数值（或换为1/item1_times）
            else:
                item1_count_dic[item1] += item1_times   # 这里用的是商品在session里面出现的次数作为累计计数值（或换为1/item1_times）
        # 找出当前session最多次位于“第一位”的商品
        aim_item = find_1stValue_key(click_items, item1_count_dic)
        aim_dic[session] = list()
        # 注意这里一个session只有预测的第一个skyline object的商品，并人为设置其概率为1
        aim_dic[session].append([aim_item, 1])
    return aim_dic


# “整合”每次浏览的结果（# 取“第一位”商品“在session中出现最多次”的商品作为最终预测购买商品）
def prob_aggregate3(dic, session_idx_item_prob_dic, item_session_times_dic):
    aim_dic = dict()
    for session in dic.keys():
        # 当前session所有浏览过的商品
        click_items = dic[session]
        click_items_num = len(click_items)
        max_times = 0
        # 算上第一个点击商品/不算上第一个点击商品
        # 这里的1/2可调
        up_bound = click_items_num
        for i in range(1, up_bound+1):      # 这种aggregate方法里第一个点击商品考虑进去是比较合理的
            key = (session, i)
            # 此时“第一位”的商品及其概率
            [item1, prob1] = session_idx_item_prob_dic[key][0]
            item1_times = item_session_times_dic[(item1, session)]
            if item1_times >= max_times:
                max_times = item1_times
                aim_item = item1
        aim_dic[session] = list()
        # 注意这里一个session只有预测的第一个skyline object的商品，并人为设置其概率为1
        aim_dic[session].append([aim_item, 1])
    return aim_dic


# “整合”每次浏览的结果（# 取“第一位”商品“在session中出现最多次”的商品作为最终预测购买商品）（只取前五个第一位商品进行整合）
def prob_aggregate4(dic, session_idx_item_prob_dic, item_session_times_dic):
    aim_dic = dict()
    for session in dic.keys():
        # 当前session所有浏览过的商品
        click_items = dic[session]
        click_items_num = len(click_items)
        max_times = 0
        # 算上第一个点击商品/不算上第一个点击商品
        # 这里的1/2可调
        up_bound = min([5, click_items_num])      # “只取前5”
        for i in range(1, up_bound+1):
            key = (session, i)
            # 此时“第一位”的商品及其概率
            [item1, prob1] = session_idx_item_prob_dic[key][0]
            item1_times = item_session_times_dic[(item1, session)]
            if item1_times >= max_times:
                max_times = item1_times
                aim_item = item1
        aim_dic[session] = list()
        # 注意这里一个session只有预测的第一个skyline object的商品，并人为设置其概率为1
        aim_dic[session].append([aim_item, 1])
    return aim_dic


# 找出dict中值最大的对应的key。对于形如｛1:10, 2:20, 3:30, 4:20｝，结果为3；对于形如｛1:10, 2:20, 4:20｝，结果为2
def find_1stValue_key(click_items, item1_count_dic):
    cur_item1s = item1_count_dic.keys()
    max_value = 0
    aim_key = 0
    # 对于当前session每个浏览的商品（按照浏览顺序）
    for item in click_items:
        if item in cur_item1s:
            if item1_count_dic[item] > max_value:
                max_value = item1_count_dic[item]
                aim_key = item
    return aim_key


# 形如[[1, 0.3], [2, 0.3]]， 归一化为[[1, 0.5], [2, 0.5]]
# 用于归一化商品为skyline object的概率
def normalize(ls):
    s = 0
    for i in range(len(ls)):
        s += ls[i][1]
    for i in range(len(ls)):
        ls[i][1] = ls[i][1]/s


def evaluate(session_item_data, session_item_prob_dic):
    p1 = calc_precision_at_1(session_item_data, session_item_prob_dic)
    # p2 = calc_precision_at_2(session_item_data, session_item_prob_dic)
    # MRR = calc_MRR(session_item_data, session_item_prob_dic)
    print('p1: ' + ('%.4f' % p1))
    # print('p2: ' + ('%.4f' % p2))
    # print('MRR: ' + ('%.4f' % MRR))
    return p1


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
    MRR /= len(session_item_data)
    return MRR


# proving_列出每个session每次浏览排在“第一位”的所有skyline object(检验所有“第一位”商品的准确率上限)
def proving_session_item1s(dic, session_idx_item_prob_dic):
    session_item1s_dic = dict()
    for session in dic.keys():
        # 当前session所有浏览过的商品
        click_items = dic[session]
        click_num = len(click_items)
        session_item1s_dic[session] = list()
        # 当前session所有排在“第一位”的商品
        cur_item1_set = set()
        # 计算当前session每个商品在“第一位”出现的次数
        # 这里的1不可变动
        for i in range(1, click_num + 1):
            key = (session, i)
            # 此时“第一位”的商品及其概率
            [item1, prob1] = session_idx_item_prob_dic[key][0]
            if item1 not in cur_item1_set:
                session_item1s_dic[session].append(item1)
                cur_item1_set.add(item1)

    return session_item1s_dic


# proving evaluation
def proving_evaluate(session_item_data, proving_session_item1s_dic):
    p1 = proving_calc_precision_at_1(session_item_data, proving_session_item1s_dic)
    print('proving p1: ' + ('%.4f' % p1))


# proving calc_precision_at_1
def proving_calc_precision_at_1(session_item_data, proving_session_item1s_dic):
    p = 0.0
    for cur_data in session_item_data:
        session = cur_data[0]
        cur_buy_items = cur_data[1]
        cur_item1s = proving_session_item1s_dic[session]
        for item1 in cur_item1s:
            if item1 in cur_buy_items:
                p += 1.0
                break
    p /= len(session_item_data)
    return p


# early predict relevant statistic（购买商品第一次出现在“预测商品第一位”时session的浏览商品数）
def early_predict_statistic(session_item_data, session_idx_item_prob_dic):
    session_buyItemFirstRank1Idx_dic = dict()
    for cur_data in session_item_data:
        # early predict relevant statistic（购买商品第一次出现在“预测商品第一位”时session的浏览商品数）
        session = cur_data[0]
        cur_buy_items = cur_data[1]
        cur_click_items = cur_data[1] + cur_data[2]
        click_num = len(cur_click_items)
        # 初始化为0，放置存在当前session所有浏览商品数目下排在第一位的商品都不是购买商品的情况
        session_buyItemFirstRank1Idx_dic[session] = 0
        for i in range(1, click_num+1):
            key = (session, i)
            cur_item_prob = session_idx_item_prob_dic[key]
            # 判断当前浏览商品数目下的cur_item_prob中，排在第一位的商品是否为购买商品
            if cur_item_prob[0][0] in cur_buy_items:
                session_buyItemFirstRank1Idx_dic[session] = i
                break

    return session_buyItemFirstRank1Idx_dic


if __name__ == '__main__':
    # test
    click_items = [1, 2, 3, 4, 5]
    item1_count_dic = {1: 30, 2: 20, 3: 30, 4: 20}
    k = find_1stValue_key(click_items, item1_count_dic)
    print(k)
