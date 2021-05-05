import os
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

path=r'C:\Users\Administrator\PycharmProjects\Greedy_Data\BA_kits\综合成本分析_批量递归读取报销数据_绘制柱状图对比分析\source_data'

final_df_data = pd.DataFrame()  #声明一个空数据帧  #声明全局变量，方便递归函数传递数据
handle_file_list = []           #声明一个空列表    #声明全局变量，方便递归函数传递数据

def get_all_file_name(path):
    files = os.listdir(path)
    global final_df_data     #声明全局变量，方便递归函数传递数据
    global handle_file_list  #声明全局变量，方便递归函数传递数据
    for file in files:
        if os.path.isfile(path+"/"+file):
            filename,extension=os.path.splitext(file)
            # print(filename)
            if extension == ".xlsx" and re.findall(r"报销",filename) != [] :
                # print(filename)    #查看文件名
                file_df_data=pd.read_excel(path+'/'+file,parse_dates=['报销日期'])
                # print(file_df_data)  #查看文件内容
                final_df_data = final_df_data.append(file_df_data, ignore_index=True) #合并文件内容
                handle_file_list.append(path+"/"+file)
        elif os.path.isdir(path + "/" + file):   #如果是子目录，就递归调用自身
            get_all_file_name(path + "/" + file) #特别注意：递归函数的处理结果也放在全局变量中（与父函数一样），这就相当于“自动合并了 子函数的解”

    # print(final_df_data)
    # print(handle_file_list)

    return final_df_data,handle_file_list



get_all_file_name(path)
print(final_df_data)
#样例数据：可以看到所有的报销数据 已经都拼接到一个df中了（即final_df_data） //特别注意：其中有些空值是NaN 有些空值是NaT
#                   报销单号       报销日期  报销单位    报销总金额 报销科目    科目金额
# 0   BS_NJ_20210501_001 2021-05-01  机械厂A   4500.0  NaN     NaN
# 1                  NaN        NaT   NaN      NaN   水费  1900.0
# 2                  NaN        NaT   NaN      NaN   电费  2600.0
# 3   BS_NJ_20210501_002 2021-05-02  机械厂A   6000.0  NaN     NaN
# 4                  NaN        NaT   NaN      NaN  原材料  6000.0
# 5   BS_NJ_20210501_003 2021-05-03  机械厂A  10000.0  NaN     NaN
# 6                  NaN        NaT   NaN      NaN  运输费  3000.0
# 7                  NaN        NaT   NaN      NaN  维护费  7000.0

# print(final_df_data.info())  #查看各个字段的数据类型
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 21 entries, 0 to 20
# Data columns (total 6 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   报销单号    6 non-null      object
#  1   报销日期    6 non-null      datetime64[ns]     //特别注意：时间数据类型 能够自动匹配出来
#  2   报销单位    6 non-null      object
#  3   报销总金额   6 non-null      float64
#  4   报销科目    15 non-null     object
#  5   科目金额    15 non-null     float64
# dtypes: datetime64[ns](1), float64(2), object(3)
# memory usage: 1.1+ KB
# None
print(handle_file_list)



