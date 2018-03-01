#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 读取文件中的信息
# 输入文件格式每行如： 0;1,2,3;4,5,6  (1,2,3或4,5,6可以为空)    (!!注意key和value值均为int型!!)
# 输出格式如： 每行对应一个list: [0,[1,2,3],[4,5,6]]   所有行的数据append后构成一个"data lists"
# 适用于读取session_item_data和item_session_data
def get_data_lists(file_path):
    data_lists = list()
    f = open(file_path)
    try:
        for line in f:
            if line == '\n':
                continue
            # strip('\n')去掉每行行末换行符
            line = line.strip('\n')
            line = line.strip('\r')
            tmp = line.split(';')
            # x 为当前行第一个值
            x_str = tmp[0]
            x = int(x_str)
            # 初始化当前行的数据
            cur_list = [x, [], []]
            x_list1 = cur_list[1]
            x_list2 = cur_list[2]
            # tmp[1] 为当前行第二个值
            if tmp[1] != "":
                tmp1tmp = tmp[1].split(',')
                for elem_str in tmp1tmp:
                    elem = int(elem_str)
                    x_list1.append(elem)
            # tmp[2] 为当前行第三个值
            if tmp[2] != "":
                tmp2tmp = tmp[2].split(',')
                for elem_str in tmp2tmp:
                    elem = int(elem_str)
                    x_list2.append(elem)
            data_lists.append(cur_list)
    except Exception as e:
        print(e)
    finally:
        f.close()
    return data_lists


# 读取文件中的信息
# 输入文件格式每行如： 0;1,2,3;4,5,6  (1,2,3或4,5,6可以为空)   (!!注意key和value值均为int型!!)
# 输出格式如： 一个dic，其中，某一行的数据形如： { 0:[[1,2,3],[4,5,6]] }
# 适用于读取session_item_data和item_session_data
# 这个可以看做函数get_data_lists的升级版
def get_2lists_dict(file_path):
    dic = dict()
    f = open(file_path)
    try:
        for line in f:
            if line == '\n':
                continue
            # strip('\n')去掉每行行末换行符
            line = line.strip('\n')
            line = line.strip('\r')
            tmp = line.split(';')
            # x 为当前行第一个值
            x_str = tmp[0]
            x = int(x_str)
            # 初始化当前行的数据
            cur_list = [[], []]
            x_list1 = cur_list[0]
            x_list2 = cur_list[1]
            # tmp[1] 为当前行第二个值
            if tmp[1] != "":
                tmp1tmp = tmp[1].split(',')
                for elem_str in tmp1tmp:
                    elem = int(elem_str)
                    x_list1.append(elem)
            # tmp[2] 为当前行第三个值
            if tmp[2] != "":
                tmp2tmp = tmp[2].split(',')
                for elem_str in tmp2tmp:
                    elem = int(elem_str)
                    x_list2.append(elem)
            dic[x] = cur_list
    except Exception as e:
        print(e)
    finally:
        f.close()
    return dic


# 读取文件中的信息
# 输入文件格式为一行整数如： 1,2,3,4,5,6      (注意list中元素值为int型)
# 输出格式如： 一个list: [1,2,3,4,5,6]
# 适用于读取items
def get_int_list(file_path):
    ls = list()
    f = open(file_path)
    try:
        line = f.readline()
        # strip('\n')去掉每行行末换行符
        line = line.strip('\n')
        line = line.strip('\r')
        tmp = line.split(',')
        for i in range(len(tmp)):
            val = int(tmp[i])
            ls.append(val)
    except Exception as e:
        print(e)
    finally:
        f.close()
    return ls


# 读取文件中的信息
# 输入文件格式为一行浮点数如： 0.1, 0.2, 0.3, 0.4, 0.5, 0.6      (注意list中元素值为float型)
# 输出格式如： 一个list: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

# 适用于读取likelihood/theta
def get_float_list(file_path):
    ls = list()
    f = open(file_path)
    try:
        line = f.readline()
        # strip('\n')去掉每行行末换行符
        line = line.strip('\n')
        line = line.strip('\r')
        tmp = line.split(',')
        for i in range(len(tmp)):
            val = float(tmp[i])
            ls.append(val)
    except Exception as e:
        print(e)
    finally:
        f.close()
    return ls


# 读取文件中的信息
# 输入文件格式每行如： 2;0.1,0.2,0.3  (注意key值为int型，value值为float型)
# 输出格式如： 一个dic，其中，某一行的数据形如： {2:[0.1, 0.2, 0.3], ...}
# 适用于读取模型参数U和V
def get_float_list_dict(file_path):
    dic = dict()
    f = open(file_path)
    try:
        for line in f:
            if line == '\n':
                continue
            # strip('\n')去掉每行行末换行符
            line = line.strip('\n')
            line = line.strip('\r')
            tmp = line.split(';')
            # 获取dic的key
            x_str = tmp[0]
            x = int(x_str)
            # 获取dic的value(represent by a list)
            cur_list = list()
            if tmp[1] != "":
                tmp1tmp = tmp[1].split(',')
                for elem_str in tmp1tmp:
                    elem = float(elem_str)
                    cur_list.append(elem)
            dic[x] = cur_list
    except Exception as e:
        print(e)
    finally:
        f.close()
    return dic


# 读取文件中的信息
# 输入文件格式每行如： 2;1,2,3  (注意key值为int型，value值为int型)
# 输出格式如： 一个dic，其中，某一行的数据形如： {2:[1,2,3], ...}
# 适用于读取点击流数据，如  7176201;214845127,214849740,214849740
def get_int_list_dict(file_path):
    dic = dict()
    f = open(file_path)
    try:
        for line in f:
            if line == '\n':
                continue
            # strip('\n')去掉每行行末换行符
            line = line.strip('\n')
            line = line.strip('\r')
            tmp = line.split(';')
            # 获取dic的key
            x_str = tmp[0]
            x = int(x_str)
            # 获取dic的value(represent by a list)
            cur_list = list()
            if tmp[1] != "":
                tmp1tmp = tmp[1].split(',')
                for elem_str in tmp1tmp:
                    elem = int(elem_str)
                    cur_list.append(elem)
            dic[x] = cur_list
    except Exception as e:
        print(e)
    finally:
        f.close()
    return dic


if __name__ == '__main__':
    dic = get_2lists_dict(r'E:\ranking aggregation\dataset\yoochoose\Full1\extracted1\session_item_xxxxxxxxxxxxxxxxx.txt')
    print('stop here')
