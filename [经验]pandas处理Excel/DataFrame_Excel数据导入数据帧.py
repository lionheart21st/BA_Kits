import pandas as pd

pd.set_option('display.unicode.east_asian_width',True)  #调整“列名与数据的对齐”


df_excel=pd.read_excel(io="./实验数据/excel_data_1.xlsx") #默认导入第一页'Sheet1'  #形参1 io 文件路径文件名(一般都使用位置参数)
print(df_excel.head(3))
#    日期1  总销售额1  FBA销售额1  自配送销售额1
# 0  42964    3211.87     1596.16        1615.71
# 1  42965    3376.35     1777.65        1598.70
# 2  42966    3651.55     2304.97        1239.75

print(type(df_excel)) #<class 'pandas.core.frame.DataFrame'>


df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",sheet_name='Sheet2')   #形参2 sheet_name(一般第二个参数 都使用关键字参数，该函数的参数非常多)
print(df_excel.head(3))
#    日期2  总销售额2  FBA销售额2  自配送销售额2           //从字段可以看出来，这是Sheet2的数据
# 0  42964    3211.87     1596.16        1615.71
# 1  42965    3376.35     1777.65        1598.70
# 2  42966    3651.55     2304.97        1239.75

df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",sheet_name=0)   #形参sheet_name也可以用数值赋值(相当于位置参数）0表示第一页
print(df_excel.head(3))
#    日期1  总销售额1  FBA销售额1  自配送销售额1
# 0  42964    3211.87     1596.16        1615.71
# 1  42965    3376.35     1777.65        1598.70
# 2  42966    3651.55     2304.97        1239.75

df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",sheet_name=[0,1])  #用列表给sheet_name赋值（使用的是“位置索引”），该列表元素作为“返回值（字典）的key” 我称之为“页索引”
print(type(df_excel))      #<class 'dict'>   #特别注意：读取单页数据 返回值类型是DataFrame，读取多页数据 返回值类型是dict 其中“页索引”是key 相应的数据帧DataFrame是key对应的value
print(type(df_excel[0]))   #<class 'pandas.core.frame.DataFrame'>  #字典通过key访问元素dict[key]
print(df_excel[1].head(3)) #读取第二页数据
#    日期2  总销售额2  FBA销售额2  自配送销售额2
# 0  42964    3211.87     1596.16        1615.71
# 1  42965    3376.35     1777.65        1598.70
# 2  42966    3651.55     2304.97        1239.75

df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",sheet_name=['Sheet1','Sheet2'])  #用列表给sheet_name赋值（使用的是“名称索引”），该列表元素作为“返回值（字典）的key”
print(type(df_excel))             #<class 'dict'>
print(type(df_excel['Sheet1']))   #<class 'pandas.core.frame.DataFrame'>  #字典通过key访问元素dict[key]
print(df_excel['Sheet2'].head(3)) #读取第二页数据
#    日期2  总销售额2  FBA销售额2  自配送销售额2
# 0  42964    3211.87     1596.16        1615.71
# 1  42965    3376.35     1777.65        1598.70
# 2  42966    3651.55     2304.97        1239.75
# df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",sheet_name=[0,'Sheet2'])  #效果同上  //“页索引”可以是 位置索引 与 名称索引的 混合
# print(df_excel['Sheet2'].head(3))

df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",sheet_name=None) #None赋值给sheet_name表示读取所有页
print(df_excel.keys()) #dict_keys(['Sheet1', 'Sheet2']) 可以看到确实是读取了所有页



df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",header=0)  #参数header是表头的意思，就是“字段行（我自己的命名）”  #header的默认值就是0（位置索引）
print(df_excel.head(3))
#    日期1  总销售额1  FBA销售额1  自配送销售额1
# 0  42964    3211.87     1596.16        1615.71
# 1  42965    3376.35     1777.65        1598.70
# 2  42966    3651.55     2304.97        1239.75


