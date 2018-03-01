#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 将数据输出到文件中


# 输入： "data lists"，如session_item_data与item_session_data
# 输出： 如data lists中的一个list： [0,[1,2,3],[4,5,6]]   输出为文本文件中的一行： 0;1,2,3;4,5,6
def print_data_lists_to_file(data_lists, write_path):

    f = open(write_path, 'w')
    for cur_data_list in data_lists:
        x = cur_data_list[0]
        x_list1 = cur_data_list[1]      # 购买的商品
        x_list2 = cur_data_list[2]      # 点击不购买的商品
        list1_len = len(x_list1)
        list2_len = len(x_list2)
        try:
            f.write(str(x) + ';')
            if list1_len == 0:
                f.write(';')
            else:
                idx = 0
                for list1_elem in x_list1:
                    if idx == list1_len - 1:
                        f.write(str(list1_elem) + ';')
                    else:
                        f.write(str(list1_elem) + ',')
                    idx += 1
            if list2_len == 0:
                pass
            else:
                idx = 0
                for list2_elem in x_list2:
                    if idx == list2_len - 1:
                        f.write(str(list2_elem))
                    else:
                        f.write(str(list2_elem) + ',')
                    idx += 1
        except Exception as e:
            print(e)
        f.write('\n')
    f.close()


# 输入：如data lists中的一个list： [0：[[1,2,3],[4,5,6]], ]
# # 输出：输出为文本文件中的一行： 0;1,2,3;4,5,6
def print_2lists_dict_to_file(dic, write_path):
    # print(11)
    f = open(write_path, 'w')
    try:
        for key in dic.keys():
            f.write(str(key) + ';')
            list1 = dic[key][0]
            for e in list1:
                if e == list1[-1]:
                    f.write(str(e) + ';')
                else:
                    f.write(str(e) + ',')
            list2 = dic[key][1]
            for e in list2:
                if e == list2[-1]:
                    f.write(str(e) + '\n')
                else:
                    f.write(str(e) + ',')
    except Exception as e:
        print(e)
    finally:
        f.close()


# 输入： 一个list，如[1,2,3,4,5]
# 输出： 输出为文本文件中的一行，格式为： 1,2,3,4,5,6
# 如果cur_file_path指定的文件已存在，则会重新生成并覆盖
def print_list_to_file(cur_list, cur_file_path):

    f = open(cur_file_path, 'w')
    try:
        list_len = len(cur_list)
        idx = 0
        for elem in cur_list:
            # 判断elem是否为当前list的最后一个元素
            if idx == list_len - 1:
                f.write(str(elem))
            else:
                f.write(str(elem) + ',')
            idx += 1
    except Exception as e:
        print(e)
    finally:
        f.close()


# 输入： 输入数据格式形如：  {1:1,2:2}
# 输出： 输出形如：   第一行：1;1  第二行：2;2
def print_dict_to_file(dic, file_path):
    f = open(file_path, 'w')
    try:
        for k in dic.keys():
            f.write(str(k) + ';' + str(dic[k]) + "\n")
    except Exception as e:
        print(e)
    finally:
        f.close()


# 输入： 输入数据格式形如：  {1:[0.1,0.1,0.1],2：[0.2,0.2,0.2]}
# 输出： 输出形如：   第一行：1;0.1,0.1,0.1  第二行：2;0.2,0.2,0.2
def print_list_dict_to_file(list_dic, file_path):
    f = open(file_path, 'w')
    try:
        for k in list_dic.keys():
            f.write(str(k) + ';')
            list_len = len(list_dic[k])
            cur_list = list_dic[k]
            idx = 0
            for elem in cur_list:
                # 判断elem是否为当前list的最后一个元素
                if idx == list_len - 1:
                    f.write(str(elem))
                else:
                    f.write(str(elem) + ',')
                idx += 1
            # 换行
            f.write("\n")
    except Exception as e:
        print(e)
    finally:
        f.close()



