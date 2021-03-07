import pandas as pd
import numpy as np

'''
NaN的含义:not a number
pandas用NaN表示 缺失值，据说NaN 是float类型的

在pandas读取Excel数据的时候，默认将以下的值(16种) 解析为NaN     //即 默认缺失值  
''  //空字符串 

'NULL'   //注意：经过测试：直接在Excel单元格里写NULL，读入之后 可以解析为NaN。但是 如果在Excel单元格里写"NULL",读入只有 就不会解析为NaN

'NA'     //各种NA
'N/A'
'n/a'
'#NA'
'#N/A'
'#N/A N/A'
'<NA>'

'NaN'    //各种NaN
'-NaN'
'-nan'

'-1.#IND'
'1.#IND'

'-1.#QNAN'
'1.#QNAN'

'''

#测试上面改的16个默认空值
df_excel=pd.read_excel("./实验数据/na_values.xlsx",sheet_name="Sheet2",header=None)  #注意：这该表 没有表头  #注意，这里没有使用na_values参数，也会将默认缺失值 解析为NaN
print(df_excel)
#     0   1   2   3
# 0 NaN NaN NaN NaN     //可以看到 将“各种默认缺失值” 都解析为NaN，这样数据处理起来就统一了
# 1 NaN NaN NaN NaN
# 2 NaN NaN NaN NaN
# 3 NaN NaN NaN NaN

#测试发现，如果“表头为缺失值”，也不会被解析为NaN
df_excel=pd.read_excel("./实验数据/na_values.xlsx",sheet_name="Sheet2")
print(df_excel)
#    Unnamed: 0  -1.#IND  1.#IND  NA    //这里把第一行数据当做表头了，所以 没有将缺失值 解析为NaN
# 0         NaN      NaN     NaN NaN
# 1         NaN      NaN     NaN NaN
# 2         NaN      NaN     NaN NaN


df_excel=pd.read_excel("./实验数据/na_values.xlsx")
print(df_excel)
#     列1   列2
# 0    a    0
# 1  NaN  NaN    //该行在Excel中为  #N/A  #NA
# 2  NaN         //该行在Excel中为  空（啥都不填） 有一个空格   //特别注意：空格 不是默认的缺失值，默认不会被解析为NaN
# 3    b    1



###参数na_values指定哪些值“要解析为空值”  //在默认缺失值的基础上，额外添加“缺失值的定义”
## 参数na_values有多种不同赋值方式，含义不同

##1
#将单个数值 或者 字符串 赋值给参数na_values表示：将这个数值 或者字符串 解析为NaN，全表有效
df_excel=pd.read_excel("./实验数据/na_values.xlsx",na_values=0)
print(df_excel)
#     列1   列2
# 0    a  NaN    //可以看到：此时 将0 解析成了空值NaN
# 1  NaN  NaN
# 2  NaN
# 3    b    1

df_excel=pd.read_excel("./实验数据/na_values.xlsx",na_values='a')
print(df_excel)
#     列1   列2
# 0  NaN    0    //可以看到：此时 将字符串'a' 解析成了空值NaN
# 1  NaN  NaN
# 2  NaN
# 3    b    1


##2
#将列表 赋值给参数na_values表示：将列表中的元素 都解析为NaN，全表有效
df_excel=pd.read_excel("./实验数据/na_values.xlsx",na_values=['a',0,' '])
print(df_excel)
#     列1   列2
# 0  NaN  NaN    //可以看到：此时 将字符串'a'和数字0 都解析成了空值NaN
# 1  NaN  NaN
# 2  NaN  NaN    //可以看到：空格 也被解析为空值NaN
# 3    b  1.0

###特别说明：单元格里面 只填一个空格，一般都是人为操作的结果（如果是系统导出的表格，不会这样），有时候 单元格里面 会有“连续空额”。//上面的方法 是指定了“单个空格”为NaN，如果是“连续空格”的话 则不会指定为NaN。这在处理上 是有点麻烦的！
#          操作表格时，应该避免这种错误   //同样的，人为 在单元格的数据前面加空格、后面加空格，也是不应该的

##3
#将字典 赋值给参数na_values表示：在key指定的列中，将列表中的元素 都解析为NaN
df_excel=pd.read_excel("./实验数据/na_values.xlsx",na_values={"列1":['a',0,' ']})
print(df_excel)
#     列1   列2   //可以看到 列2没有受到影响
# 0  NaN    0
# 1  NaN  NaN
# 2  NaN
# 3    b    1

df_excel=pd.read_excel("./实验数据/na_values.xlsx",na_values={1:['a',0,' ']})
print(df_excel)
#     列1   列2  //可以开电脑 列1没有受到影响
# 0    a  NaN
# 1  NaN  NaN
# 2  NaN  NaN
# 3    b  1.0

print("=============================================================================================1")

df_excel=pd.read_excel("./实验数据/converters.xlsx")
print(df_excel)
#         货号  销量
# 0  \t\naaa  10       //特别注意：有时候，Excel单元格中的数据 是带有\t\n制表符换行符的（在Excel中 还看不出来），这是会影响数据匹配的
# 1  \t\nbbb  20


