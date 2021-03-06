import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.unicode.east_asian_width',True)  #调整“列名与数据的对齐”

##连接数据库
db_info={
    'host':'localhost'
    ,'user':'root'
    ,'password':'123456'
    ,'database':'management_systems'
    ,'charset':'utf8'
}
conn = pymysql.connect(**db_info)


#读取源数据
sql='select * from customer'
data=pd.read_sql(sql,conn)


#索引重新设置
data.set_index('id',inplace=True)
#修改列名
data.columns=['用户id','订单时间','订单数量','订单金额']
#修改字段数据类型
data['订单时间']=data['订单时间'].astype('datetime64')
data['订单数量']=data['订单数量'].astype('int')
data['订单金额']=data['订单金额'].astype('int')

#数据透视表
user_rfm=data.pivot_table(index='用户id'
                          ,values=['订单时间','订单数量','订单金额']
                          ,aggfunc={'订单时间':'max','订单数量':'count','订单金额':'sum'})
#R:以2021-01-01为基准时间 ，计算 距离最近一次消费的天数
user_rfm['距离最近一次消费']=(pd.to_datetime('2021-01-01 00:00:00')-user_rfm['订单时间'])/np.timedelta64(1,'D')
user_rfm=user_rfm.rename(columns={'距离最近一次消费':'R','订单数量':'F','订单金额':'M'})

#RMF模型的用户分类标准
def rfm_func(x):
    level=x.apply(lambda x:'1' if x >=0 else '0')  #大于0 置1，小于0 置0
    label=level.R + level.F + level.M    #根据RFM三个维度进行编码
    d={                       #定义编码对应的标签（含义）
        '111':'高价值客户'
        ,'011':'重点保持客户'
        ,'101':'重点发展客户'
        ,'001':'重点挽留客户'
        ,'110':'一般价值客户'
        ,'010':'一般保持客户'
        ,'100':'一般发展客户'
        ,'000':'潜在客户'
    }
    result=d[label]
    return result
#通过计算 进行用户分类，计算阈值分别为R、M、F的均值
user_rfm['label']=user_rfm[['R','F','M']].apply(lambda x:x-x.mean()).apply(rfm_func,axis=1)


print(user_rfm['label'].head(21))

# print(user_rfm.groupby('label')['label'].count())



#将用户标签数据 保存到数据库中
from sqlalchemy import create_engine  #导入sqlalchemy包
conn = create_engine('mysql+pymysql://root:123456@localhost:3306/management_systems?charset=utf8')
user_rfm=user_rfm.reset_index() #重置索引
user_rfm[["用户id","label"]].to_sql("customer_level", conn, if_exists='replace', index=False)  #if_exists的值改为'replace'，反复运行也是247行




#绘图
font={
    "family":"SimHei"
    ,"size":20
}
plt.rc('font',**font)
plt.figure(figsize=(20,10))
plt.pie(user_rfm.groupby('label').count()['F']
        ,labels=['一般保持客户','一般发展客户','潜在客户','重点保持客户','重点发展客户','重点挽留客户','高价值客户']
        ,autopct='%.2f%%'
        ,explode=(0,0,0,0.1,0.3,0.3,0.5))
plt.title('基于RFM模型的用户分类占比')
plt.show()