def fill_nan_line(df_cost):   #实现 “半空行”的智能填充
    head_line=df_cost.loc[0]  #head_line是“同组半空行”的“同组首行” //“同组首行”一定不是“半空行”（由报销表的特点决定） //df_cost的首行 就是“首组的同组首行”
    # print(head_line)
    index_list=['报销单号','报销日期','报销单位']  #这三个字段都为“空”的行 就是“半空行”
    for indexs in df_cost.index:       #遍历df_cost的每一行
        line_data=df_cost.loc[indexs]  #提取df_cost的一行数据
        # print(line_data)
        # print(type(line_data))  #<class 'pandas.core.series.Series'>
        # print(line_data['报销单号'])  #样例数据1：BS_NJ_20210501_001        #样例数据2：nan 即 空值
        # print(line_data['报销日期'])  #样例数据1：2021-05-01 00:00:00       #样例数据2：Nat 即 空值
        # print(line_data['报销单位'])  #样例数据1：机械厂A                    #样例数据2：nan 即 空值
        # print(line_data['报销单号'] is np.NaN)  #样例数据1：False           #样例数据2：True
        # print(line_data['报销日期'] is np.NaN)  #样例数据1：False           #样例数据2：False  //有问题：空值判断失败
        # print(line_data['报销日期'] is pd.NaT)  #样例数据1：False           #样例数据2：True   //此时，空值判断成功 //特别注意：df中的nan与nat是不同类型的空值，貌似nat是“时间类型数据的空值”
        # print(line_data['报销单位'] is np.nan)  #样例数据1：False           #样例数据2：True
        if line_data['报销单号'] is np.nan and line_data['报销单位'] is np.nan and line_data['报销日期'] is pd.NaT: #这三个字段都是空值的行，就是“半空行”。“半空行”从“同组首行”的相应字段中，复制数据
            # print(line_data)
            for i in index_list:
                df_cost.loc[indexs,i]=head_line[i]
        else:  #不是“半空行”，就是“同组首行”
            head_line=line_data  #将“同组首行”的数据保存在head_line中

    df_cost['报销日期']=df_cost['报销日期'].astype("str")  #如果“时间类型数据”不做类型转换的话，数据写入Excel之后 Excel会自动加上“时分秒”（都是0 不好看）
    # print(df_cost)
    df_cost.to_excel(r'C:\Users\Administrator\PycharmProjects\Greedy_Data\BA_kits\综合成本分析_批量递归读取报销数据_绘制柱状图对比分析\报销汇总.xlsx',index=False)

    return df_cost

df_cost=fill_nan_line(final_df_data)
print(df_cost) #查看：样例数据，可以看到“半空行”都被“智能填充”了（注意：报销单号 报销日期 报销单位，这三个字段）  //此时，就能做groupby聚合计算（关于 报销单位 这个字段，进行分组）
#                   报销单号        报销日期  报销单位    报销总金额 报销科目    科目金额
# 0   BS_NJ_20210501_001  2021-05-01  机械厂A   4500.0  NaN     NaN
# 1   BS_NJ_20210501_001  2021-05-01  机械厂A      NaN   水费  1900.0
# 2   BS_NJ_20210501_001  2021-05-01  机械厂A      NaN   电费  2600.0
# 3   BS_NJ_20210501_002  2021-05-02  机械厂A   6000.0  NaN     NaN
# 4   BS_NJ_20210501_002  2021-05-02  机械厂A      NaN  原材料  6000.0
# 5   BS_NJ_20210501_003  2021-05-03  机械厂A  10000.0  NaN     NaN
# 6   BS_NJ_20210501_003  2021-05-03  机械厂A      NaN  运输费  3000.0
# 7   BS_NJ_20210501_003  2021-05-03  机械厂A      NaN  维护费  7000.0
# 8   BS_SZ_20210501_001  2021-05-01  电子厂A   6000.0  NaN     NaN

print("===========================================================================================")
#将单柱图的绘制过程 封装为 单柱绘制函数