df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name=0,header=1) #sheet_name=0表示第一页，header=1表示 指定第二行为表头
print(df_excel.head(3))
#  日期11  总销售额11  FBA销售额11  自配送销售额11          //可以看到 成功读取表头
# 0  42964    3211.87     1596.16        1615.71
# 1  42965    3376.35     1777.65        1598.70
# 2  42966    3651.55     2304.97        1239.75


df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name=0,header=0) #sheet_name=1表示第二页，header=0表示 指定第一行为表头
print(df_excel.head(3))
#   Unnamed: 0 Unnamed: 1  Unnamed: 2     Unnamed: 3       #可以看到：这个表头读取失败了  //因为，这个sheet页 第一行是空的
# 0      日期11  总销售额11  FBA销售额11  自配送销售额11         #把“真正的表头”当做数据读取了
# 1      42964    3211.87     1596.16        1615.71
# 2      42965    3376.35     1777.65         1598.7
###特别注意：header表头参数是使用位置索引（自动索引）来定位“第几行”的，不要受“Excel行标（即Excel软件中的行号）“的影响！
###我的理解：header表头参数所指定的行，读取的数据 作为DataFrame数据帧的columns“列索引”（而不是作为数据）。
###        DataFrame数据帧 哪一行才是真正的数据的：行索引 位置索引为0的行！


#据说：如果，一个sheet页 开头空了几行 并且 是有表头的，header默认 是可以“自动定位”到表头所在行的。//进过实验证明：默认是没有“自动定位”功能的，但 配合skiprows 会自动定位“剩余行”的第一行！见下文
df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name=0) #使用header的默认
print(df_excel.head(3))  #但是，我的实验结果 说明：不存在“header默认能够自动定位表头”
#   Unnamed: 0  Unnamed: 1   Unnamed: 2      Unnamed: 3
# 0     日期11  总销售额11  FBA销售额11  自配送销售额11
# 1      42964     3211.87      1596.16         1615.71
# 2      42965     3376.35      1777.65          1598.7


#特别注意：有的sheet页是没有表头（“字段行”）的
df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name=1,header=None)  # header=None表示 sheet页中没有表头（“字段列”）
print(df_excel.head(3))
#        0        1        2        3        #可以看到：此时，columns使用了DataFrame的默认值（自动索引 即位置索引）
# 0  42964  3211.87  1596.16  1615.71
# 1  42965  3376.35  1777.65  1598.70
# 2  42966  3651.55  2304.97  1239.75

df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name=1)  #如果 sheet页是没有表头（“字段行”），但 header没有赋值为None，会怎么样？
print(df_excel.head(3))
# 42964.00  3211.87   1596.16   1615.71       #可以看到：有一行数据 作为表头了，不仅不好看 而且可以理解为“丢失了一行数据”
# 0     42965   3376.35   1777.65   1598.70
# 1     42966   3651.55   2304.97   1239.75
# 2     42967   2833.74   1431.51   1402.23

#特别注意：有的sheet也是多行表头
df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name='Sheet3',header=[0,1]) #用列表给header赋值，指定多行作为表头
print(df_excel.head(6))
# Unnamed: 0_level_0    销售额                               //可以看到：读取了“复合表头”   //Unnamed: 0_level_0 是因为 表中这一个格是空的
#                日期2 总销售额2 FBA销售额2 自配送销售额2
# 0              42964   3211.87    1596.16       1615.71
# 1              42965   3376.35    1777.65       1598.70
# 2              42966   3651.55    2304.97       1239.75
# 3              42967   2833.74    1431.51       1402.23
# 4              42968   3232.76    1568.85       1663.91
# 5              42969   3548.81    2180.57       1368.24

#虽然 表格的表头是复合（多行）的，但其实 也可以读取一行表头（根据业务实际情况来）
df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name='Sheet4',header=1,index_col=0)  #header=1 指定第二行为表头，index_col=0指定表格的第一列为索引
print(df_excel.head(6))
#       日期2  总销售额2  FBA销售额2  自配送销售额2
# 编号                                                 //注意：这是表格的第一列作为索引 //特别注意：“编号”这个字符串，此时 既不属于字段（列索引） 也不属于行索引，所以单独一行（醒目的说明 索引列是哪一列或哪几列）！
# 1     42964    3211.87     1596.16        1615.71
# 2     42965    3376.35     1777.65        1598.70
# 3     42966    3651.55     2304.97        1239.75
# 4     42967    2833.74     1431.51        1402.23
# 5     42968    3232.76     1568.85        1663.91
# 6     42969    3548.81     2180.57        1368.24
###说明：行索引默认是自动索引（位置索引）。如果 表格数据中 本来就有索引列，那么就可以指定该列作为数据帧DataFrame的行索引
print(df_excel.shape) #返回(44, 4)

