#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import os
from matplotlib import pyplot
from input import Input
import print_to_file as p2f
from rlso import Rlso
import read_from_file as rff
from recommendation import Recommendation
import real_data
import feature4                              # 位于classification文件夹中
from preprocess import Preprocess
import calcCorrelation
import csv
from recommendation_aggregate import Recommendation_aggregate


def TestRLSO():

    # # 模型训练输入例子
    # # 用户、session数据——判断session属于哪个用户
    # user_sessions_data = [[100, 101, 102],]
    # # 每个session购买的商品与点击不购买的商品，按照在数据集中出现的顺序放置
    # session_item_data = [[100, [10, 11], [12, 13]],
    #                      [101, [11, 12], [10, 14]],
    #                      [102, [10, 13, 14], [11, ]]]
    # # 每个商品被哪些session购买以及被哪些session点击但不购买（item_session_data由session_item_data决定）
    # item_session_data = [[10, [100, 102], [101, ]],
    #                      [11, [100, 101], (102, ]],
    #                      [12, [101, ], [100, ]],
    #                      [13, [102, ], [100, ]],
    #                      [14, [102, ], [101, ]]]
    # # parameter：the number of aspects(That's K)
    aspects_num = 5
    # 当前所有已设计的aggregate方法的数目（当改变了aggregate方法时才需设置）
    aggregate_num = 9  ##### aggregate方法的数目 
    # \result\yoochoose\Full\D1_partition\sampling@x@2@partition\train中likelihood.txt，有0-199，
    # \result\yoochoose\Full\D2_partition\sampling@x@2@partition\train 中likelihood.txt，有0-149，
    # 模型训练迭代次数(大约迭代完成次数：D1_partition:200,D2_partition:150,D3_partition:100,D4_partition:100,D5_partition:100,D6_partition:50)
    train_flag = 0 #是否启用训练
    iteration =50
    extract_flag = 0 #训练前是否重新从full data中选择数据


    data_file_dir = '..\\data' #应该是唯一需要修改路径

    # Zero：当前数据样本的训练数据路径（更新上面）
    train_file_dir = data_file_dir + '\\train'
    print('have got the data！！！！！！！！！！！！！')
    # Zero：当前数据样本的训练数据路径（更新上面）
    test_data_dir = data_file_dir +'\\test'

    # Zero：训练出的模型参数的存放路径（更新上面）
    write_file_dir = data_file_dir + '\\result\\TrainedParameters'
    if not os.path.exists(write_file_dir):
          os.makedirs(write_file_dir)
    # Zero：实验结果存放路径（更新上面）
    res_dir = data_file_dir + '\\result\\ExperimentResult'
    if not os.path.exists(res_dir):
                os.makedirs(res_dir)

    #--------------------------- 训练过程（若未有训练好的模型参数文件时，重新训练模型）start----------------------
    # 生成对应数据的点击数据文件（只需生成一次即会保存下来。若已生成，下次可强制关闭，以节省运行时间。）
    if(train_flag):
        if(extract_flag):
            print('注意，已强制关闭extract_yoochoose_selected_data!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('注意，已开启extract_yoochoose_selected_data!!!')
            startExtract = time.time()
            print('extract_yoochoose_selected_data..')
            yoochoose_data_dir = data_file_dir +'\\Full'
            yoochoose_selected_dir= data_file_dir +'\\yoochoose-selected'
            Preprocess.extract_data(train_file_dir, test_data_dir, yoochoose_data_dir, yoochoose_selected_dir)
            endExtract=time.time()
            c1 = endExtract - startExtract
            print('finish extract_yoochoose_selected_data.., runtime is :%0.2f' % c1, 's')
        user_sessions_data, session_item_data, item_session_data = Input.get_data(train_file_dir)
        print('finish getting data')
        print('Starting training~~~~~~')
        print('完整数据中训练数据的session数是：',len(session_item_data))
        # 开始计时
        startRlso = time.time()
        U, V, theta, likelihood = Rlso.go(user_sessions_data, session_item_data, item_session_data, aspects_num, iteration)
        endRlso=time.time()
        c2 = endRlso - startRlso
        print('Rlso 程序运行总耗时:%0.2f' % c2, 's')
        #
        # 假如输出文件夹不存在，则创建文件夹
        if not os.path.exists(write_file_dir):
            os.makedirs(write_file_dir)
        #
        print2file_list = [[theta], likelihood]
        # 输出结果到文件中
        file_name = ['theta.txt', 'likelihood.txt']
        idx = 0
        for cur_list in print2file_list:
                cur_file_path = write_file_dir + '\\' + file_name[idx]
                p2f.print_list_to_file(cur_list, cur_file_path)
                idx += 1
        U_file_path = write_file_dir + '\\' + 'U.txt'
        p2f.print_list_dict_to_file(U, U_file_path)
        print('训练出参数U')
        V_file_path = write_file_dir + '\\' + 'V.txt'
        p2f.print_list_dict_to_file(V, V_file_path)
        print('训练出参数V')
        endTrained = time.time()
        c3 = endTrained - startRlso
        print('参数训练结束，总共耗时:%0.2f' % c3, 's')
        # 画图——似然迭代过程
        pyplot.plot(range(len(likelihood)), likelihood)
        pyplot.show()
    # --------------------------- 训练过程---------------------end------------

    #  write_file_dir：模型参数路径

    # （已经训练好模型）从文件中读取已经训练好的模型参数
    theta_file_path = write_file_dir + '\\' + 'theta.txt'
    [theta] = rff.get_float_list(theta_file_path)   # rff ：read from file
    U_file_path = write_file_dir + '\\' + 'U.txt'
    U = rff.get_float_list_dict(U_file_path)
    V_file_path = write_file_dir + '\\' + 'V.txt'
    V = rff.get_float_list_dict(V_file_path)


    init_flag = 0
    if init_flag == 0:
       init_excel(res_dir, aggregate_num)
    # 表示表格已经初始化一次了，不用再初始化了
       init_flag = 1

    # 非early predict部分的实验（各种种整合策略）
    # 非ealry predict就是我们的论文里面的实验，本来还想做个early predict的东西，但是效果不好，就放弃了
    # Recommendation_aggregate.generate(click_file_path, buy_file_path, test_file_path,
    #                                     U, V, theta, aspects_num, session_item_data, dic, item_session_times_dic,
    #                                      res_dir, part_num, aggregate_num)

    # （非early predict部分的实验（模型原始计算方法））
    # 重复加载一遍下面的数据的原因是Recommendation_aggregate.generate（）方法貌似会对其函数参数造成一定改变，导致后面的程序运行时结果发生
    # （续）一定的改变（已知知道会发生改变）。
    # 测试过程
    # 测试数据
    # test data/groundtruth

    #  test_data_dir = dataset_dir + r'\test' 当前数据样本的测试数据路径
    #  dataset_dir=I:\Papers\consumer\codeandpaper\Full\D1_partition\sampling@x@1@partition
    print('testing~~~~~~')

    test_data_path = test_data_dir + r'\session_item.txt'
    session_item_data = rff.get_data_lists(test_data_path)

    yoochoose_selected_dir = '..\\data\\yoochoose-selected'
    # 测试数据的点击数据文件
    test_file_path = yoochoose_selected_dir + r'\yoochoose-test-selected.dat'
    # 获取测试数据中各个session点击的item(item按点击顺序存放)
    dic, sessions, items_set = real_data.get_session_itemList(test_file_path)
    # 每个商品在各个session的出现次数（原静态特征，点击流场景下不会用到）
    item_session_times_dic = feature4.get_item_session_times(test_file_path)

    # res_path = res_dir + '\\' + dataset_para + '.txt'

    # 非early predict部分的实验（原始方法）

    print('0.01 数据包含的Session 数目：', len(session_item_data))
    startTotal = time.time()

    # def count_Part_num(session_item_data):
    #    for cur_data in session_item_data:
    #
    #       part_num = [len(cur_data[1])]
    #       print('测试数据输出的partnum : ',part_num)
    #       return part_num
    #
    # startPer = time.time()
    #
    Recommendation.generate(U, V, theta, aspects_num, session_item_data, dic, item_session_times_dic,
                               res_dir)
    # endPer = time.time()
    # spendTimePer = endPer - startPer
    # print('跑一个session花费时间:%0.2f' % spendTimePer, 's')
    endTotal = time.time()
    spendTimeTotal = endTotal - startTotal
    print('所有迭代完成总花费时间:%0.2f' % spendTimeTotal, 's')

    # print('完整数据包含的Session 数目：', len(session_item_data))
    # startTotal = time.time()
    # for cur_data in session_item_data:
    #     startPer = time.time()
    #     part_num = len(cur_data[1])
    #     print('测试数据输出的partnum : ', part_num)
    #
    #     Recommendation.generate(U, V, theta, aspects_num, session_item_data, dic, item_session_times_dic,
    #                                res_dir, part_num)
    #     endPer = time.time()
    #     spendTimePer = endPer - startPer
    #     print('迭代一次（每跑一个session）花费时间:%0.2f' % spendTimePer, 's')
    #
    # endTotal = time.time()
    # spendTimeTotal = endTotal - startTotal
    # print('所有迭代完成总花费时间:%0.2f' % spendTimeTotal, 's')

    # def calPart_num(session_item_data):
    #     part_num = 0
    #     for cur_data in session_item_data:
    #         part_num = len(cur_data[1])
    #         print(part_num)
    #         return part_num
    #
    #
    # Recommendation.generate(U, V, theta, aspects_num, session_item_data, dic, item_session_times_dic,
    #                            res_dir,calPart_num(session_item_data))


# 开始时初始化实验结果表格：输出行名、列名等信息
def init_excel(res_dir, aggregate_num):
    # 实验结果路径 res_dir = out_file_dir + '\\' + part_para + r'\experiment result'

    res_file_path = res_dir + r'\SimpleComparison.csv'
    file = open(res_file_path, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(['', 'p1', 'precision', 'MRR'])
    file.close()

    res_file_path = res_dir + r'\Recommendation.csv'
    file = open(res_file_path, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(['', 'calc_item_prob', '', '', '', 'calc_item_prob2', '', '', 'calc_item_prob3'])
    writer.writerow(['sessionID', 'precision', 'MRR', '', 'part_num', 'precision', 'MRR', '', 'precision', 'MRR'])
    file.close()
if __name__ == '__main__':
    TestRLSO()
