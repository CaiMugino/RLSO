#!/usr/bin/env python
# -*- coding:utf-8 -*-

from math import sqrt
import feature4
import read_from_file as rff
import math

# 计算pearson相关系数，验证早购买/晚购买的程度与某一个特征（如item ICR）的关系

def multiply(a,b):
    #a,b两个列表的数据一一对应相乘之后求和
    sum_ab=0.0
    for i in range(len(a)):
        temp=a[i]*b[i]
        sum_ab+=temp
    return sum_ab


def cal_pearson(x,y):
    n=len(x)
    #求x_list、y_list元素之和
    sum_x=sum(x)
    sum_y=sum(y)
    #求x_list、y_list元素乘积之和
    sum_xy=multiply(x,y)
    #求x_list、y_list的平方和
    sum_x2 = sum([pow(i,2) for i in x])
    sum_y2 = sum([pow(j,2) for j in y])
    molecular=sum_xy-(float(sum_x)*float(sum_y)/n)
    #计算Pearson相关系数，molecular为分子，denominator为分母
    denominator=sqrt((sum_x2-float(sum_x**2)/n)*(sum_y2-float(sum_y**2)/n))
    return molecular/denominator


# 计算点二列相关系数
def cal_2pointColumn(x, y):
    p = len(x)/(len(x)+len(y))
    q = len(y)/(len(x)+len(y))
    x_avg = sum(x)/len(x)
    y_avg = sum(y)/len(y)
    all = x + y
    std = calc_standard_deviation(all)
    return (x_avg-y_avg)*math.sqrt(p*q)/std


# 计算标准差
def calc_standard_deviation(x):
    avg = sum(x)/len(x)
    s = 0
    for i in range(len(x)):
        s += math.pow(x[i]-avg, 2)
    return math.sqrt(s/(len(x)-1))


# 提取各个session属于早购买/晚购买的数值表示（用第一个购买商品在session中出现的位置值表示）
def get_session_buyIdx(click_file_path, buy_file_path, data_path):
    # session的购买商品与点击不购买商品
    data = rff.get_2lists_dict(data_path)
    # 提取文件的点击流数据，即各个session的点击流
    session_click_stream = extract_click_stream(click_file_path)
    session_buyIdx_dic = get_session_buyIdx_help(session_click_stream, data)

    return session_buyIdx_dic


# 提取各个session属于早购买/晚购买的数值表示（用第一个购买商品在session中出现的位置值表示）
def get_session_buyIdx_help(session_click_stream, data):
    session_buyIdx_dic = dict()
    for session in session_click_stream.keys():
        click_stream = session_click_stream[session]
        buy_items = data[session][0]
        for i in range(len(click_stream)):
            if click_stream[i] in buy_items:
                # 记录该购买商品在点击流中最早出现的位置
                session_buyIdx_dic[session] = i+1
                break

    return session_buyIdx_dic


# 数据集中各个session属于早购买/晚购买的判断（早购买为1，晚购买为0）
def get_session_ifEarlyBuyFlag(click_file_path, buy_file_path, data_path):
    # session的购买商品与点击不购买商品
    data = rff.get_2lists_dict(data_path)
    # 提取文件的点击流数据，即各个session的点击流
    session_click_stream = extract_click_stream(click_file_path)
    session_ifEarlyBuyFlag_dic = get_session_ifEarlyBuyFlag_help(session_click_stream, data)

    return session_ifEarlyBuyFlag_dic


# 数据集中各个session属于早购买/晚购买的判断（早购买为1，晚购买为0）
def get_session_ifEarlyBuyFlag_help(session_click_stream, data):
    session_ifEarlyBuyFlag_dic = dict()
    for session in session_click_stream.keys():
        # 初始化
        session_ifEarlyBuyFlag_dic[session] = 0
        click_stream = session_click_stream[session]
        buy_items = data[session][0]
        # 判断第一个点击商品是否为购买商品
        if click_stream[0] in buy_items:
            session_ifEarlyBuyFlag_dic[session] = 1

    return session_ifEarlyBuyFlag_dic


# 待考察的特征数据。如对应第一列数据的每个session”第一个点击商品“的item ICR值。
def get_session_ICR(click_file_path, buy_file_path):
    # 获取数据集中所有的item
    item_list = get_item_list(click_file_path)
    # Item conversion rate——{item:ICR}
    item_ICR_dic = feature4.get_item_ICR(click_file_path, buy_file_path, item_list)

    # 每个session”第一个点击商品“的item ICR值
    session_ICR_dic = dict()
    # 提取文件的点击流数据，即各个session的点击流
    session_click_stream = extract_click_stream(click_file_path)
    for session in session_click_stream.keys():
        fisrt_click_item = session_click_stream[session][0]
        ICR = item_ICR_dic[fisrt_click_item]
        session_ICR_dic[session] = ICR

    return session_ICR_dic