df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name='Sheet4',header=1,index_col=[0,1]) #index_col可以指定多行索引列
print(df_excel.head(6))
#             总销售额2  FBA销售额2  自配送销售额2
# 编号 日期2                                          //可以看到，有两个索引字段
# 1    42964    3211.87     1596.16        1615.71
# 2    42965    3376.35     1777.65        1598.70
# 3    42966    3651.55     2304.97        1239.75
# 4    42967    2833.74     1431.51        1402.23
# 5    42968    3232.76     1568.85        1663.91
# 6    42969    3548.81     2180.57        1368.24
print(df_excel.shape) #返回(44, 3)

print("===========================================================================================1")

##使用usecols参数 导入指定列   //数据表有可能很大：只导入指定列可以提升性能    //不经可以提升性能，还能实现“跳过列” 见下文
df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",usecols=None)  #usecols的默认值是None，表示导入所有列
print(df_excel.head(3))         #可以看到：导入了所有的列
#    日期1  总销售额1  FBA销售额1  自配送销售额1
# 0  42964    3211.87     1596.16        1615.71
# 1  42965    3376.35     1777.65        1598.70
# 2  42966    3651.55     2304.97        1239.75
# df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx") #效果同上

##使用usecols参数的赋值形式多样：不同的赋值形式含义不同
#使用整数列表（由整数作为元素的列表）给usecols赋值，表示按照“位置索引（自动索引）”抽取指定列
df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",usecols=[2,3])
print(df_excel.head(3))
#    FBA销售额1  自配送销售额1
# 0     1596.16        1615.71
# 1     1777.65        1598.70
# 2     2304.97        1239.75

#使用字符串列表（由字符串作为元素的列表）给usecols赋值，表示按照“字段名称”抽取指定列
df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",usecols=['FBA销售额1','自配送销售额1'])
print(df_excel.head(3))
#    FBA销售额1  自配送销售额1
# 0     1596.16        1615.71
# 1     1777.65        1598.70
# 2     2304.97        1239.75

#使用字符串给usecols赋值，表示按照“Excel列标”抽取指定列  //Excel表格 都用字母作为“列标”来定位列，A、B、C、……、Z、AA、AB、AC、……、AZ、BA、BB、BC……
df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",usecols='A,C:D')   #'A,C:D'是“Excel列标”的写法，其中C:D是切片（与Python不同，Excel的切片 两边都是闭合的）
print(df_excel.head(3))
#    日期1  FBA销售额1  自配送销售额1
# 0  42964     1596.16        1615.71
# 1  42965     1777.65        1598.70
# 2  42966     2304.97        1239.75

#使用lambda函数给usecols赋值，表示 抽取符合条件的列
df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",usecols=lambda x:x=='自配送销售额1')   #条件抽取一列
print(df_excel.head(3))
#    自配送销售额1
# 0        1615.71
# 1        1598.70
# 2        1239.75

df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",usecols=lambda x:x in ['自配送销售额1','FBA销售额1'])  #条件抽取多列
print(df_excel.head(3))
#    FBA销售额1  自配送销售额1
# 0     1596.16        1615.71
# 1     1777.65        1598.70
# 2     2304.97        1239.75

df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",usecols=lambda x:(x == '自配送销售额1') | (x == 'FBA销售额1'))  #条件抽取多列
print(df_excel.head(3))
#    FBA销售额1  自配送销售额1
# 0     1596.16        1615.71
# 1     1777.65        1598.70
# 2     2304.97        1239.75

