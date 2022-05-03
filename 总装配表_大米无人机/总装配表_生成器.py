#coding:utf-8
import os
import re
import pandas as pd
from sqlalchemy import create_engine
import pymysql

db = pymysql.connect(
    host = '',
    port = 3306,
    user = '',
    password = '',
    charset = 'utf8',
    database = ''
)

cur = db.cursor()
engine = create_engine('mysql+pymysql://root:@localhost:3306/coco_test?charset=utf8')



path = r"C:\Users\Dell\PycharmProjects\pythonProject3\总装配表_大米无人机"    #为了方便调试，可以将path赋值为当前路径，把该代码模块 放到图片的相同目录中 运行即可
# path=input("请输入路径：")
# print(os.listdir(path))   #查看目标目录下的文件

#从目标目录中读取产品文件，并合成一张 产品_配件表
def get_all_product_data(path):
    df_data1 = pd.DataFrame(columns=["产品", "配件", "标准版", "畅飞版", "至尊版"])  # 新建一个“空df” //该df 用来存放“批量处理的数据结果”：“多个Excel表中的数据，汇总保存
    df_data2 = pd.DataFrame(columns=["产品", "配件", "标准版", "畅飞版", "至尊版"])
    # print(df_data)
    files=os.listdir(path)  #读取目录下的文件列表
    for file in files:
        if os.path.isfile(path+"/"+file):   #判断文件的目的 是为了与子目录相区分
            # print('"' + file + '"' + ">>>>>>是文件")
            filename, extension = os.path.splitext(file)   #分离出文件名与后缀名
            if (extension == ".xlsx") :
                # print(path+"/"+filename+".xlsx")
                df1 = pd.read_excel(path+"/"+filename+".xlsx")   #不处理 合并单元格
                df_data1=pd.concat([df_data1,df1])
                df2 = pd.read_excel(path+"/"+filename+".xlsx").fillna(method='pad')  #fillna(method='pad')处理“合并单元格”
                df_data2=pd.concat([df_data2,df2])
    print(df_data1)
    print(df_data2)
    cur.execute("drop table if exists 产品_配件表_预处理1")
    df_data1.to_sql("产品_配件表_预处理1", engine, index=False)  ###mysql数据表
    cur.execute("drop table if exists 产品_配件表_预处理2")
    df_data2.to_sql("产品_配件表_预处理2", engine, index=False)  ###mysql数据表

    sql_1= """create table 产品_配件表 (
    with table1 as (
    select *
    ,row_number() over() as 编号 -- 读取的数据是一样的，所以 编号也是一样的
    from 产品_配件表_预处理1    -- 第一遍读取  不填充(默认模式)
    )
    ,table2 as (
    select *
    ,row_number() over() as 编号  -- 读取的数据是一样的，所以 编号也是一样的
    from 产品_配件表_预处理2   -- 第二遍读取  填充(“method='pad')
    )

    select b.产品,a.配件,a.标准版,a.畅飞版,a.至尊版 -- ,a.编号       //分别读取 产品字段与其他字段(来自不同的表)
    from table1 a 
    left join table2 b 
    on  a.编号=b.编号   -- 编号作为连接条件
    )"""

    cur.execute("drop table if exists 产品_配件表")
    cur.execute(sql_1)
    return 0


#批量拼接(部分)SQL语句，为行转列做准备
def generate_spec_codes_pre():
    sql1="""create table 产品_配件_字符串 (
    with table1 as (  -- 产品_配件表的所有配件种类
    select distinct 配件  
    from 产品_配件表 
    ) 
    select concat(',max(case when 配件="',配件,'"then 规格 else 0 end) as'," ",'"',配件,'"') as 字符串   -- 批量拼接SQL(case_when_聚合)语句 为行转列做准备 #每种配件都有一行“字符串”
    from table1 
    )"""
    cur.execute("drop table if exists 产品_配件_字符串")
    cur.execute(sql1)
    cur.execute("select * from 产品_配件_字符串")
    semi_sql_codes = cur.fetchall() #将批量拼接的字符串 保存到 元组semi_sql_codes中
    # print(semi_sql_codes)
    # print(type(semi_sql_codes)) #<class 'tuple'>
    return semi_sql_codes

#生成指定规格的产品_配件表，如 产品_配件_标准版、产品_配件_畅飞版、产品_配件_至尊版
def generate_product_spec_data(spec,semi_sql_codes): #形参spec是specification的缩写 表示规格
    spec_words=" "+spec+" "

    sql_s1 = "create table 产品_配件_"+spec+" ( select 产品,\""+spec+"\" as 规格"  #spec是specification的缩写 表示规格
    # print(sql_s1)

    sql_s = ""
    i = 0
    while i < len(semi_sql_codes ):
        code_i=semi_sql_codes[i][0]
        # print(code_i)
        code_i=re.sub(" 规格 ",spec_words,code_i)
        # print(code_i)
        sql_s = sql_s + code_i
        # print(sql_s + code_i)
        i += 1
    # print(sql_s)

    sql_s2 = """
    from 产品_配件表
    group by 产品
    )"""
    #
    s_sql = sql_s1 + sql_s + sql_s2
    # print(s_sql)
    cur.execute("drop table if exists " + "产品_配件_" + spec)
    cur.execute(s_sql)
	return 0

#生成不同规格的产品_配件表(如 产品_配件_标准版、产品_配件_畅飞版、产品_配件_至尊版),并且合并为 产品_配件_规格_总表
def generate_data_union(spec_list,semi_sql_codes):
    for i in spec_list:
        # print(i)
        generate_product_spec_data(i,semi_sql_codes)


    sql_s1 = "create table 产品_配件_规格_总表 ( "

    sql_s = ""
    i = 0
    while i < len(spec_list):
        # print(spec_list[i])
        if i == 0:
            sql_s = sql_s + "select * from 产品_配件_" + spec_list[i]
            i += 1
        else:
            sql_s = sql_s + " union select * from 产品_配件_" + spec_list[i]
            i += 1
    # print(sql_s)

    sql_s2 = ")"
    s_sql = sql_s1 + sql_s + sql_s2
    print(s_sql)

    cur.execute("drop table if exists " + "产品_配件_规格_总表")
    cur.execute(s_sql)
	return 0


if __name__ == "__main__":
    product_name_set = get_all_product_data(path)
    semi_sql_codes=generate_spec_codes_pre()
    # generate_spec_codes("标准版", semi_sql_codes)
    generate_data_union(["标准版", "畅飞版", "至尊版"],semi_sql_codes)



"""
select 产品,规格,AiR飞行器,Mini飞行器,经纬飞行器,前后下感知系统,前后上下感知系统,全向感知系统,航空级感知系统
,`3轴机械云台`,PayloadSDK云台,`1200万像素摄像头`,`2000万像素摄像头`,`4800万像素摄像头`,`30倍光学变焦传感器`,热成像传感器,激光测距 `10公里图传`,`12公里图传`,`15公里图传`
,遥控器,带屏遥控器,建模软件,航线规划软件,IP45防水
,`2200毫安电池`,`3500毫安电池`,`6000毫安电池`,充电器,双向充电管家
,小电机,小电机,大电机,大桨叶,小桨叶,大桨叶保护罩,小桨叶保护罩,扩展卡扣,单肩包,工具包,探照灯,喊话器
from 产品_配件_规格_总表
order by 产品,规格
"""