# 待考察的特征数据。每个session”第一个点击商品“的的popularity（总点击数）。
def get_session_popularity_click(click_file_path, buy_file_path):
    # 获取数据集中所有的item
    item_list = get_item_list(click_file_path)
    # 表明该商品是否被点击过
    item_flag_dic = dict()
    # 初始化
    for item in item_list:
        item_flag_dic[item] = 0
    # 每个商品被哪些session点击
    item_sessionList_dic1 = feature4.get_item_clicked(click_file_path)
    # 被点击过的商品
    for item in item_sessionList_dic1.keys():
        item_flag_dic[item] = 1
    # 提取文件的点击流数据，即各个session的点击流
    session_click_stream = extract_click_stream(click_file_path)
    session_popularity_dic = dict()
    for session in session_click_stream.keys():
        fisrt_click_item = session_click_stream[session][0]
        if item_flag_dic[fisrt_click_item] == 1:
            # 该商品被哪些session点击
            sessionList = item_sessionList_dic1[fisrt_click_item]
            # 该商品的popularity（总点击数）
            popularity = len(sessionList)
        else:
            # 该商品的popularity（总点击数）
            popularity = 0
        session_popularity_dic[session] = popularity
    return session_popularity_dic


# 待考察的特征数据。每个session”第一个点击商品“的的popularity（总购买数）。
def get_session_popularity_buy(click_file_path, buy_file_path):
    # 获取数据集中所有的item
    item_list = get_item_list(click_file_path)
    # 表明该商品是否被购买过
    item_flag_dic = dict()
    # 初始化
    for item in item_list:
        item_flag_dic[item] = 0
    # 每个商品被哪些session购买
    item_sessionList_dic1 = feature4.get_item_clicked(buy_file_path)
    # 被购买过的商品
    for item in item_sessionList_dic1.keys():
        item_flag_dic[item] = 1
    # 提取文件的点击流数据，即各个session的点击流
    session_click_stream = extract_click_stream(click_file_path)
    session_popularity_dic = dict()
    for session in session_click_stream.keys():
        fisrt_click_item = session_click_stream[session][0]
        if item_flag_dic[fisrt_click_item] == 1:
            # 该商品被哪些session购买
            sessionList = item_sessionList_dic1[fisrt_click_item]
            # 该商品的popularity（总购买数）
            popularity = len(sessionList)
        else:
            # 该商品的popularity（总购买数）
            popularity = 0
        session_popularity_dic[session] = popularity
    return session_popularity_dic


# 待考察的特征数据。每个session的点击流中第一次点击和第二次点击（可能两次点击的是同一个商品）的相差时间。
def get_session_timeDiff(click_file_path, buy_file_path):
    session_timeDiff_dic = dict()
    session_list = list()
    # 计数-计算该session已经点击过多少个商品
    count = 0
    file = open(click_file_path)
    try:
        for line in file:
            tmp = line.split(',')
            session_str = tmp[0]
            session = int(session_str)
            time_str = tmp[1]
            # 取出其中包含时间的部分
            time1_str = time_str[0:19]
            # 第一个session
            if len(session_list) == 0:
                session_list.append(session)
                first_time_str = time1_str
                count = 1
            # 来了一个新的session
            elif session != session_list[-1]:
                session_list.append(session)
                first_time_str = time1_str
                count = 1

            # 还是原来的session；或者来了一个新的session
            if count == 2:
                second_time_str = time1_str
                timeDiff = calcTime(first_time_str, second_time_str)
                session_timeDiff_dic[session] = timeDiff
                count += 1

            if count == 1:
                count = 2

    except Exception as e:
        print(Exception)
    finally:
        file.close()

    return session_timeDiff_dic


# 获取数据集中所有的item
def get_item_list(file_path):
    item_set = set()
    file = open(file_path)
    try:
        for line in file:
            tmp = line.split(',')
            item_str = tmp[2]
            item = int(item_str)
            item_set.add(item)
    except Exception as e:
        print(e)
    finally:
        file.close()
    return list(item_set)


# 提取文件的点击流数据，即各个session的点击流
def extract_click_stream(click_file_path):
    # 提取点击流数据
    dic = dict()
    session_list = list()
    f = open(click_file_path)
    try:
        for line in f:
            tmp = line.split(',')
            session = int(tmp[0])
            item = int(tmp[2])

            # 判断该data session是否出现过
            # 是否为第一个data session
            if len(session_list) == 0:
                session_list.append(session)
                dic[session] = list()
            # 是否来了一个新的session
            elif session != session_list[-1]:
                session_list.append(session)
                dic[session] = list()
            dic[session].append(item)
    except Exception as e:
        print(e)
    finally:
        f.close()
    return dic


