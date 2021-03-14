import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

pd.set_option('display.unicode.east_asian_width',True)  #调整“列名与数据的对齐”

config={
    'earn':int(input("请输入单个商品利润："))
    ,'lose':int(input("请输入单个商品成本："))
    ,'days':int(input("请输入计划销售天数："))
    ,'stocking':list(map(int, re.findall(r"\d+",input("请输入想要计算的进货量（可以输入多个，以英文逗号隔开）:"))))
}

def make_profit(stocking=[100,150,200],earn=5,lose=2,days=10):

    df_days = pd.DataFrame(columns=[['',''],["销售天数","单日需求量"]])
    # print(len(stocking))
    j = 0
    df_list = []
    while j < len(stocking):
        df_list.append(pd.DataFrame(
            columns=[['q=' + str(stocking[j]), 'q=' + str(stocking[j]), 'q=' + str(stocking[j])],
                     ["日销量", "日滞销量", "利润"]]))
        j += 1

    i=1
    while i <= days:
        needs = int(random.normalvariate(135,40))  #日销量均值135 日销量标准差40
        df_days.loc[i - 1] = [i, needs]
        j=0
        for df in df_list:
            if needs <= stocking[j]:
                sales = needs
                unsale = stocking[j] - needs
                profit = sales * earn - unsale * lose
            elif needs > stocking[j]:
                sales = stocking[j]
                unsale = 0
                profit = stocking[j] * earn
            df.loc[i -1]=[sales, unsale, profit]
            j+=1
        i += 1

    j=0
    for df in df_list:
        df.loc[days, ('q=' + str(stocking[j]), "日滞销量")]="平均利润"
        df.loc[days, ('q=' + str(stocking[j]), "利润")]=round(df[('q=' + str(stocking[j]), "利润")].mean(),2)
        df.loc[days+1, ('q=' + str(stocking[j]), "日滞销量")] = "波动幅度"
        df.loc[days + 1, ('q=' + str(stocking[j]), "利润")] = round(df[('q=' + str(stocking[j]), "利润")].max()-df[('q=' + str(stocking[j]), "利润")].mean(),2)
        df.loc[days + 2, ('q=' + str(stocking[j]), "日滞销量")] = "亏损概率"
        df.loc[days + 2, ('q=' + str(stocking[j]), "利润")] =str(round((sum(df[('q=' + str(stocking[j]), "利润")]<0)/days)*100,2))+'%'

        j+=1

    df_comeout=df_days
    for df in df_list:
        df_comeout=pd.concat([df_comeout,df],axis=1)
    # print(df_comeout)
    # return df_comeout
    df_comeout.to_excel("进销利润分析.xlsx")


if __name__ ==  '__main__':
    make_profit(**config)







