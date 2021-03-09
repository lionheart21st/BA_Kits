import os
import re
import pandas as pd

path = "./source_data"
# path=input("请输入路径：")

# print(os.listdir(path))  #查看目标目录下的文件

#判断出目标目录下的店名
def get_all_shop_name(path):
    shop_name_set = set()  #保存店名
    files=os.listdir(path)  #读取目录下的文件列表
    for file in files:
        if os.path.isfile(path+"/"+file):
            # print('"' + file + '"' + ">>>>>>是文件")
            filename, extension = os.path.splitext(file)
            if (extension == ".xlsx") & bool(re.search(r".*?店",filename)): #bool(re.search(r".*?店",filename))提高程序健壮性
                shop_name_set.add(re.findall(r".*?店", filename)[0])
    return shop_name_set


# shop_name_set=get_all_shop_name(path)
# print(shop_name_set)


def files_merge(shop_name_set):
    df_log=pd.DataFrame(columns=["目录名","文件名"])  #声明空数据帧
    i=0
    for name in shop_name_set:
        print(name)
        print(path+"/"+name+'广告销售.xlsx')
        # print(os.path.exists(path+"/"+name+'广告销售.xlsx'))
        if os.path.exists(path+"/"+name+'广告销售.xlsx') and os.path.exists(path+"/"+name+'销售总额.xlsx'):
            # print("ok")
            os.mkdir(path+"/"+name)
            os.rename(path+"/"+name+'广告销售.xlsx',path+"/"+name+"/"+name+'广告销售.xlsx') #改变目标文件目录
            os.rename(path + "/" + name + '销售总额.xlsx', path + "/" + name + "/" + name + '销售总额.xlsx')#改变目标文件目录
            df_log.loc[i]=[path+"/"+name,path+"/"+name+"/"+name+'广告销售.xlsx']  #添加信息到《归并信息汇总.xlsx》
            df_log.loc[i+1] = [path + "/" + name, path + "/" + name + "/" + name + '销售总额.xlsx']#添加信息到《归并信息汇总.xlsx》
            i+=2

    excel_name= path+'/'+'归并信息汇总.xlsx'
    df_log.to_excel(excel_name)



if __name__ == "__main__":
    shop_name_set = get_all_shop_name(path)
    files_merge(shop_name_set)
