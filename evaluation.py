#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 计算评价指标：p@n(n=session中的购买商品数)，MRR

class Evaluation:

    # 根据数据集购买了几个商品，分别计算对应的precision
    @staticmethod
    def calc_precision_at_n(session_item_data, session_item_prob_dic ,n):
        precision = 0.0
        for cur_data in session_item_data:
            session = cur_data[0]
            cur_buy_items = cur_data[1]
            cur_item_prob = session_item_prob_dic[session]
            for i in range(n):
                if cur_item_prob[i][0] in cur_buy_items:
                    precision += 1/n
        precision /= len(session_item_data)
        return precision

    @staticmethod
    def calc_MRR(session_item_data, session_item_prob_dic):
        MRR = calc_MRR_help(session_item_data, session_item_prob_dic)
        return MRR

def calc_MRR_help(session_item_data, session_item_prob_dic):
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