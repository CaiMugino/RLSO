#!/usr/bin/env python
# -*- coding:utf-8 -*-

import print_to_file as p2f

# 新特征的提取
# 改正了其中测试数据两种特征的计算方式（改为利用训练数据的特征计算得到）


class Feature4:

    @staticmethod
    def go(dataset_dir, feature_dir, feature_para=(1, 2, 3, 4)):

        yoochoose_selected_dir = dataset_dir + r'\yoochoose-selected'
        groundtruth_dir = dataset_dir + r'\test'

        click_file_path = yoochoose_selected_dir + r'\yoochoose-clicks-selected.dat'
        buy_file_path = yoochoose_selected_dir + r'\yoochoose-buys-selected.dat'
        test_file_path = yoochoose_selected_dir + r'\yoochoose-test-selected.dat'
        groundtruth_file_path = groundtruth_dir + r'\session_item.txt'

        # data_para_list为1和2分别表示训练数据集和测试数据集的特征输出
        data_para_list = [1, 2, 2]
        # print_para_list为1和0分别表示是、否输出数据的session ID, item ID信息
        print_para_list = [0, 1, 0]

        for i in range(len(data_para_list)):
            data_para = data_para_list[i]
            print_para = print_para_list[i]

            if data_para == 1:
                write_file_path = feature_dir + r'\click-buy-train.arff'
            else:
                if print_para == 1:
                    write_file_path = feature_dir + r'\click-buy-test-BR.txt'
                else:
                    write_file_path = feature_dir + r'\click-buy-test.arff'

            # 获取训练数据和测试数据中所有的item
            item_list = get_item_list(click_file_path, test_file_path)

            # if data_para == 2:
            #     click_file_path = test_file_path
            #     buy_file_path = groundtruth_file_path
            Feature4.print_feature(click_file_path, buy_file_path, test_file_path, groundtruth_file_path, data_para, write_file_path, print_para, item_list, feature_para)

    @staticmethod
    def print_feature(click_file_path, buy_file_path, test_file_path, groundtruth_file_path, data_para, write_file_path, print_para, item_list, feature_para):

        if data_para == 1:
            # 训练数据
            # 用来求每个session长度（不同item，不是按照click算）——{session:item list length}
            session_len_dic = get_session_len(click_file_path)
            # 用来求每个商品在各个session的出现次数——{(item, session):times}
            item_session_times_dic = get_item_session_times(click_file_path)
        else:
            # 测试数据
            session_len_dic = get_session_len(test_file_path)
            item_session_times_dic = get_item_session_times(test_file_path)
        # 接下来的两个特征都是从训练数据提取得到
        # 用来求每个商品被哪些session点击——{item:session list clicked by}——借此可求出：每个商品的总出现session次数
        item_session_dic = get_item_clicked(click_file_path)
        # Item conversion rate——{item:ICR}
        item_ICR_dic = get_item_ICR(click_file_path, buy_file_path, item_list)
        item_len = len(item_list)
        # # 用来求每个item都可以用和它同时出现在一个session里的item表示——{(item, session):occurrence vector}
        # item_session_vector_dic = get_item_session_vector(click_file_path, item_list)
        if data_para == 1:
            # 训练数据的购买数据：每个商品被哪些session购买
            buys_item_sessionList_dic = get_item_clicked(buy_file_path)
        else:
            # 测试数据的购买数据：每个商品被哪些session购买
            buys_item_sessionList_dic = get_test_item_bought(groundtruth_file_path)
        # 将发生了购买行为的(item,session)放入groundtruth_buys中
        groundtruth_buys = list()
        extract_groundtruth(buys_item_sessionList_dic, groundtruth_buys)
        # 输出数据头
        print_head(write_file_path, print_para, item_len, feature_para)
        session_list = list()
        item_set = set()
        data_list = list()
        if data_para == 1:
            file = open(click_file_path)
        else:
            file = open(test_file_path)
        try:
            for line in file:
                tmp = line.split(',')
                session_str = tmp[0]
                session = int(session_str)
                item_str = tmp[2]
                item = int(item_str)
                # 第一个session
                if len(session_list) == 0:
                    session_list.append(session)
                # 来了一个新的session
                elif session != session_list[-1]:
                    session_list.append(session)
                    item_set.clear()
                if item not in item_set:
                    # feature
                    # 每个session长度（不同item，不是按照click算）
                    session_len = session_len_dic[session]
                    # 每个商品的总出现session次数
                    item_all_session_len = len(item_session_dic[item])
                    # 每个商品在当前session的出现次数
                    item_session_times = item_session_times_dic[(item, session)]
                    # vector = item_session_vector_dic[(item, session)]
                    # ICR
                    item_ICR = item_ICR_dic[item]
                    label = 0
                    if (item, session) in groundtruth_buys:
                        label = 1
                    if print_para == 1:
                        data = [session, item]
                    else:
                        data = []
                    # data += vector
                    # 选择使用哪些特征
                    if 1 in feature_para:
                        data.append(item_all_session_len)
                    if 2 in feature_para:
                        data.append(item_session_times)
                    if 3 in feature_para:
                        data.append(session_len)
                    if 4 in feature_para:
                        data.append(item_ICR)
                    data.append(label)
                    # all sample feature
                    data_list.append(data)
                    item_set.add(item)
        except Exception as e:
            print(e)
        finally:
            file.close()
        p2f.print_lists_to_file(data_list, write_file_path)