###我的理解：这里lambda的自变量x 是header所指定的“字段列”的一个个元素，lambda返回的是“关于 这些元素的真值判断”，如果为真 就赋值给usecols（可以假想 usecols有一个“隐含”的列表来保存所有的“真”元素，即“真”列名 ）

#测试：如果把header置为None 会如何
df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",header=None,usecols=lambda x:(x == '自配送销售额1') | (x == 'FBA销售额1'))
print(df_excel.head(3))
# Empty DataFrame
# Columns: []
# Index: []

#测试：如果没有正确指定“字段行” 会如何
df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",header=1,usecols=lambda x:(x == '自配送销售额1') | (x == 'FBA销售额1'))
print(df_excel.head(3))
# Empty DataFrame
# Columns: []
# Index: []

#测试：x能否 使用“位置索引”
df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",usecols=lambda x:(x == 2) | (x == 3))
print(df_excel.head(3))  #可以看到：不能使用位置索引
# Empty DataFrame
# Columns: []
# Index: []

### usecols参数的赋值形式 推荐为 字符串列表（或者以字符串列表为基础的lambda表达式），可读性好！
#                      而且“稳定性”好，因为Excel表格在使用过程中 有可能会插入列 这样的话 列的“位置索引”、“Excel列定位”可能发生变化（代码抽取的列 就不对了）！

###重要技巧：1，在Excel表格中“一拉”或者“一点” 复制所有列名
#          2，在IDLE中，先打上引号，在引号中 粘贴 复制的列名
#          3，在引号中，即字符串中 删除不需要的列名 //注意：保留空格作为元素间隔
#          4，在字符串后面 敲 .split() 回车
#          5，返回的就是 字符串列表，可以复制之后 赋值给usecols
df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",usecols=['日期1', 'FBA销售额1', '自配送销售额1'])  #操作效率 非常高！
print(df_excel.head(3))
#    日期1  FBA销售额1  自配送销售额1
# 0  42964     1596.16        1615.71
# 1  42965     1777.65        1598.70
# 2  42966     2304.97        1239.75

print("===========================================================================================2")
## 使用skiprows跳过指定行
#skiprows有两种赋值方式，含义不同！

#整数赋值给skiprows 表示从表格顶部跳过多少行
df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",skiprows=1)  #可以看到：从“顶”跳过1行，header会自动匹配
print(df_excel.head(3))
#    日期11  总销售额11  FBA销售额11  自配送销售额11
# 0   42964     3211.87      1596.16         1615.71
# 1   42965     3376.35      1777.65         1598.70
# 2   42966     3651.55      2304.97         1239.75

#“整数列表”赋值给skiprows 表示 按照行索引（位置索引）跳行
df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name='Sheet5',skiprows=[0,2,4]) #可以看到：跳过位置索引为0、2、4的行，header会自动匹配
print(df_excel.head(3))
#    日期51  总销售额51  FBA销售额51  自配送销售额51
# 0   42964     3211.87      1596.16         1615.71
# 1   42965     3376.35      1777.65         1598.70
# 2   42966     3651.55      2304.97         1239.75

#我猜，header默认 会自动从“跳过 剩下的行”中 取第一行作为表头即“字段列”

###思考：有没有skipcols？即有没有跳过列？这个参数是有的 但是不起作用（保留参数），也就是说 pandas有设计但没实现
#       怎么实现 跳过列？用usecols指定列来“间接”实现跳过列  //非指定列 自然就跳过了
df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name='Sheet6',skiprows=[0,2,4],usecols=['日期51', '总销售额51', 'FBA销售额51', '自配送销售额51'])
print(df_excel.head(3))
#    日期51  总销售额51  FBA销售额51  自配送销售额51
# 0   42964     3211.87      1596.16         1615.71
# 1   42965     3376.35      1777.65         1598.70
# 2   42966     3651.55      2304.97         1239.75


print("===========================================================================================3")

###names参数 自定义表头
df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx",names=['date','total_sales','FBA_total_sales','Self_delivery_total_sales']) #通过names参数，重命名表头
print(df_excel.head(3))
#     date  total_sales  FBA_total_sales  Self_delivery_total_sales
# 0  42964      3211.87          1596.16                    1615.71
# 1  42965      3376.35          1777.65                    1598.70
# 2  42966      3651.55          2304.97                    1239.75