print(list(df_cost.groupby("报销单位")))  #查看“数据行”的分组情况：元素是元组，"报销单位"的一个取值 和 该取值的所有行（即一个“子df”）
# [('机械厂A',                  报销单号        报销日期  报销单位    报销总金额 报销科目    科目金额
# 0  BS_NJ_20210501_001  2021-05-01  机械厂A   4500.0  NaN     NaN
# 1  BS_NJ_20210501_001  2021-05-01  机械厂A      NaN   水费  1900.0
# 2  BS_NJ_20210501_001  2021-05-01  机械厂A      NaN   电费  2600.0
# 3  BS_NJ_20210501_002  2021-05-02  机械厂A   6000.0  NaN     NaN
# 4  BS_NJ_20210501_002  2021-05-02  机械厂A      NaN  原材料  6000.0
# 5  BS_NJ_20210501_003  2021-05-03  机械厂A  10000.0  NaN     NaN
# 6  BS_NJ_20210501_003  2021-05-03  机械厂A      NaN  运输费  3000.0
# 7  BS_NJ_20210501_003  2021-05-03  机械厂A      NaN  维护费  7000.0), ('电子厂A',                   报销单号        报销日期  报销单位   报销总金额 报销科目    科目金额
# 8   BS_SZ_20210501_001  2021-05-01  电子厂A  6000.0  NaN     NaN
# 9   BS_SZ_20210501_001  2021-05-01  电子厂A     NaN   水费  1000.0
# 10  BS_SZ_20210501_001  2021-05-01  电子厂A     NaN   电费  2000.0
# 11  BS_SZ_20210501_001  2021-05-01  电子厂A     NaN  原材料  3000.0
# 18  BS_SZ_20210501_003  2021-05-02  电子厂A  7000.0  NaN     NaN
# 19  BS_SZ_20210501_003  2021-05-02  电子厂A     NaN  运输费  2000.0
# 20  BS_SZ_20210501_003  2021-05-02  电子厂A     NaN  维护费  5000.0), ('芯片厂A',                   报销单号        报销日期  报销单位    报销总金额 报销科目    科目金额
# 12  BS_SZ_20210501_002  2021-05-01  芯片厂A  13500.0  NaN     NaN
# 13  BS_SZ_20210501_002  2021-05-01  芯片厂A      NaN   水费  1100.0
# 14  BS_SZ_20210501_002  2021-05-01  芯片厂A      NaN   电费  2100.0
# 15  BS_SZ_20210501_002  2021-05-01  芯片厂A      NaN  原材料  3100.0
# 16  BS_SZ_20210501_002  2021-05-01  芯片厂A      NaN  运输费  2100.0
# 17  BS_SZ_20210501_002  2021-05-01  芯片厂A      NaN  维护费  5100.0)]
print(df_cost.groupby("报销单位").agg('sum'))
#         报销总金额     科目金额
# 报销单位
# 机械厂A  20500.0  20500.0
# 电子厂A  13000.0  13000.0
# 芯片厂A  13500.0  13500.0
print(type(df_cost.groupby("报销单位").agg('sum')))
#<class 'pandas.core.frame.DataFrame'>
#我对df的groupby聚合计算的理解：groupby('x')指定'x'为分组字段，agg('y')指定计算方法'y'
#                          df.groupby('x').agg('y'))生成一个“新的数据帧”：新的数据帧的index为'x'，并对 所有数值字段 做'y'计算，并“丢弃”原df的所有非数值字段


print(df_cost.groupby("报销单位").agg('sum')['报销总金额'])  #“投影”所需要的数值字段
# 报销单位
# 机械厂A    20500.0
# 电子厂A    13000.0
# 芯片厂A    13500.0
# Name: 报销总金额, dtype: float64
print(type(df_cost.groupby("报销单位").agg('sum')['报销总金额']))
# <class 'pandas.core.series.Series'>

s1=df_cost.groupby("报销单位").agg('sum')['报销总金额']
print(s1.index)       #Series的索引数据 #样例数据：Index(['机械厂A', '电子厂A', '芯片厂A'], dtype='object', name='报销单位')
print(list(s1.index)) #将Series索引转换为列表：['机械厂A', '电子厂A', '芯片厂A']
print(s1.values)      #Series的数值数据#样例数据：[20500. 13000. 13500.]
print(list(s1.values))#将Series将值转换成列表：[20500.0, 13000.0, 13500.0] //特别注意：这里的两个列表，元素是有“顺序对应”的

#将 绘制单柱的过程，封装为一个函数 即 单柱绘制函数  //提高 可复制性、可读性
def single_bar(x_data,y_data,fig_title,xlabel,ylabel): #x_data表示 x轴的取值列表，y_data表示 y轴的取值列表，fig_title表示 全图标签，xlabel表示 x轴标签，ylabel表示 y轴标签
    font = {
        "family": "SimHei"  # 设置中文字体          //注意：很多参数没有放到形参中（形参太多 可能会增加"使用复杂性"），在函数内部手动（复制）调整
        , "size": "20"  # 设置字体大小
    }
    plt.rc("font", **font)#因为 接下来要在图上显示汉字，所以设置中文显示
    plt.figure(figsize=(20,10))       #设置画布大小
    plt.bar(x_data,y_data,width=0.5)  #width指定 柱子的宽度
                                      #特别注意：x_data、y_data的实参 都必须是“可迭代对象”！ 因为 一张“单柱图”也需要 多个x、y坐标 来绘制 多个柱子！
                                      #虽然 叫“单柱图”，图上不止画一根柱子！之所以 叫“单柱图” 是因为图看起来“一个x轴对象 对应 一个根柱子”，而 图上一般有多个“x轴对象” 所以一口气要画多个“柱子”！

    ax=plt.gca() #gca方法返回边框对象 #通过 边框对象，设置一下三个标签
    ax.set_title(fig_title)  #图片标签（即 解释图片的含义）
    ax.set_xlabel(xlabel)    #X轴标签（即 解释x轴的含义）
    ax.set_ylabel(ylabel)    #Y轴标签（即 解释y轴的含义）

    # print(list(zip(x_data, y_data)))#样例数据：[('原材料', 13200.0), ('水费', 4500.0), ('电费', 6700.0), ('维护费', 17100.0), ('运输费', 7700.0)]
    for x, y in zip(x_data, y_data):  # 每个柱子的标签（即 解释柱子的含义）
        plt.text(x,y+20,"%.0f" % y,ha='center',va='bottom')  #ha有三个选择：right,center,left #va有四个选择：'top', 'bottom', 'center', 'baseline'
    #我对柱子标签的理解：第一、第二参数 确定“标签的坐标”（其实，柱状图就是根据这个“坐标”绘制的） //特别注意：y+20相当于将“文本的垂直坐标值”增加了20，目的是为了“显示效果（也可以设置为+200，理解该效果）”（与ha、va参数一同参与“定位”）
    #
    #                第三参数 指定“标签的文本内容”（柱子的底部 柱状图默认就会“显示x坐标”，“标签的文本内容”其实就是显示“柱顶y坐标”） //特别注意：x轴有可能是离散取值的，而y轴一般是数值取值的
    #                第四、五参数 指定“标签的位置”（我的理解：是相对于“标签的坐标”的位置）

    plt.show()

