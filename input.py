#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import os
import print_to_file as p2f
import read_from_file as rff


class Input:

    @staticmethod
    def get_data(file_dir):

        session_item_file_path = file_dir + r"\session_item.txt"
        item_file_path = file_dir + r"\items.txt"
        # 获取session_item_data和user_session_data(此处data即为session_item_data)
        data, user_sessions_data = get_session_item_and_user_data(session_item_file_path)
        all_data_items = list()
        item_file = open(item_file_path, 'r')
        try:
            line = item_file.readline()
            tmp = line.split(',')
            for item_str in tmp:
                if item_str != '':
                    item = int(item_str)
                    all_data_items.append(item)
        except Exception as e:
            print(e)
        finally:
            item_file.close()
        # 获取item_session_data
        item_session_file_path = file_dir + r"\item_session.txt"
        if os.path.exists(item_session_file_path):
            item_session_data = rff.get_data_lists(item_session_file_path)
        else:
            # 获取item_session_data
            item_session_data = extract_item_data(data, all_data_items)
            # print("item_session_data: ", item_session_data)
            p2f.print_data_lists_to_file(item_session_data, item_session_file_path)
        print("finish get item session data")
        return user_sessions_data, data, item_session_data


# 获取session_item_data和user_session_data
# 注意这里的user_session_data只适用于数据集中只有一个用户情况下
# 这里由于还需要提取user_session_data，故不用get_data_lists函数读取session_item_data
def get_session_item_and_user_data(session_item_file_path):
    data = list()
    user_sessions_data = list()

    session_item_file = open(session_item_file_path, 'r')
    try:
        # 因为当前数据只有一个用户，因此创建一个list，将所有session存放进去
        user1_sessions = list()
        for line in session_item_file:
            if line == '\n':
                print(r"get_session_item_and_user_data: [exception: line == '\n']")
                continue
            tmp = line.split(";")
            session_str = tmp[0]
            session = int(session_str)
            cur_data = [session, [], []]
            buy_items_list = cur_data[1]
            click_not_buy_items_list = cur_data[2]
            # 用户-session信息
            user1_sessions.append(session)
            if tmp[1] != "":
                tmp1 = tmp[1].split(',')
                for buy_item_str in tmp1:
                    buy_item = int(buy_item_str)
                    buy_items_list.append(buy_item)
            if tmp[2] != "":
                tmp2 = tmp[2].split(',')
                for click_not_buy_item_str in tmp2:
                    click_not_buy_item = int(click_not_buy_item_str)
                    click_not_buy_items_list.append(click_not_buy_item)
            data.append(cur_data)
        user_sessions_data.append(user1_sessions)
    except Exception as e:
        print(e)
    finally:
        session_item_file.close()

    print("finish get session item and user data")
    return data, user_sessions_data


# 利用session_item_data和items数据提取item_session_data
def extract_item_data(data, all_data_items):
    # 开始计时
    start = time.time()
    item_session_data = list()
    for item in all_data_items:
        cur_temp = [item, [], []]
        # 当前item被哪个session购买
        cur_temp_buy_session = cur_temp[1]
        # 当前item被哪个session点击但不购买
        cur_temp_clickNotBuy_session = cur_temp[2]
        for cur_data in data:
            cur_d = cur_data[0]
            # 当前session购买了的item
            cur_d_buy_items_list = cur_data[1]
            # 当前session点击但不购买的item
            cur_d_clickNotBuy_items_list = cur_data[2]
            if item in cur_d_buy_items_list:
                cur_temp_buy_session.append(cur_d)
            elif item in cur_d_clickNotBuy_items_list:
                cur_temp_clickNotBuy_session.append(cur_d)
        item_session_data.append(cur_temp)

    c = time.time() - start
    print("extract_item_data耗时:%0.2f" % c, 's')

    return item_session_data


if __name__ == '__main__':
    pass