# 每个session长度（不同item，不是按照click算）
# template 2，需要对“最后一个session”的数据进行额外处理的。（适用于“需要记录一些历史数据的”）(template 1: rlso/real_data)
# imported by rlso/statistic.py
def get_session_len(file_path):
    session_len_dic = dict()
    session_lists = list()
    item_set = set()
    file = open(file_path)
    try:
        for line in file:
            tmp = line.split(',')
            session_str = tmp[0]
            session = int(session_str)
            item_str = tmp[2]
            item = int(item_str)
            # 若session_list为空
            if len(session_lists) == 0:
                session_lists.append(session)
            # 来了一个新的session
            elif session != session_lists[-1]:
                pre_session = session_lists[-1]
                session_len_dic[pre_session] = len(item_set)     # 这里处理的是“上一个session”的数据

                session_lists.append(session)
                item_set.clear()
            # 还是原来的session；或者来了一个新的session（此时item_set已先重置为空）
            item_set.add(item)
        # 最后一个session
        session_len_dic[session] = len(item_set)
    except Exception as e:
        print(e)
    finally:
        file.close()
    return session_len_dic


# 每个商品在各个session的出现次数
def get_item_session_times(file_path):
    item_session_times_dic = dict()
    session_lists = list()
    # 这里的item_set表示每个session所浏览过的所有商品
    item_set = set()
    cur_item_session_dic = dict()
    file = open(file_path)
    try:
        line_idx = 0
        for line in file:
            line_idx += 1
            if line_idx % 1000000 == 0:
                print("processing current file, finish line:", line_idx)
            tmp = line.split(',')
            session_str = tmp[0]
            session = int(session_str)
            item_str = tmp[2]
            item = int(item_str)
            # 第一个session
            if len(session_lists) == 0:
                session_lists.append(session)
            # 来了一个新的session
            elif session != session_lists[-1]:
                pre_session = session_lists[-1]
                for elem in item_set:
                    cur_key = (elem, pre_session)
                    times = len(cur_item_session_dic[elem])
                    item_session_times_dic[cur_key] = times

                session_lists.append(session)
                item_set.clear()
                cur_item_session_dic.clear()
            # 还是原来的session；或者来了一个新的session（此时item_set已先重置为空）
            if item not in item_set:
                item_set.add(item)
                cur_item_session_dic[item] = list()
            cur_item_session_dic[item].append(session)
        # 最后一个session
        for elem in item_set:
            cur_key = (elem, session)
            times = len(cur_item_session_dic[elem])
            item_session_times_dic[cur_key] = times
    except Exception as e:
        print(e)
    finally:
        file.close()
    return item_session_times_dic


# 每个item都可以用和它同时出现在一个session里的item表示——构建一个大向量，表示数据集里所有item，同时在该session中出现的item标为1，否则为0。
def get_item_session_vector(file_path, item_list):
    # 输出 (item,session):item向量
    item_session_vector_dic = dict()
    # 数据集里所有的item
    item_len = len(item_list)
    # 每个session里的item
    item_set = set()
    session_lists = list()
    file = open(file_path)
    try:
        for line in file:
            tmp = line.split(',')
            session_str = tmp[0]
            session = int(session_str)
            if len(session_lists) == 0:
                session_lists.append(session)
            # 来了一个新的session
            elif session != session_lists[-1]:
                pre_session = session_lists[-1]
                for elem in item_set:
                    cur_key = (elem, pre_session)
                    # 初始化vector为全零
                    vector = [0] * item_len
                    for other_item in item_set:
                        if other_item != elem:
                            other_item_index = item_list.index(other_item)
                            vector[other_item_index] = 1
                    item_session_vector_dic[cur_key] = vector

                session_lists.append(session)
                item_set.clear()

            item_str = tmp[2]
            item = int(item_str)
            item_set.add(item)
        # 最后一个session
        for elem in item_set:
            cur_key = (elem, session)
            # 初始化vector为全零
            vector = [0] * item_len
            for other_item in item_set:
                if other_item != elem:
                    other_item_index = item_list.index(other_item)
                    vector[other_item_index] = 1
            item_session_vector_dic[cur_key] = vector
    except Exception as e:
        print(e)
    finally:
        file.close()
    return item_session_vector_dic