#注意：如果读取的Excel表格 本来就没有表头，一定要加上header=None
df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name=1,header=None,names=['date','total_sales','FBA_total_sales','Self_delivery_total_sales'])
print(df_excel.head(3))
#     date  total_sales  FBA_total_sales  Self_delivery_total_sales   //可以看到：这样表 原本是没有表头的 现在有表头了
# 0  42964      3211.87          1596.16                    1615.71
# 1  42965      3376.35          1777.65                    1598.70
# 2  42966      3651.55          2304.97                    1239.75

###如果，没加header=None
df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",sheet_name=1,names=['date','total_sales','FBA_total_sales','Self_delivery_total_sales'])
print(df_excel.head(3))
#     date  total_sales  FBA_total_sales  Self_delivery_total_sales   //与上面数据对比，可以发现 少掉了第一行  //这种错误 不会有报错（不是运行出错，是逻辑错误），要特别小心！
# 0  42965      3376.35          1777.65                    1598.70
# 1  42966      3651.55          2304.97                    1239.75
# 2  42967      2833.74          1431.51                    1402.23

print("===========================================================================================f")
###特别注意：有的表格数据量很大，不要一下子直接打印出来（不要 print(df)）,否则 严重消耗计算机的资源  而且屏幕上也“看不全”那么多数据
#          可以使用df的head()或者tai()方法，控制打印的数据量

df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx")
print(df_excel.head(10)) #看 （不含字段）头10行数据
#    日期1  总销售额1  FBA销售额1  自配送销售额1
# 0  42964    3211.87     1596.16        1615.71
# 1  42965    3376.35     1777.65        1598.70
# 2  42966    3651.55     2304.97        1239.75
# 3  42967    2833.74     1431.51        1402.23
# 4  42968    3232.76     1568.85        1663.91
# 5  42969    3548.81     2180.57        1368.24
# 6  42970    3583.35     2175.67        1407.68
# 7  42971    4276.04     3019.30        1256.74
# 8  42972    4324.31     2621.78        1654.54
# 9  42973    3414.59     2430.97         983.65
print(df_excel.tail(10))   #追后10行数据，而且还“外加一行字典”
#     日期1  总销售额1  FBA销售额1  自配送销售额1
# 34  42998    7039.30     2474.84        4564.66
# 35  42999    7386.43     2745.98        4640.45
# 36  43000    6889.75     2331.15        4558.60
# 37  43001    7779.84     2311.33        5468.51
# 38  43002    8545.04     1757.67        6787.37
# 39  43003    8661.25     1875.79        6785.46
# 40  43004    7556.05     2478.30        5077.75
# 41  43005    7552.84     2298.87        5253.97
# 42  43006    9344.08     2470.79        6873.29
# 43  43007    8569.42     2443.72        6125.70

print("===========================================================================================5")
##读表之后，再定义"行索引"
df_excel=pd.read_excel("./实验数据/excel_data_2.xlsx",header=1,sheet_name='Sheet4') #假设，此时 读表“忘记”定义“行索引”
print(df_excel.head(2))
#    编号  日期2  总销售额2  FBA销售额2  自配送销售额2          //可以看到打印的数据帧，有“编号”字段
# 0     1  42964    3211.87     1596.16        1615.71
# 1     2  42965    3376.35     1777.65        1598.70
df_excel=df_excel.set_index('编号')  #读表之后，再定义"行索引" #将“编号”字段 定义为数据帧的“行索引”，将修改后的数据帧“原地保存（赋值给自己）”
print(df_excel.head(3))
#       日期2  总销售额2  FBA销售额2  自配送销售额2
# 编号                                                   //可以看到，此时使用的是 自定义的“行索引”，不是 默认的自动索引
# 1     42964    3211.87     1596.16        1615.71
# 2     42965    3376.35     1777.65        1598.70
# 3     42966    3651.55     2304.97        1239.75