# 提取用户计算pearson相关系数的数据（返回结果：两列，用两个list表示）
def get_pearson_data(dic1, dic2):
    list1 = list()
    list2 = list()
    for key in dic1.keys():
        v1 = dic1[key]
        v2 = dic2[key]
        list1.append(v1)
        list2.append(v2)
    return list1, list2


# 提取用于计算点二列相关系数的数据（返回结果：一列是1类对应的数据，一列是0类对应的数据）
def get_2pointColumn_data(dic1, dic2):
    list1 = list()
    list0 = list()
    for key in dic1.keys():
        flag = dic1[key]
        val = dic2[key]
        if flag == 1:
            list1.append(val)
        else:
            list0.append(val)
    return list1, list0


# 第一列的数据：数据集中各个session属于早购买/晚购买的数值表示（用第一个购买商品在session中出现的位置值表示）
# 第二列的数据：待考察的特征数据。待考察的特征数据，对应第一列数据的每个session“第一个点击商品”的某种特征值（如item ICR）。
if __name__ == '__main__':
    # 文件路径
    main_dir = r'E:\ranking aggregation\dataset\yoochoose\Full\extracted'
    click_file_path = main_dir + r'\yoochoose-selected\yoochoose-clicks-selected.dat'
    buy_file_path = main_dir + r'\yoochoose-selected\yoochoose-buys-selected.dat'
    data_path = main_dir + r'\session_item.txt'

    # 第一列的数据：数据集中各个session属于早购买/晚购买的数值表示（用第一个购买商品在session中出现的位置值表示）
    # session_buyIdx_dic = get_session_buyIdx(click_file_path, buy_file_path, data_path)
    # 第一列的数据：数据集中各个session属于早购买/晚购买的判断（早购买为1，晚购买为0）
    session_ifEarlyBuyFlag_dic = get_session_ifEarlyBuyFlag(click_file_path, buy_file_path, data_path)
    # 第二列的数据：待考察的特征数据，对应第一列数据的每个session“第一个点击商品”的某种特征值（如item ICR）。
    # 每个session”第一个点击商品“的item ICR值。
    # session_ICR_dic = get_session_ICR(click_file_path, buy_file_path)
    # 每个session”第一个点击商品“的popularity（总点击数/总购买数）。
    session_popularity_dic = get_session_popularity_click(click_file_path, buy_file_path)
    # session_popularity_dic = get_session_popularity_buy(click_file_path, buy_file_path)
    # 每个session第一个点击和第二个点击商品的相差时间。
    # session_timeDiff_dic = get_session_timeDiff(click_file_path, buy_file_path)

    # 计算pearson相关系数（适用于两列数据都是连续型数值，且都服从正态分布）
    # 提取用于计算pearson相关系数的数据
    # list1, list2 = get_pearson_data(session_buyIdx_dic, session_timeDiff_dic)
    # 测试计算pearson相关系数是否正确(下列测试数据的pearson相关系数为0.9942，正确)
    # list1 = [12.5, 15.3, 23.2, 26.4, 33.5, 34.4, 39.4, 45.2, 55.4, 60.9]
    # list2 = [21.2, 23.9, 32.9, 34.1, 42.5, 43.2, 49.0, 52.8, 59.4, 63.5]
    # 计算pearson相关系数
    # correlation_val = cal_pearson(list1, list2)
    # print(correlation_val)

    # 计算点二列相关系数（适用于一列数据是正态型连续数值，一列数据是二分类数值（该二分类数值非从正态型连续数值变化而来））
    # 提取用于计算点二列相关系数的数据
    list1, list0 = get_2pointColumn_data(session_ifEarlyBuyFlag_dic, session_popularity_dic)
    # 测试计算点二列相关系数是否正确(下列测试数据的点二列相关系数为0.76，正确)
    # list1 = [84, 84, 88, 90, 78, 92, 94, 96, 88, 90]
    # list0 = [82, 76, 60, 72, 74, 76, 80, 78, 76, 74]
    # 计算点二列相关系数
    correlation_val = cal_2pointColumn(list1, list0)
    print(correlation_val)

#from feature5,in order to delete feature5
def calcTime(time1, time2):
    time1 = time.strptime(time1, "%Y-%m-%dT%H:%M:%S")
    time2 = time.strptime(time2, "%Y-%m-%dT%H:%M:%S")
    time1 = datetime.datetime(time1[0], time1[1], time1[2], time1[3], time1[4], time1[5])
    time2 = datetime.datetime(time2[0], time2[1], time2[2], time2[3], time2[4], time2[5])
    return (time2-time1).seconds
