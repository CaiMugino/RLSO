#!/usr/bin/env python
# -*- coding:utf-8 -*-


# Recommendation22的另外几种整合方法

# ordinary utility比较试验之“累加”第一位商品的normalized score(不考虑第一个点击商品，因为若总共只点击两个商品的话，那一定是预测为第一个点击商品)
def aggregate5(dic, session_idx_item_prob_dic, item_session_times_dic):
    session_item_prob_dic = dict()
    for session in dic.keys():
        # 当前session所有浏览过的商品
        click_items = dic[session]
        click_num = len(click_items)
        item1_value_dic = dict()
        # 计算当前session每个商品在每个浏览次数下“第一位”商品出现的次数
        # 算上第一个点击商品/不算上第一个点击商品
        # 这里的1/2可调
        for i in range(2, click_num + 1):           # 暂时不考虑第一位商品，可以调一下试试
            key = (session, i)
            # 此时“第一位”的商品及其概率
            [item1, prob1] = session_idx_item_prob_dic[key][0]
            item1_times = item_session_times_dic[(item1, session)]
            if item1 not in item1_value_dic.keys():
                item1_value_dic[item1] = prob1
            else:
                item1_value_dic[item1] += prob1
        # 找出当前“值最大”的“第一位”商品
        aim_item = find_1stValue_key(click_items, item1_value_dic)
        session_item_prob_dic[session] = list()
        # 注意这里一个session只有预测的第一个skyline object的商品，并人为设置其概率为1
        session_item_prob_dic[session].append([aim_item, 1])
    return session_item_prob_dic


# ordinary utility比较试验之“累加”第一位商品的normalized score之后取平均(不考虑第一个点击商品，因为若总共只点击两个商品的话，那一定是预测为第一个点击商品)
def aggregate6(dic, session_idx_item_prob_dic, item_session_times_dic):
    session_item_prob_dic = dict()
    for session in dic.keys():
        # 当前session所有浏览过的商品
        click_items = dic[session]
        click_num = len(click_items)
        item1_count_dic = dict()
        item1_value_dic = dict()
        # 计算当前session每个商品在每个浏览次数下“第一位”商品出现的次数
        # 算上第一个点击商品/不算上第一个点击商品
        # 这里的1/2可调
        for i in range(2, click_num + 1):           # 暂时不考虑第一位商品，可以调一下试试
            key = (session, i)
            # 此时“第一位”的商品及其概率
            [item1, prob1] = session_idx_item_prob_dic[key][0]
            item1_times = item_session_times_dic[(item1, session)]
            if item1 not in item1_value_dic.keys():
                item1_value_dic[item1] = prob1
                item1_count_dic[item1] = 1
            else:
                item1_value_dic[item1] += prob1
                item1_count_dic[item1] += 1
        # 取平均
        for item1 in item1_value_dic.keys():
            item1_value_dic[item1] = item1_value_dic[item1]/item1_count_dic[item1]
        # 找出当前“值最大”的“第一位”商品
        aim_item = find_1stValue_key(click_items, item1_value_dic)
        session_item_prob_dic[session] = list()
        # 注意这里一个session只有预测的第一个skyline object的商品，并人为设置其概率为1
        session_item_prob_dic[session].append([aim_item, 1])
    return session_item_prob_dic