##读表之后，再修改列名
#方法1：全部字段 重名
df=df_excel  ###特别注意 数据帧DataFrame的复制 是浅复制！
df.columns=['date','total_sales','FBA_total_sales','Self_delivery_total_sales'] #全部修改df的字段名
print(df_excel.head(3))  #可以看到df_excel的字段名 也被修改了！
#        date  total_sales  FBA_total_sales  Self_delivery_total_sales
# 编号
# 1     42964      3211.87          1596.16                    1615.71
# 2     42965      3376.35          1777.65                    1598.70
# 3     42966      3651.55          2304.97                    1239.75

#再把字段名 全部改回来
# df_excel.columns=['编号', '日期2', '总销售额2', 'FBA销售额2', '自配送销售额2'] #报错：ValueError: Length mismatch: Expected axis has 4 elements, new values have 5 elements
#错误原因：四个字段 给了五个值！
df_excel.columns=['日期2', '总销售额2', 'FBA销售额2', '自配送销售额2']  #再把字段名 全部改回来
print(df_excel.head(3))
#       日期2  总销售额2  FBA销售额2  自配送销售额2
# 编号
# 1     42964    3211.87     1596.16        1615.71
# 2     42965    3376.35     1777.65        1598.70
# 3     42966    3651.55     2304.97        1239.75


##读表之后，再修改列名
#方法2：部分字段 重名
df_excel.rename(columns={"日期2":"date_2",'FBA销售额2':'FBA_total_sales'})
print(df_excel.head(3))
#       日期2  总销售额2  FBA销售额2  自配送销售额2        //发现：没有修改,解决方法如下
# 编号
# 1     42964    3211.87     1596.16        1615.71
# 2     42965    3376.35     1777.65        1598.70
# 3     42966    3651.55     2304.97        1239.75

df_excel=df_excel.rename(columns={"日期2":"date_2",'FBA销售额2':'FBA_total_sales'})  #同上，需要原地保存
print(df_excel.head(3))
#       date_2  总销售额2  FBA_total_sales  自配送销售额2       //可以看到 部分字段的名称被修改了
# 编号
# 1      42964    3211.87          1596.16        1615.71
# 2      42965    3376.35          1777.65        1598.70
# 3      42966    3651.55          2304.97        1239.75

#rename方法 的另一种赋值方式
df_excel=df_excel.rename({"date_2":"日期2",'FBA_total_sales':'FBA销售额2'},axis='columns')  #通过axis参数 指定修改的是 字段名
print(df_excel.head(3))
#       日期2  总销售额2  FBA销售额2  自配送销售额2           //可以看到列名改回来了
# 编号
# 1     42964    3211.87     1596.16        1615.71
# 2     42965    3376.35     1777.65        1598.70
# 3     42966    3651.55     2304.97        1239.75


###注意：rename不仅能够修改 列索引（字段）名，还能修改行索引名
df_excel=df_excel.rename(index={1:'one',2:'two',3:'three'})
print(df_excel.head(5))
#        日期2  总销售额2  FBA销售额2  自配送销售额2
# 编号
# one    42964    3211.87     1596.16        1615.71   #可以看到，部分 行索引名称 被修改了
# two    42965    3376.35     1777.65        1598.70
# three  42966    3651.55     2304.97        1239.75
# 4      42967    2833.74     1431.51        1402.23
# 5      42968    3232.76     1568.85        1663.91

#rename方法 的另一种赋值方式
df_excel=df_excel.rename({4:'four',5:'five'},axis='index')  #通过axis参数 指定修改的是 行索引名称
print(df_excel.head(8))
#        日期2  总销售额2  FBA销售额2  自配送销售额2
# 编号
# one    42964    3211.87     1596.16        1615.71
# two    42965    3376.35     1777.65        1598.70
# three  42966    3651.55     2304.97        1239.75
# four   42967    2833.74     1431.51        1402.23
# five   42968    3232.76     1568.85        1663.91
# 6      42969    3548.81     2180.57        1368.24
# 7      42970    3583.35     2175.67        1407.68
# 8      42971    4276.04     3019.30        1256.74

