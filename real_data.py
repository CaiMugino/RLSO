#!/usr/bin/env python
# -*- coding:utf-8 -*-

import print_to_file as p2f
import read_from_file as rff
import matplotlib.pyplot as plt
import math
import random
import os

# 提取真实数据——用于模型（存在一定假设，如下注释所示。）
# 这里提取的真实数据只提取哪些同时包含购买商品和点击不购买商品的session，item的集合也只取这些session里面的,
# (续)就是那些不符合条件的session（包括没有购买商品或者全部点击商品都购买了的session）的item没有放到数据集里面。
def extract_real_data(click_file_path, buys_file_path, write_file_dir):
    print("processing click file...")
    # dic1表示点击数据中，每个session看了哪些商品
    dic1, all_sessions, all_items_set = get_session_itemList(click_file_path)

    print("processing buy file...")
    # 提取购买数据
    # dic2表示购买数据中某个session与"其购买商品的list"的map
    dic2, all_buy_sessions, all_buy_items_set = get_session_itemList(buys_file_path)

    print("extracting session_item_data...")
    # start = time.time()
    # 整合点击数据与购买数据，获取session_item_data
    allClicksBuy_sessions = list()
    # 此处data即为session_item_data
    data = list()
    # 提取出那些既有点击商品也有点击不购买商品的session
    all_data_sessions = list()
    # 只提取那些“既有点击商品也有点击不购买商品的session”的商品
    all_data_items_set = set()
    # 只考虑那些发生了购买行为的session（再去掉其中“所有点击商品都购买的session”）
    for d in all_buy_sessions:
        # 当前session所有点击商品
        click_items_list = dic1[d]
        click_nums = len(click_items_list)
        # 当前session所有购买商品
        buy_items_list = dic2[d]
        buy_nums = len(buy_items_list)
        # “去掉”所有点击商品都购买的session
        if click_nums == buy_nums:
            allClicksBuy_sessions.append(d)
        # 该session中既有购买商品，也有点击不购买商品
        else:
            all_data_sessions.append(d)
            # 只提取那些“既有点击商品也有点击不购买商品的session”的商品
            for item in click_items_list:
                all_data_items_set.add(item)
            click_items_set = set(click_items_list)
            buy_items_set = set(buy_items_list)
            click_not_buy_items_set = click_items_set - buy_items_set
            # 数据格式（每一行）：session;购买items（用逗号隔开）；点击不购买items（用逗号隔开）
            cur_data = [d, buy_items_list, list(click_not_buy_items_set)]
            # print("current data: ", cur_data)
            data.append(cur_data)
            # print2file(d, buy_items_list, click_not_buy_items_set)

    # 所有session
    all_sessions_set = set(all_sessions)
    # 所有点击商品都购买了的session
    allClicksBuy_sessions_set = set(allClicksBuy_sessions)
    # 既有购买商品，也有点击不购买商品的session
    all_data_sessions_set = set(all_data_sessions)
    # 所有点击商品都没有购买的session
    allClicksNotBuy_sessions_set = all_sessions_set - allClicksBuy_sessions_set - all_data_sessions_set

    # 所有"点击过但没被买的item"
    all_clickNotBuy_items_set = all_items_set - all_buy_items_set

    print("session item data: ", data)
    print("0、（data中的）既有购买商品，也有点击不购买商品的session: ", all_data_sessions)
    print("1、all_sessions: ", all_sessions)
    print("2、所有点击商品都购买了的session: ", allClicksBuy_sessions)
    print("3、所有点击商品都没有购买的session: ", allClicksNotBuy_sessions_set)
    print("4、data中的所有item: ", all_data_items_set)
    print("5、all_items: ", all_items_set)
    print("6、所有被购买的item: ", all_buy_items_set)
    print("7、所有点击过但没被买的item: ", all_clickNotBuy_items_set)
    print("printing to file...")

    allClicksNotBuy_sessions = list(allClicksNotBuy_sessions_set)
    all_data_items = list(all_data_items_set)
    all_items = list(all_items_set)
    all_buy_items = list(all_buy_items_set)
    all_clickNotBuy_items = list(all_clickNotBuy_items_set)

    # 输出数据到文件中
    session_item_write_path = write_file_dir + r"\session_item.txt"
    p2f.print_data_lists_to_file(data, session_item_write_path)
    # 其他有用信息
    print2file_list = [all_data_sessions, all_sessions, allClicksBuy_sessions, allClicksNotBuy_sessions,
                       all_data_items, all_items, all_buy_items, all_clickNotBuy_items]
    file_name_list = ["all_data_sessions.txt", "all_sessions.txt", "allClicksBuy_sessions.txt",
                      "allClicksNotBuy_sessions.txt", "items.txt", "all_items.txt", "all_buy_items.txt",
                      "all_clickNotBuy_items.txt"]
    idx = 0
    for cur_list in print2file_list:
        cur_file_path = write_file_dir + "\\" + file_name_list[idx]
        p2f.print_list_to_file(cur_list, cur_file_path)
        idx += 1

    print("finish extracting real data")


