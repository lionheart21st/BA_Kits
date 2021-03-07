import pandas as pd

pd.set_option('display.unicode.east_asian_width',True)  #调整“列名与数据的对齐”
pd.set_option('display.max_columns',1000) #调整输出的列数
pd.set_option('display.width',1000)       #调整输出的最大宽度

'''
dtype类型：    //DataFrame数据帧由Series序列组成，而Series序列是有数据类型的

int8/int16/int32/int64(默认)：  整型               
float16/float32/float64(默认)： 浮点型              
str/string：                    字符串*
bool:                          布尔               
category：                     分类*
datetime64[ns]:                时间戳(纳秒)
period[Y/M/D]:                 时间周期(年/月/日)*
object:                        python对象混合类型   //Series序列中的 元素的数据类型 是不同的，那么Series序列类型 很有可能就是object

注意：上面打*的三种类型，都是要手动设置的。不打*的类型，pandas可以自动判断出来（大概 只要Series的数据元素的类型是一致的，否则就是object）
'''

df_excel=pd.read_excel("./实验数据/excel_data_1.xlsx")
print(df_excel.dtypes)
# 日期1          int64
# 总销售额1      float64
# FBA销售额1    float64
# 自配送销售额1    float64    //可以看到四个字段，都分别有自己的dtype
# dtype: object             //最后 还有一个dtype。因为df_excel.dtypes的返回值 本身也是Series 所以本身也会有一个dtype
print(type(df_excel.dtypes)) #<class 'pandas.core.series.Series'>


df_excel=pd.read_excel("./实验数据/goods_base.xlsx")
print(df_excel.dtypes)
# 货号              object   //Excel中的字符串，pandas默认判断为object
# 商品代码            object
# 颜色代码             int64  //pandas自动判断为数字
# 商品名称            object
# 品牌              object
# 成本               int64
# 季节              object
# 商品年份             int64   //pandas自动判断为数字
# 上架日期    datetime64[ns]   //Excel中 该字段是日期格式，所以pandas自动判断为时间戳
# 上架费            float64
# 在售                bool    //Excel中 该字段的取值是True和False，所以pandas自动判断为bool  //如果 该字段的取值是0和1，pandas不会自动判断为bool 而会判断为int64。
# dtype: object              //可以看到：上面11个字段，都分别有自己的dtype  //最后 还有一个dtype,是df_excel.dtypes返回值本身的dtype
print(df_excel.head(6))   #查看数据，与其数据类型对比一下
#        货号 商品代码  颜色代码  商品名称 品牌  成本  季节  商品年份   上架日期  上架费  在售
# 0  QTVW5600     QTVW      5600    羽绒服    A   180  冬季      2018 2018-01-01     1.2  True
# 1  AXTB3200     AXTB      3200      棉服    B    90  冬季      2019 2019-01-02     1.2  True
# 2  VBOY1800     VBOY      1800    家居服    C   120  冬季      2018 2018-01-01     1.2  True
# 3  HWLA4700     HWLA      4700   长袖T恤    A    30  秋季      2020 2020-01-01     1.2  True
# 4  XDQV5600     XDQV      5600      卫衣    B    56  春季      2019 2019-01-03     1.2  True
# 5  XHQA3700     XHQA      3700  羊毛大衣    C   200  冬季      2018 2018-05-05     1.2  True


##读取Excel表格时，手动指定dtype类型
df_excel=pd.read_excel("./实验数据/goods_base.xlsx"
                       ,dtype={
                                '货号':'str'
                                ,'商品代码':'string'
    })
print(df_excel.dtypes)
# 货号                object   //可以看到：虽然将“货号”的dtype定义为str类型，但是显示的还是object
# 商品代码            string    //可以看到：“商品代码”的dtype改为string了
# 颜色代码             int64
# 商品名称            object
# 品牌                object
# 成本                 int64
# 季节                object
# 商品年份             int64
# 上架日期    datetime64[ns]
# 上架费             float64
# 在售                  bool
# dtype: object


##再将“颜色代码”的类型 改为string  //虽然，看起来是数字 但是希望是字符串
df_excel=pd.read_excel("./实验数据/goods_base.xlsx"
                       ,dtype={
                                '货号':'str'
                                ,'商品代码':'string'
                                ,'颜色代码':'string'
    })