def get_item_ICR(click_file_path, buy_file_path, item_list):
    item_ICR_dic = dict()
    # 此处是为了使哪些没被购买的item的ICR有个值
    for item in item_list:
        item_ICR_dic[item] = 0
    # 训练数据的点击数据：每个商品被哪些session点击
    item_sessionList_dic1 = get_item_clicked(click_file_path)
    # 训练数据的购买数据：每个商品被哪些session购买
    item_sessionList_dic2 = get_item_clicked(buy_file_path)
    for item in item_sessionList_dic2.keys():
        click_num = len(item_sessionList_dic1[item])
        buy_num = len(item_sessionList_dic2[item])
        item_ICR_dic[item] = 1.0 * buy_num / click_num
    return item_ICR_dic


# 每个商品被哪些session点击/购买（训练数据每个商品被哪些session点击/购买、测试数据每个商品被哪些session点击）——借此可求出：每个商品的总出现session次数
def get_item_clicked(file_path):
    # 每个商品被哪些session点击/购买
    item_sessionList_dic = dict()
    # 当前文件中的item集合
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
                item_sessionList_dic[item] = list()
                item_sessionList_dic[item].append(session)
            else:
                if session not in item_sessionList_dic[item]:
                    item_sessionList_dic[item].append(session)
            item_set.add(item)
    except Exception as e:
        print(e)
    finally:
        file.close()
    return item_sessionList_dic


# 每个商品被哪些session点击/购买（测试数据每个商品被哪些session购买）——借此可求出：每个商品的总出现session次数
def get_test_item_bought(file_path):
    item_sessionList_dic = dict()
    item_set = set()
    file = open(file_path)
    try:
        for line in file:
            if line == '\n':
                continue
            tmp = line.split(';')
            session_str = tmp[0]
            session = int(session_str)
            items_str = tmp[1]
            tmp1 = items_str.split(',')
            for i in range(len(tmp1)):
                item_str = tmp1[i]
                item = int(item_str)
                if item not in item_set:
                    item_sessionList_dic[item] = list()
                    item_sessionList_dic[item].append(session)
                else:
                    if session not in item_sessionList_dic[item]:
                        item_sessionList_dic[item].append(session)
                item_set.add(item)
    except Exception as e:
        print(e)
    finally:
        file.close()
    return item_sessionList_dic


# 辅助——获取训练集和测试集里所有的item
def get_item_list(file_path1, file_path2):
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
    return item_list


# (item_session_dic:训练/测试数据每个商品被哪些session购买) 从item_session_dic中提取发生购买行为的(item,session)
def extract_groundtruth(item_session_dic, groundtruth_buys):
    for item in item_session_dic.keys():
        for session in item_session_dic[item]:
            cur_buy = (item, session)
            groundtruth_buys.append(cur_buy)


def print_head(file_path, print_para, item_len, feature_para):
    f = open(file_path, 'w')
    try:
        f.write('@relation data' + '\n')
        if print_para == 1:
            f.write('@attribute sessionID integer' + '\n')
            f.write('@attribute itemID integer' + '\n')
        if 1 in feature_para:
            f.write('@attribute item_all_session_len integer' + '\n')
        if 2 in feature_para:
            f.write('@attribute item_session_times integer' + '\n')
        if 3 in feature_para:
            f.write('@attribute session_len integer' + '\n')
        if 4 in feature_para:
            f.write('@attribute item_ICR integer' + '\n')
        # for i in range(item_len):
        #     f.write('@attribute value_' + str(i) + '_of_vector integer\n')

        f.write('@attribute class {1, 0}' + '\n')
        f.write('@data' + '\n')
    except Exception as e:
        print(e)
    finally:
        f.close()


if __name__ == '__main__':
    pass