# 提取真实数据——用于统计分析
# 这里提取的真实数据包含所有session的数据（包括没有购买商品或者全部点击商品都购买了的session）
def extract_real_data1(click_file_path, buys_file_path, write_file_dir):
    print("processing click file...")
    # dic1表示点击数据中，每个session看了哪些商品
    dic1, all_sessions, all_items_set = get_session_itemList(click_file_path)

    print("processing buy file...")
    # 提取购买数据
    # dic2表示购买数据中，某个session与"其购买商品的list"的map
    dic2, all_buy_sessions, all_buy_items_set = get_session_itemList(buys_file_path)

    print("extracting session_item_data...")
    # 此处data即为session_item_data
    data = list()
    all_data_items_set = set()
    # 考虑所有的session（包括没有购买商品或者全部点击商品都购买了的session）
    idx = 1
    # 节约时间——表示一个session是否有购买了商品
    session_flag_dic = dict()
    for d in all_sessions:
        session_flag_dic[d] = 0
    for d in all_buy_sessions:
        session_flag_dic[d] = 1
    for d in all_sessions:
        if idx % 10000 == 0:
            print("processing all_session, idx:", idx)
        # 当前session所有点击商品
        click_items_list = dic1[d]
        for item in click_items_list:
            all_data_items_set.add(item)
        buy_items_list = list()
        if session_flag_dic[d] == 1:
            # 当前session所有购买商品
            buy_items_list = dic2[d]
        click_items_set = set(click_items_list)
        buy_items_set = set(buy_items_list)
        click_not_buy_items_set = click_items_set - buy_items_set
        # 数据格式（每一行）：session;购买items（用逗号隔开）；点击不购买items（用逗号隔开）
        cur_data = [d, buy_items_list, list(click_not_buy_items_set)]
        data.append(cur_data)

    all_data_items = list(all_data_items_set)
    # 输出数据到文件中
    session_item_write_path = write_file_dir + r"\session_item.txt"
    item_write_path = write_file_dir + r"\items.txt"
    p2f.print_data_lists_to_file(data, session_item_write_path)
    p2f.print_list_to_file(all_data_items, item_write_path)


# 提取数据——用于计算相似度
# 这里提取的数据只提取那些有购买且只购买1个商品的session，item的集合也只取这些session里面的,
def extract_real_data2(click_file_path, buys_file_path, write_file_dir):
    print("processing click file...")
    # dic1表示点击数据中，每个session看了哪些商品
    dic1, all_sessions, all_items_set = get_session_itemList(click_file_path)

    print("processing buy file...")
    # 提取购买数据
    # dic2表示购买数据中某个session与"其购买商品的list"的map
    dic2, all_buy_sessions, all_buy_items_set = get_session_itemList(buys_file_path)

    print("extracting session_item_data...")
    # start = time.time()
    # 此处data即为session_item_data
    data = list()
    # 只提取那些“既有点击商品也有点击不购买商品的session”的商品
    all_data_items_set = set()
    # 只考虑那些发生了购买行为的session（且只取其中“购买商品数等于1的session”）
    for d in all_buy_sessions:
        # 当前session所有点击商品
        click_items_list = dic1[d]
        # 当前session所有购买商品
        buy_items_list = dic2[d]
        buy_nums = len(buy_items_list)
        if buy_nums == 1:
            # 只提取那些“有购买且只购买1个商品的session”的商品
            for item in click_items_list:
                all_data_items_set.add(item)
            click_items_set = set(click_items_list)
            buy_items_set = set(buy_items_list)
            click_not_buy_items_set = click_items_set - buy_items_set
            # 数据格式（每一行）：session;购买items（用逗号隔开）；点击不购买items（用逗号隔开）
            cur_data = [d, buy_items_list, list(click_not_buy_items_set)]
            # print("current data: ", cur_data)
            data.append(cur_data)
            # print2file(d, buy_items_list, click_not_buy_items_set)

    all_data_items = list(all_data_items_set)
    # 输出数据到文件中
    session_item_write_path = write_file_dir + r"\session_item.txt"
    item_write_path = write_file_dir + r"\items.txt"
    p2f.print_data_lists_to_file(data, session_item_write_path)
    p2f.print_list_to_file(all_data_items, item_write_path)

    print("finish extracting real data")