print(df_excel.dtypes)
# 货号                object
# 商品代码            string
# 颜色代码            string    //可以看到修改成功！
# 商品名称            object
# 品牌                object
# 成本                 int64
# 季节                object
# 商品年份             int64
# 上架日期    datetime64[ns]
# 上架费             float64
# 在售                  bool
# dtype: object

###特别注意：有时候，在read_excel中 将某个字段(比如“颜色代码”)类型设置为string可能会失败（报错：StringArray requires a sequence of string or pandas.NA）。即不能直接将int64转化为string
#                可以先在read_excel中 将其dtype设置为str。然后，df[“颜色代码”]=df[“颜色代码”].astype('string')  //即读取之后，再对单个字段 手动修改属性
df_excel=pd.read_excel("./实验数据/goods_base.xlsx"
                       ,dtype={
                                '货号':'str'
                                ,'商品代码':'string'
                                ,'颜色代码':'str'
    })
df_excel['颜色代码']=df_excel['颜色代码'].astype('string')  #调用DataFrame的astype方法 将dtype修改为string
print(df_excel.dtypes['颜色代码']) #返回string  #df_excel.dtypes['颜色代码'] 表示单独看一个字段的dtype


#如果一个字段"很多行数据中，只有几个取值的话”，可以将这个字段 定义为“分类 类型”，有利于节约内存（也有利于排序）
df_excel=pd.read_excel("./实验数据/goods_base.xlsx"
                       ,dtype={
                                '货号':'str'
                                ,'商品代码':'string'
                                ,'颜色代码':'string'
                                ,'品牌':'category'      #将'品牌'设置为 “分类 类型”
                                ,'季节':'category'      #将'季节'设置为 “分类 类型”
                                ,'商品年份':'period[Y]'  #将'商品年份'设置为 时间周期 [Y]表示时间周期是年
    })
print(df_excel.dtypes)
# 货号                object
# 商品代码            string
# 颜色代码            string
# 商品名称            object
# 品牌              category    //修改成功
# 成本                 int64
# 季节              category    //修改成功
# 商品年份     period[A-DEC]     //修改成功
# 上架日期    datetime64[ns]
# 上架费             float64
# 在售                  bool
# dtype: object

###特别注意：为什么 读取Excel要修改dtype,因为 字段不同的dtype 就会有不同的函数可以使用（即 可以调用的“功能”是不同的）
#          貌似，混合型object 因为不能确定数据类型 其“功能”是最弱的！//读取时，尽量减少object类型！

print("=============================================================================================1")
'''
在Excel表格中填写的日期，往往有如下的“形式”
20200120
2020/1/20
1/20/2020
2020-01-20
2020-01-20 00:10:10
这个其中，按照Excel的“数字格式”来看 有可能是数值 有可能是文本 也有可能日期
pandas读取这些数据，如果是数值 可能会解析为int64格式
                 如果是文本 可能会解析为object格式
                 如果是日期 可能会解析为datetime64[ns]格式

通过read_excel的parse_dates参数，可以将上述日期形式 都解析为datetime64[ns]格式                
                 
但是，如果Excel表格中填写的日期格式为：
2020年1月20日    //中文日期形式
仅凭parse_dates参数还不能解析，还需要 配合date_parser参数指定解析函数   
我的理解：parse_dates用来指定哪些列需要解析为日期格式，date_parser是指定解析的方法
'''

#读取Excel表格
df_excel=pd.read_excel("./实验数据/parse_dates.xlsx",index_col=2)  #index_col=2将第三列作为“行索引列”
print(df_excel)   #可以看到日期2 作为行索引
#                日期0     日期1      日期3      日期4                日期5      日期6
# 日期2
# 2020-01-20  20200120  20200120  1/20/2020  2020/1/20  2020-01-20 00:10:10 2020-01-20
# 2020-01-21  20200121  20200121  1/21/2020  2020/1/21  2020-01-21 00:10:11 2020-01-21
print(df_excel.dtypes)     #dtypes查看各个字段的数据类型 //特别注意：看不到“行索引”的数据类型
# 日期0             int64  //Excel的数值 pandas解析为 解析为int64格式
# 日期1             int64
# 日期3            object  //Excel的文本 pandas解析为 解析为object格式
# 日期4            object
# 日期5            object
# 日期6    datetime64[ns]  //Excel的日期 pandas解析为 解析为datetime64[ns]格式
# dtype: object
print(df_excel.index) #Index(['2020-01-20', '2020-01-21'], dtype='object', name='日期2')
                      #通过index 才能查看“行索引列”的数据类型  #注意：此时  “行索引”的数据类型为object格式