single_bar(list(s1.index),list(s1.values),fig_title="三家工厂的总成本的对比",xlabel="工厂",ylabel="成本") #调用“单柱绘制函数”


print(df_cost.groupby("报销科目").agg('sum')['科目金额'])
# 报销科目
# 原材料    13200.0
# 水费      4500.0
# 电费      6700.0
# 维护费    17100.0
# 运输费     7700.0
# Name: 科目金额, dtype: float64
s2=df_cost.groupby("报销科目").agg('sum')['科目金额']
print(s2.index)
print(list(s2.index))
print(s2.values)
print(list(s2.values))

single_bar(list(s2.index),list(s2.values),fig_title="各种科目的总成本的对比",xlabel="科目",ylabel="成本") #调用“单柱绘制函数”

print("===========================================================================================")
#将多柱图（分组柱图）的绘制过程 封装为 多柱（分组柱图）绘制函数
#从下面函数的定义就能看出：多柱图（分组柱图）的绘制 要比 单柱图 复杂得多
#简单讲：多柱图（分组柱图）就是 一个x_data(列表) 对齐 多个y_data(列表)  //单柱图，是 一个x_data(列表) 对齐 一个y_data(列表)
#      在绘制多柱图（分组柱图）之前的 数据预处理部分，就是为了实现“一个x_data(列表) 对齐 多个y_data(列表)”！

#要对比 每家工厂的各种科目的费用，就需要 使用多柱图（分组柱图） //一家工厂 对应 一组柱子
# print(list(df_cost.groupby(["报销单位","报销科目"])))                 #对两个字段进行分组
# print(df_cost.groupby(["报销单位","报销科目"]).agg("sum")['科目金额'])  #进行聚合计算之后，再投影
# 报销单位  报销科目
# 机械厂A  原材料     6000.0
#       水费      1900.0
#       电费      2600.0
#       维护费     7000.0
#       运输费     3000.0
# 汽车厂A  原材料     3000.0    #注意：汽车厂A的报销科目 只有3项
#       水费      1000.0
#       电费      2000.0
# 电子厂A  原材料     3000.0
#       水费      1500.0
#       电费      2000.0
#       维护费     5000.0
#       运输费     2000.0
# 芯片厂A  原材料     4200.0
#       水费      1100.0
#       电费      2100.0
#       维护费     5100.0
#       运输费     2700.0
# Name: 科目金额, dtype: float64
s3=df_cost.groupby(["报销单位","报销科目"]).agg("sum")['科目金额'] #s3就是 上面的 这个“复合index”的Series
print("s3.index:\n",s3.index)
# MultiIndex([('机械厂A', '原材料'),
#             ('机械厂A',  '水费'),
#             ('机械厂A',  '电费'),
#             ('机械厂A', '维护费'),
#             ('机械厂A', '运输费'),
#             ('汽车厂A', '原材料'),
#             ('汽车厂A',  '水费'),
#             ('汽车厂A',  '电费'),
#             ('电子厂A', '原材料'),
#             ('电子厂A',  '水费'),
#             ('电子厂A',  '电费'),
#             ('电子厂A', '维护费'),
#             ('电子厂A', '运输费'),
#             ('芯片厂A', '原材料'),
#             ('芯片厂A',  '水费'),
#             ('芯片厂A',  '电费'),
#             ('芯片厂A', '维护费'),
#             ('芯片厂A', '运输费')],
#            names=['报销单位', '报销科目'])