# ordinary utility比较试验之累加“第一位商品的normalized score与后面商品的（和的）差”(不考虑第一个点击商品，因为若总共只点击两个商品的话，那一定是预测为第一个点击商品)
def aggregate7(dic, session_idx_item_prob_dic, item_session_times_dic):
    session_item_prob_dic = dict()
    for session in dic.keys():
        # 当前session所有浏览过的商品
        click_items = dic[session]
        click_num = len(click_items)
        item1_count_dic = dict()
        item1_value_dic = dict()
        # 计算当前session每个商品在每个浏览次数下“第一位”商品出现的次数
        # 算上第一个点击商品/不算上第一个点击商品
        # 这里的1/2可调
        for i in range(2, click_num + 1):           # 暂时不考虑第一位商品，可以调一下试试
            key = (session, i)
            # 此时“第一位”的商品及其概率
            [item1, prob1] = session_idx_item_prob_dic[key][0]
            item1_times = item_session_times_dic[(item1, session)]
            # 第一位商品的normalized score与后面的（和的）差
            prob1_diff = 2*prob1-1;
            if item1 not in item1_value_dic.keys():
                item1_value_dic[item1] = prob1_diff
                item1_count_dic[item1] = 1
            else:
                item1_value_dic[item1] += prob1_diff
                item1_count_dic[item1] += 1
        # 取平均
        for item1 in item1_value_dic.keys():
            item1_value_dic[item1] = item1_value_dic[item1]/item1_count_dic[item1]
        # 找出当前“值最大”的“第一位”商品
        aim_item = find_1stValue_key(click_items, item1_value_dic)
        session_item_prob_dic[session] = list()
        # 注意这里一个session只有预测的第一个skyline object的商品，并人为设置其概率为1
        session_item_prob_dic[session].append([aim_item, 1])
    return session_item_prob_dic


# （第一位商品累加出现次数的平均）=第一位商品累加出现次数/该商品在session中的出现次数
def aggregate8(dic, session_idx_item_prob_dic, item_session_times_dic):
    session_item_prob_dic = dict()
    for session in dic.keys():
        # 当前session所有浏览过的商品
        click_items = dic[session]
        click_num = len(click_items)
        item1_count_dic = dict()
        # 计算当前session每个商品在每个浏览次数下“第一位”商品出现的次数
        # 算上第一个点击商品/不算上第一个点击商品
        # 这里的1/2可调
        for i in range(1, click_num + 1):           # 暂时不考虑第一位商品，可以调一下试试
            key = (session, i)
            # 此时“第一位”的商品及其概率
            [item1, prob1] = session_idx_item_prob_dic[key][0]
            item1_times = item_session_times_dic[(item1, session)]
            if item1 not in item1_count_dic.keys():
                item1_count_dic[item1] = 1
            else:
                item1_count_dic[item1] += 1
        # 取平均
        for item1 in item1_count_dic.keys():
            item1_times = item_session_times_dic[(item1, session)]
            item1_count_dic[item1] = item1_count_dic[item1]/item1_times
        # 找出当前“值最大”的“第一位”商品
        aim_item = find_1stValue_key(click_items, item1_count_dic)
        session_item_prob_dic[session] = list()
        # 注意这里一个session只有预测的第一个skyline object的商品，并人为设置其概率为1
        session_item_prob_dic[session].append([aim_item, 1])
    return session_item_prob_dic


# 取滑动窗口
def aggregate9(dic, session_idx_item_prob_dic, item_session_times_dic):
    WIN = 3
    session_item_prob_dic = dict()
    for session in dic.keys():
        # 当前session所有浏览过的商品
        click_items = dic[session]
        click_num = len(click_items)
        # 计算当前session每个商品在每个浏览次数下“第一位”商品出现的次数
        # 算上第一个点击商品/不算上第一个点击商品
        # 这里的1/2可调
        for i in range(1, click_num + 1):           # 暂时不考虑第一位商品，可以调一下试试
            key = (session, i)
            # 此时“第一位”的商品及其概率
            [item1, prob1] = session_idx_item_prob_dic[key][0]

            # 滑动窗口方法
            if i==1:
                sliding_item1 = item1
                count = 1
            else:
                # 当前“第一位”商品与上一个“第一位”商品相同
                if item1 == sliding_item1:
                    count += 1
                else:  # 当前“第一位”商品与上一个“第一位”商品不同
                    sliding_item1 = item1
                    count = 1

            # 点击商品个数小于3，已点击到第二个商品时：
            if click_num == 2 and i==2:
                aim_item = item1

            # 已经连续三个第一位商品相同
            if count == 3:
                aim_item = item1
                break

            # 该session不满足滑动窗口条件
            if i == click_num:
                aim_item = item1
                break

        session_item_prob_dic[session] = list()
        # 注意这里一个session只有预测的第一个skyline object的商品，并人为设置其概率为1
        session_item_prob_dic[session].append([aim_item, 1])
    return session_item_prob_dic






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