##parse_dates参数有多种赋值方式，含义不同
##1
#pares_dates = True 表示：尝试解析index即“行索引列” ，也就是 尝试把DataFrame的index“行索引列”解析成日期格式。如果解析不成功 也不会出错 也就是保留原格式！
df_excel=pd.read_excel("./实验数据/parse_dates.xlsx",index_col=2,parse_dates=True)
print(df_excel.index) #DatetimeIndex(['2020-01-20', '2020-01-21'], dtype='datetime64[ns]', name='日期2', freq=None)
                      #可以看到，此时 “行索引列” 解析为datetime64[ns]格式了

##2
#使用列表（元素可以是“列的位置索引” 也可以 “列名字符串”）给pares_dates赋值，表示 将这些字段解析为日期格式   //特别注意：列表中可以包含“行索引列”
df_excel=pd.read_excel("./实验数据/parse_dates.xlsx",index_col=2,parse_dates=[0,1,2]) #parse_dates=[0,1,2] 列表中包含了“行索引列”
print(df_excel.dtypes)
# 日期0    datetime64[ns]   //可以看到 此时 该列解析为时间戳datetime64[ns]格式了
# 日期1    datetime64[ns]   //可以看到 此时 该列解析为时间戳datetime64[ns]格式了
# 日期3            object
# 日期4            object
# 日期5            object
# 日期6    datetime64[ns]
# dtype: object
print(df_excel.index) #DatetimeIndex(['2020-01-20', '2020-01-21'], dtype='datetime64[ns]', name='日期2', freq=None)
                      #可以看到，此时 “行索引列” 也解析为时间戳datetime64[ns]格式了

df_excel=pd.read_excel("./实验数据/parse_dates.xlsx",index_col=2,parse_dates=['日期0','日期1'])  #注意：这次 没有将“行索引列”放入列表
print(df_excel.dtypes)
# 日期0    datetime64[ns]
# 日期1    datetime64[ns]
# 日期3            object
# 日期4            object
# 日期5            object
# 日期6    datetime64[ns]
# dtype: object
print(df_excel.index) #Index(['2020-01-20', '2020-01-21'], dtype='object', name='日期2')
                      #可以看到，此时 “行索引列” 还是混合格式

##3
#使用二维列表给pares_dates赋值，表示 将“Excel中的多列解析”为DataFrame中单个日期列
df_excel=pd.read_excel("./实验数据/parse_dates.xlsx",sheet_name=1,parse_dates=[[0,1,2]])  #二维列表 可以用“列的位置索引”描述
print(df_excel)
#     年_月_日  销量      //可以看到 年月日被合并成一列。合并后的列名为：列名1_列名2_列名3
# 0 2020-01-20   100
# 1 2020-01-21   200
print(pd.read_excel("./实验数据/parse_dates.xlsx",sheet_name=1))  #查看 原数据，年、月、日分别 一列
#      年  月  日  销量
# 0  2020   1  20   100
# 1  2020   1  21   200

df_excel=pd.read_excel("./实验数据/parse_dates.xlsx",sheet_name=1,parse_dates=[['年','月','日']])  #二维列表 也可以用“列的名称字符串”描述
print(df_excel)
#     年_月_日  销量
# 0 2020-01-20   100
# 1 2020-01-21   200

##4
##使用字典给pares_dates赋值，效果是第3中方式类似，同时再给 合并后的列 命名
df_excel=pd.read_excel("./实验数据/parse_dates.xlsx",sheet_name=1,parse_dates={"日期":['年','月','日']})  #字典的key就是 “合并列的名”，字典的value就是 哪些列参入合并解析
print(df_excel)
#         日期  销量     //可以看到 合并的列名 被命名为“日期”
# 0 2020-01-20   100
# 1 2020-01-21   200

print("=============================================================================================2")
##parse_dates和date_parser两种参数的配置使用

#先看下原数据
df_excel=pd.read_excel("./实验数据/date_parser.xlsx")
print(df_excel)
#             日期    //就一列数据 中文日期形式
# 0  2020年1月20日
# 1  2020年1月21日
print(df_excel.dtypes)
# 日期    object
# dtype: object

#尝试 仅靠parse_dates参数 解析 中文日期形式
df_excel=pd.read_excel("./实验数据/date_parser.xlsx",parse_dates=[0])
print(df_excel)
#             日期
# 0  2020年1月20日
# 1  2020年1月21日
print(df_excel.dtypes)
# 日期    object
# dtype: object    //可以看到 解析时间戳失败了，但是 虽然失败 并不影响数据的导入（按照“原格式”导入）