def preprocess_multi_bar(s):  #多柱（分组柱图）_预处理函数 #作用：各个科目的金额数据（列表）按照工厂名“对齐”  #形参s 表示“上述分组聚合的投影” 比如上文中的s3
    factory_name=set()
    subject_name=set()

    for x,y in s.index:       #解析出 “复合index”中，第一维index的取值种类 和 第二维index的取值种类  //注意：set数据类型 天然具有去重的功能
        factory_name.add(x)
        subject_name.add(y)

    # print(sorted(factory_name)) #['机械厂A', '汽车厂A', '电子厂A', '芯片厂A']   //set数据类型 不是“稳定的”，即每次运行 元素排序可能不同！这对下一步的数据处理 会造成不利的影响！
    # print(sorted(subject_name)) #['原材料', '水费', '电费', '维护费', '运输费'] //所以，将set的数据进行排序，这样 每次运行 再排序 得到的列表的元素 排序是相同的！有利于 下一步的处理（绘图的时候 要对柱子的含义 进行中文解释，所以 科目的排序 必须固定）！



    s_value_1=[] #原材料
    s_value_2=[] #水费
    s_value_3=[] #电费
    s_value_4=[] #维护费
    s_value_5=[] #运输费

    for i in sorted(factory_name):     #外循环：根据 排序的工厂名 进行遍历
        # print(i)  #样例数据：机械厂A
        dim = 1   #变量dim
        for j in sorted(subject_name): #内循环：根据 排序的科目名 进行遍历
            if (i,j) not in s.index:   #如果，工厂名、科目名的组合 不存在（因为，没有金额数据），就将 该组合的金额数据 置为0
                s[i,j]=0               #如果 不这么做的话，各科目的数据 有可能 没有办法“按照工厂名 对齐”，也就 不利于 多柱（分组柱图）图的绘制！
            # print(j) #样例数据：原材料
            # print(s[i,j])  #样例数据：6000.0
            if dim == 1 :   #表示 科目1 即 原材料s_value_1
                s_value_1.append(s[i,j])
            elif dim == 2:  #表示 科目2 即 水费s_value_2
                s_value_2.append(s[i, j])
            elif dim == 3:  #表示 科目3 即 电费s_value_3
                s_value_3.append(s[i, j])
            elif dim == 4:  #表示 科目4 即 维护费s_value_4
                s_value_4.append(s[i, j])
            elif dim == 5:  #表示 科目5 即 运输费s_value_5
                s_value_5.append(s[i, j])
            dim+=1
        # print()
    return sorted(factory_name), sorted(subject_name), [s_value_1, s_value_2, s_value_3, s_value_4, s_value_5]  #将可以 各个科目的数据 打包成一个二维列表 返回

s_factory_name,s_subject_name,s_value=preprocess_multi_bar(s3)
# print(s_factory_name) #['机械厂A', '汽车厂A', '电子厂A', '芯片厂A']
# print(s_subject_name) #['原材料', '水费', '电费', '维护费', '运输费']
# print(s_value)
# #[[6000.0, 3000.0, 3000.0, 4200.0], [1900.0, 1000.0, 1500.0, 1100.0], [2600.0, 2000.0, 2000.0, 2100.0], [7000.0, 0.0, 5000.0, 5100.0], [3000.0, 0.0, 2000.0, 2700.0]]
# print(s_value[0]) #[6000.0, 3000.0, 3000.0, 4200.0]
# print(s_value[1]) #[1900.0, 1000.0, 1500.0, 1100.0]
# print(s_value[2]) #[2600.0, 2000.0, 2000.0, 2100.0]
# print(s_value[3]) #[7000.0, 0.0, 5000.0, 5100.0]   #可以看到，通过 补0 对齐了
# print(s_value[4]) #[3000.0, 0.0, 2000.0, 2700.0]   #可以看到，通过 补0 对齐了
#可以看到：5个科目的数据，都按照“工厂名的顺序 对齐排序”了