###converters参数 可以对指定列做数据转换
##使用字典给converters参数赋值，key指定字段，value指定转换方法
df_excel=pd.read_excel("./实验数据/converters.xlsx"
                       ,converters={
                            '货号':lambda x:x.strip()   #调用字符串的strip()方法，将字符串首尾的“空白”去掉  //函数、方法 也可以作为value
                            #'货号':str.strip  #效果同上，我觉得 可读性没有上面的好
    })
print(df_excel)
#     货号  销量
# 0  aaa  10         //可以看到：单元格中中的\t\n，被清洗了
# 1  bbb  20

df_excel=pd.read_excel("./实验数据/converters.xlsx",sheet_name=1)
print(df_excel)
#         货号    销量
# 0  \t\naaa    10
# 1  \t\nbbb             //该行的销量 是三个“连续空格”

# df_excel=pd.read_excel("./实验数据/converters.xlsx",sheet_name=1
#                        ,converters={
#                             '销量':lambda x:x.strip()
#     })  #报错
#AttributeError: 'int' object has no attribute 'strip'   //错误原因：销量字段中 有的单元格个数据是整型，而整型对象是没有strip方法的

#读取数据之后，也可以判断空值、去除空格
df_excel['销量']=df_excel['销量'].astype('string')          #先将该列的dtype改为string，这样就能调用isspace()和strip()方法了
df_excel['销量']=df_excel['销量'].apply(lambda x:np.NaN if x.isspace() else x.strip()) #对该列应用lambda函数 去除单元格中字符串首尾的“空白”
df_excel['货号']=df_excel['货号'].apply(lambda x:x.strip())
print(df_excel)
#     货号   销量
# 0  aaa   10
# 1  bbb  NaN

#说明：字符串的isspace()用来判断是不是“空白字符串”，     测试：‘ ’.isspace()返回True   '\r\n'.isspace()返回True
#                    注意：“空字符串”不是 “空白字符串”     ''.isspace()返回False
#lambda x:np.NaN if x.isspace() else x.strip()的逻辑是：如果 单元格是“（连续）空白字符” 就返回NaN，如果不是“（连续）空白字符” 就“去除字符串的首尾空白（如果有的话）”
#不能先对某个单元格x.strip()，否则 如果这个单元格是“（连续）空白字符” x.strip()返回的就是“空字符串”，而“空字符串”.isspace() 返回False

# df_excel['销量']=df_excel['销量'].astype('int64') #报错
# ValueError: cannot convert float NaN to integer   //因为NaN是float类型

###特别注意：apply()方法是 序列Series对象的方法，我的理解：apply()方法的实参就是一个“处理函数”，apply会遍历序列元素 “处理函数”依次处理 从而得到“新的序列”


df_excel['销量']=df_excel['销量'].astype('float64')  #一个字段中 有NaN,是可以转换为float64的
print(df_excel.dtypes)
# 货号     object
# 销量    float64
# dtype: object

print(type(np.NaN)) #<class 'float'>

print("=============================================================================================2")

###真值处理

df_excel=pd.read_excel("./实验数据/true_false_values.xlsx")
print(df_excel)
#   列1 列2  列3
# 0  a  d   0
# 1  b  e   1
# 2  c  f   2
print(df_excel.dtypes)
# 列1    object
# 列2    object
# 列3     int64
# dtype: object

#将某列的dtype设置为bool类型，就会将该列的数据强制为True或False  //非零、非空就是FALSE
df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",dtype={0:bool,1:bool,2:bool})  #把所有列 都强置dtype为bool
print(df_excel)
#      列1    列2     列3
# 0  True  True  False
# 1  True  True   True
# 2  True  True   True

##注意：测试：bool("")返回True  bool(0)返回True  bool(0.0)返回True   bool(None)返回False  bool("")返回False

df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",dtype={"列3":bool})  #将 列3 强置dtype为bool
print(df_excel)
#   列1 列2     列3
# 0  a  d  False
# 1  b  e   True
# 2  c  f   True

#注意：强置列为bool类型的方式，其实就是调用Python的bool()函数 进行真值判断

#使用参数true_values和false_values 自定义真值判断
df_excel=pd.read_excel("./实验数据/true_false_values.xlsx"
                       ,true_values=["a","b"]     #自定义 为真的值有哪些
                       ,false_values=['c','d']    #自定义 为假的值有哪些
                       )#参数true_values和false_values ，全表有效
print(df_excel)
#       列1 列2  列3
# 0   True  d   0    //可以看到列1起作用了
# 1   True  e   1
# 2  False  f   2
print(df_excel.dtypes)
# 列1      bool      //可以看到列1的类型为bool
# 列2    object
# 列3     int64
# dtype: object