#parse_dates用来指定哪些列需要解析为日期格式，date_parser是指定解析的方法
df_excel=pd.read_excel("./实验数据/date_parser.xlsx",parse_dates=[0],date_parser=lambda x:pd.to_datetime(x,format='%Y年%m月%d日')) #date_parser参数 使用lambda函数描述解析格式
print(df_excel.dtypes)
# 日期    datetime64[ns]    //可以看到，此时 中文日期格式 解析成功
# dtype: object
##我的理解：这里的lambda函数 调用的是pandas的to_datetime方法  该方法中的format参数 定义了解析格式为'%Y年%m月%d日'
#         lambda函数的x是什么？
#         我猜想：pandas的基础数据结构是Series和DataFrame，那么x很有可能就是序列，而且pandas中 lambda会迭代处理序列中的元素（可能是pandas的特性）！也就简单粗暴的“先把x看做列名 再把x看做列中元素”！
#         lambda函数处理完毕 之后，我猜，返回的也是序列

#在Excel表格数据读入之后，也可以修改某个字段的数据类型
df_excel=pd.read_excel("./实验数据/date_parser.xlsx")
df_excel['日期']=pd.to_datetime(df_excel['日期'],format='%Y年%m月%d日')  #可以看到 to_datetime方法的第一个形参 确实是Series序列 //to_date的返回值也是Series序列，我的理解，to_date是“遍历处理函数”  对序列中的每个元素按照format='%Y年%m月%d日'的规则处理
print(df_excel.dtypes)
# 日期    datetime64[ns]  //可以看到，此时 中文日期格式 解析成功
# dtype: object

print("=============================================================================================3")
###综合日期解析实验

df_excel=pd.read_excel("./实验数据/parse_dates.xlsx",sheet_name="Sheet3")
print(df_excel)
#       日期0     日期1       日期2      日期3      日期4                日期5      日期6          日期7    年  月  日
# 0  20200120  20200120  2020-01-20  1/20/2020  2020/1/20  2020-01-20 00:10:10 2020-01-20  2020年1月20日  2020   1  20
# 1  20200121  20200121  2020-01-21  1/21/2020  2020/1/21  2020-01-21 00:10:11 2020-01-21  2020年1月21日  2020   1  21
print(df_excel.dtypes)
# 日期0             int64
# 日期1             int64
# 日期2            object
# 日期3            object
# 日期4            object
# 日期5            object
# 日期6    datetime64[ns]
# 日期7            object
# 年                int64
# 月                int64
# 日                int64
# dtype: object

df_excel=pd.read_excel("./实验数据/parse_dates.xlsx",sheet_name="Sheet3",parse_dates=[0,1,2,3,4,5,[8,9,10]]) #在指定哪些列要时间机械的时候 同时指定哪几列要合并解析
print(df_excel)    #貌似 “合并列”总是出现在“第一列”
#     年_月_日      日期0      日期1      日期2      日期3      日期4               日期5      日期6          日期7
# 0 2020-01-20 2020-01-20 2020-01-20 2020-01-20 2020-01-20 2020-01-20 2020-01-20 00:10:10 2020-01-20  2020年1月20日
# 1 2020-01-21 2020-01-21 2020-01-21 2020-01-21 2020-01-21 2020-01-21 2020-01-21 00:10:11 2020-01-21  2020年1月21日
print(df_excel.dtypes)
# 年_月_日    datetime64[ns]
# 日期0       datetime64[ns]
# 日期1       datetime64[ns]
# 日期2       datetime64[ns]
# 日期3       datetime64[ns]
# 日期4       datetime64[ns]
# 日期5       datetime64[ns]
# 日期6       datetime64[ns]
# 日期7               object
# dtype: object

df_excel['日期7']=pd.to_datetime(df_excel['日期7'],format='%Y年%m月%d日')
print(df_excel.dtypes)         #可以看到，此时 所有字段都成功解析为时间戳了！
# 年_月_日    datetime64[ns]
# 日期0       datetime64[ns]
# 日期1       datetime64[ns]
# 日期2       datetime64[ns]
# 日期3       datetime64[ns]
# 日期4       datetime64[ns]
# 日期5       datetime64[ns]
# 日期6       datetime64[ns]
# 日期7       datetime64[ns]
# dtype: object


