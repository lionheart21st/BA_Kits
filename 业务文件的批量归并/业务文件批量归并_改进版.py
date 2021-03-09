import os
import re
import pandas as pd

# path = "./source_data"    #为了方便调试，可以将path赋值为当前路径，把该代码模块 放到图片的相同目录中 运行即可
path=input("请输入路径：")

# print(os.listdir(path))   #查看目标目录下的文件

#判断出目标目录下的所有店名
def get_all_shop_name(path):
    shop_name_set = set()   #保存店名   //特别注意：集合set天然去重
    files=os.listdir(path)  #读取目录下的文件列表
    for file in files:
        if os.path.isfile(path+"/"+file):   #判断文件的目的 是为了与子目录相区分
            # print('"' + file + '"' + ">>>>>>是文件")
            filename, extension = os.path.splitext(file)   #分离出文件名与后缀名
            if (extension == ".xlsx") & bool(re.search(r".*?店",filename)): #bool(re.search(r".*?店",filename))提高程序健壮性 //因为 有可能会有Excel文件 文件名中没有“店”这个字，如果 直接re.findall(r".*?店", filename)[0]，报错：IndexError: list index out of range
                shop_name_set.add(re.findall(r".*?店", filename)[0])  #解析出店名 并添加到集合中
    return shop_name_set


# shop_name_set=get_all_shop_name(path)
# print(shop_name_set)

#遍历店名集合，新建店名子目录 并将相应的数据文件放入子目录
def files_merge(shop_name_set):
    df_log=pd.DataFrame(columns=["目录名","文件名"])  #声明空数据帧
    i=0
    for name in shop_name_set:   #读取店名集合
        print(name)
        print(path+"/"+name+'广告销售.xlsx')  #拼接文件路径
        # print(os.path.exists(path+"/"+name+'广告销售.xlsx'))
        if os.path.exists(path+"/"+name+'广告销售.xlsx') and os.path.exists(path+"/"+name+'销售总额.xlsx'):  #判断相应店名的广告销售、销售总额Excel表格文件是否存在
            # print("ok")
            os.mkdir(path+"/"+name)    #以店名 新建子目录
            os.rename(path+"/"+name+'广告销售.xlsx',path+"/"+name+"/"+name+'广告销售.xlsx') #改变目标文件目录 即将目标文件放入相应的子目录中（其实就是在路径上加一层目录）
            os.rename(path + "/" + name + '销售总额.xlsx', path + "/" + name + "/" + name + '销售总额.xlsx') #改变目标文件目录 即将目标文件放入相应的子目录中（其实就是在路径上加一层目录）
            df_log.loc[i]=[path+"/"+name,path+"/"+name+"/"+name+'广告销售.xlsx']  #添加记录到《归并信息汇总.xlsx》
            df_log.loc[i+1] = [path + "/" + name, path + "/" + name + "/" + name + '销售总额.xlsx']#添加记录到《归并信息汇总.xlsx》
            i+=2

    excel_name= path+'/'+'归并信息汇总.xlsx'   #指定《归并信息汇总.xlsx》的路径
    df_log.to_excel(excel_name) #生成《归并信息汇总.xlsx》



if __name__ == "__main__":
    shop_name_set = get_all_shop_name(path)
    files_merge(shop_name_set)