# 获取各个session点击/购买的item(item按点击顺序存放)，存放在dic中
# template 2，无需对“最后一个session”的数据进行额外处理的。（适用于“数据从当前行就能获取到”）（template 1：classification/feature4）
# imported by rlso/statistic.py
def get_session_itemList(file_path):

    # dic表示当前数据中某个session与"其商品的list"的map
    dic = dict()
    # 当前数据里所有的session
    sessions = list()
    # 当前数据里所有的item
    items_set = set()
    # 注：不能把open语句放在try块里，因为当打开文件出现异常时，无法执行close()方法。
    f = open(file_path, 'r')
    try:
        idx = 0
        for line in f:
            idx += 1
            if idx % 1000000 == 0:
                print("processing current file, finish line:", idx)
            tmp = line.split(',')
            session_str = tmp[0]
            session = int(session_str)
            item_str = tmp[2]
            item = int(item_str)
            items_set.add(item)

            # 如果sessions为空，即刚开始
            if len(sessions) == 0:
                sessions.append(session)
                dic[session] = list()
                dic[session].append(item)
            # 来了一个新的session
            elif session != sessions[-1]:
                sessions.append(session)
                dic[session] = list()
            # 还是原来的session；或者来了一个新的session
            if item not in dic[session]:
                dic[session].append(item)     # 此处保留记录了各个item在被点击/购买时的位置（购买时一般不明确顺序）

    except Exception as e:
        print(e)
    finally:
        f.close()

    return dic, sessions, items_set


def buy_quantity_statistic(click_file_path, buys_file_path, write_file_dir):
    print("processing click file...")
    dic1, all_sessions, all_items_set = get_session_itemList(click_file_path)

    print("processing click file...")
    item_quantity_dic, all_buy_items_set = extract_buy_quantity(buys_file_path)

    # 购买次数为零的商品——所有"点击过但没被买的item"
    all_clickNotBuy_items_set = all_items_set - all_buy_items_set

    # destination dictionary
    quantity_items_dic = dict()
    for item in item_quantity_dic.keys():
        quantity = item_quantity_dic[item]
        if quantity not in quantity_items_dic.keys():
            quantity_items_dic[quantity] = list()
        quantity_items_dic[quantity].append(item)

    # 找出最大“购买次数”
    max_quantity = 0
    for quantity in quantity_items_dic.keys():
        if quantity > max_quantity:
            max_quantity = quantity

    # buy_quantity_statistic_dic表示商品的购买次数及对应（该购买次数）的商品个数
    buy_quantity_statistic_dic = dict()
    quantity_lists = list()
    # 从小到大输出数据中商品的购买次数及对应（该购买次数）的商品个数
    for i in range(max_quantity+1):
        if i == 0:
            items_num = len(all_clickNotBuy_items_set)
        if i in quantity_items_dic.keys():
            items_num = len(quantity_items_dic[i])
        quantity_lists.append(i)
        buy_quantity_statistic_dic[i] = items_num
        print(i, items_num)

    # 输出到文件中
    write_file_path = write_file_dir + r'\buy_quantity_statistic_dic.txt'
    p2f.print_dict_to_file(buy_quantity_statistic_dic, write_file_path)

    # 画图——似然迭代过程
    print(len(quantity_lists))
    print(len([buy_quantity_statistic_dic[x] for x in quantity_lists]))
    print(quantity_lists)
    print([buy_quantity_statistic_dic[x] for x in quantity_lists])
    part_list = [50, 100, 1000, len(quantity_lists)]
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)
    for part in part_list:
        # 注意这里没有购买次数为零的“商品个数”没有放进去
        left = 0
        right = part
        part_quantity_lists = quantity_lists[left:right]
        plt.sca(ax1)
        plt.plot([quantity_lists[i] for i in range(left, right)],
                 [buy_quantity_statistic_dic[x] for x in part_quantity_lists])
        plt.sca(ax2)
        # 取log的图不考虑"x=0"这个点
        left = 1
        right = part
        part_quantity_lists = quantity_lists[left:right]
        plt.plot([math.log(quantity_lists[i]) for i in range(left, right)],
                 [math.log(buy_quantity_statistic_dic[x]) for x in part_quantity_lists])
        plt.show()


def extract_buy_quantity(file_path):

    # 当前数据里所有的item
    items_set = set()
    # dic统计购买数据中各个item被购买的次数
    dic = dict()
    f = open(file_path, 'r')
    try:
        for line in f:
            tmp = line.split(',')
            item_str = tmp[2]
            item = int(item_str)
            items_set.add(item)
            quantity_str = tmp[4]
            quantity = int(quantity_str)
            if item not in dic.keys():
                dic[item] = quantity
            else:
                dic[item] += quantity
    except Exception as e:
        print(e)
    finally:
        f.close()

    return dic, items_set


if __name__ == '__main__':
    main_dir = r"E:\ranking aggregation\dataset\yoochoose\Full2"
    click_file_path = main_dir + r"\yoochoose-clicks.dat"
    buys_file_path = main_dir + r"\yoochoose-buys.dat"
    write_file_dir = main_dir + r"\extracted2"
    # 假如输出文件夹不存在，则创建文件夹
    if not os.path.exists(write_file_dir):
        os.makedirs(write_file_dir)
    extract_real_data2(click_file_path, buys_file_path, write_file_dir)
    # buy_quantity_statistic(click_file_path, buys_file_path, write_file_dir)