##注意：可以看到 列1起作用了，但是列2和列3不起作用
#      列3不起作用 是因为列3中的元素不是字符串， “true_values和false_values 两个列表”中 只有字符串是有效的 数字无效
#      列2不起作用 是因为列2中 有元素的值（比如'e'和'f'） 不在“true_values和false_values 两个列表”中，也就是说“一列中 只要有元素的值 不能判断真假，就不起作用”

df_excel=pd.read_excel("./实验数据/true_false_values.xlsx"
                       ,true_values=["a","b","e"]     #自定义 为真的值有哪些
                       ,false_values=['c','d','f']    #自定义 为假的值有哪些
                       )
print(df_excel)
#       列1     列2  列3  //可以看到 此时 对列1和列2都起作用了
# 0   True  False   0
# 1   True   True   1
# 2  False  False   2
print(df_excel.dtypes)
# 列1     bool
# 列2     bool
# 列3    int64
# dtype: object

#思考：我觉得，参数true_values和false_values 一般应该同时使用的，因为 如果只定义了一个 比如true_values 那么除非有一列中元素全部都是True 否则就不起做作用了


print("=============================================================================================3")

###补充

###参数index_col指定行索引时，如果用“字符串列表”赋值 可能会报错
# df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",index_col=["列1","列2"]) #TypeError: list indices must be integers or slices, not str
#可能原因是pandas还不完善
df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",index_col=[0,1])
print(df_excel)  #“多个索引列”，只能用“数值列表”给index_col赋值   //单个“索引列”，可以用数值 也可以用字符串 赋值给index_col
#        列3
# 列1 列2
# a  d    0
# b  e    1
# c  f    2


###参数squeeze 默认为False，表示：如果Excel表只有一列，返回值类型为DataFrame
#           如果为True，表示：如果Excel表只有一列，返回值类型为Series
df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",sheet_name=2)
print(df_excel)
#   列1   //该表只有一列，可以看出来 打印的数据是DataFrame形式
# 0  d
# 1  e
# 2  f
print(type(df_excel)) #<class 'pandas.core.frame.DataFrame'>
df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",sheet_name=2,squeeze=True)
print(df_excel)
# 0    d   //可以看出来 打印的数据是Series形式
# 1    e
# 2    f
# Name: 列1, dtype: object
print(type(df_excel)) #<class 'pandas.core.series.Series'>


###参数mangle_dupe_cols 默认为True，表示：如果Excel表中 有重复的列名，则自动重命名
#                    如果为False，表示：如果Excel表中 有重复的列名，就抛异常
df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",sheet_name=3)
print(df_excel)
#    列 列.1 列.2   //可以看到，将重复的列  改名为“列名.几”
# 0  d   a   x
# 1  e   b   y
# 2  f   c   z


###参数nrows表示要解析的函数   //可能一张Excel表的行数很多，不是所有行都需要读入
df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",sheet_name=4)
print(df_excel.shape) #(15, 3) 数据量：15行 3列
df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",sheet_name=4,nrows=3) #nrow=3表示读入3行数据（不算表头的那一行）
print(df_excel)
#   列1 列2 列3
# 0  d  a  x
# 1  e  b  y
# 2  f  c  z


###参数thousands 默认None ,表示：不解析“千分位字符串”
#如果将一个“符号”即字符 赋值给参数thousands，表示：用该"符号" 将“千分位字符串”解析为数值
df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",sheet_name=5)
print(df_excel)
#        金额1        金额2    //可以看到 第一列数据正确解析为数值了，第二列数据 还是字符串的形式   //这两列数据在Excel表格中 看起来一样，第一列 类型为“货币” 第一列 类型为“常规”
# 0     2188      2,188
# 1  1000188  1,000,188
print(df_excel.dtypes)
# 金额1     int64
# 金额2    object
# dtype: object

df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",sheet_name=5,thousands=',')  #thousands=','指定千分位 分隔符为逗号','
print(df_excel)
#        金额1      金额2     //可以看到 ，此时 第二列数据也被正确解析了
# 0     2188     2188
# 1  1000188  1000188
print(df_excel.dtypes)   #数据类型都是int64
# 金额1    int64
# 金额2    int64
# dtype: object


###参数convert_float 默认为True 表示：在可能的情况下 是否将float转化为int
#                   如果为false ，则读取的数据 都是float类型
df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",sheet_name=6)
print(df_excel)
#    列1   列2  列2.1  //注意：列2.1是“重复名列的重命名”
# 0   1  1.1   1.0
# 1   2  2.1   2.0
# 2   3  3.1   3.0
# 3   4  4.1   4.0
# 4   5  5.1   5.0
# 5   6  6.1   6.0

df_excel=pd.read_excel("./实验数据/true_false_values.xlsx",sheet_name=6,convert_float=False)
print(df_excel)
#     列1   列2  列2.1  //可以看到都是浮点数
# 0  1.0  1.1   1.0
# 1  2.0  2.1   2.0
# 2  3.0  3.1   3.0
# 3  4.0  4.1   4.0
# 4  5.0  5.1   5.0
# 5  6.0  6.1   6.0