def multi_bar(s_factory_name,s_subject_name,s_value):
    font = {
        "family": "SimHei"  # 设置中文字体   //注意：很多参数没有放到形参中（形参太多 可能会增加"使用复杂性"），在函数内部手动（复制）调整
        , "size": "20"      # 设置字体大小
    }
    plt.rc("font", **font)  # 因为 接下来要在图上显示汉字，所以设置中文显示

    width=0.1 #柱子宽度
    plt.figure(figsize=(20,10))
    x_data=s_factory_name
    xticks = np.arange(len(s_factory_name)) #以工厂名的个数 来生成ndarray  //特别注意：单柱图绘制函数（见上文）没有使用ndarray，而是直接使用x_data给plt.bar的第一个参数赋值
    print(xticks)       #[0 1 2 3]                                     //        多柱图绘制函数，之所以要使用ndarray，是因为“多柱（分组柱）” 需要偏移来实现（见下文），而偏移一般都是基于“数值”实现的
    print(type(xticks)) #<class 'numpy.ndarray'>
    print(xticks+0.2)   #[0.2 1.2 2.2 3.2]
    rects_dict={} #用一个字典 来保存 柱状图对象，在绘制柱顶标签（一般都是“数值”）的时候 需要使用
    i,j=0,0
    for na in s_subject_name: #根据科目名称 生成相应的柱状图
        rects_dict[i]=plt.bar(xticks+width*j, s_value[i], width=width,label=na)  #特别注意：xticks+width*j 表示每一轮“单柱图绘制”的时候，x轴坐标向右偏移“一个 柱子宽度”
        i+=1
        j+=1
    #我的理解：多柱图（分组柱图），其实 就在一张画布上 调用多轮“单柱图绘制”，而且 每次画柱状图的时候“x轴的偏移量正好就是柱子的宽度”
    #        所以 看起来，一组有多个柱子 多个柱子贴在一起！  //这样，图看起来就是“一个x轴对象 对应 多根（后者说）一组柱子”
    #        注意：这里plt.bar的第一个实参、第二个实参 依然要求都是可迭代对象，因为 一张“单柱图”也需要 多个x、y坐标 来绘制 多个柱子！

    print("rects_dict:",rects_dict)
    # {0: <BarContainer object of 4 artists>, 1: <BarContainer object of 4 artists>, 2: <BarContainer object of 4 artists>, 3: <BarContainer object of 4 artists>, 4: <BarContainer object of 4 artists>}

    ax=plt.gca()
    ax.set_xticks(xticks + 0.25) #设置“组名”偏移量，“组名”在x轴的所在位置 也应该在“一组柱子”之下
    ax.set_xticklabels(x_data)   #注销该行的话，打印出来的图 每组的“组名”就不是工厂名了，而是数字
    ax.legend(fontsize=10)       #通过“颜色”解释“各个分组的含义”  //特别注意：ax.legend() 是基于plt.bar()中的label参数实现的。如果plt.bar()没有设置label参数 则ax.legend()在图像“显示为空”
                                 #我的理解：ax.legend()的原理，就是“打印”plt.bar()的颜色与label对应关系  //颜色是会自动赋值的
    ax.set_title("三家工厂成本细分到各个科目的对比")
    ax.set_xlabel("工厂")
    ax.set_ylabel("成本")

    def set_label(rects):  #通过 子函数 实现：多柱图（分组柱图）的柱顶标签  #形参rects表示 “单柱图”的对象
        for rect in rects: #我的理解：“单柱图”的对象 也是一个可迭代对象，我猜 就是在迭代 一个个x、y坐标点（或者别的什么数据）
            height = rect.get_height() #获取高度   //一个rect 就是 一轮绘制“单柱图”对象中的 其中一次迭代（一组数据）
            plt.text(x = rect.get_x() + rect.get_width()/2, #水平坐标
                     y = height + 0.5, #数值坐标
                     s = "%.0f" % height, #文本内容（“数值”）
                     ha = 'center',
                     va = 'bottom')

    for key in rects_dict.keys():
        set_label(rects_dict[key]) #字典中的一个元素 就是 一轮绘制“单柱图”的对象
    #我理解：柱状图是一轮一轮画的，柱顶标签（数值） 也是一轮一轮打的！

    plt.show()

multi_bar(s_factory_name,s_subject_name,s_value)

