import os
from aip import AipOcr
import pandas as pd


#配置AI参数
app_id=''
api_key=''
secret_key=''

#生成AI对象
client=AipOcr(app_id,api_key,secret_key)

#输入图片路径
# path="."
path=input("请输入路径：")

#判断出目标目录下的所有png图片
pic_name_list=[]     #保存图片文件名
def get_all_pics(path):
    files=os.listdir(path)  #读取目录下的文件列表
    for file in files:
        if os.path.isfile(path+"/"+file):
            # print('"' + file + '"' + ">>>>>>是文件")
            filename, extension = os.path.splitext(file)
            if extension == ".png":
                # print('"' + filename + '"' + " 是png图片")
                pic_name_list.append(path+"/"+file)

get_all_pics(path)
print(pic_name_list)  #['./微信图片1.png', './微信图片2.png']



# file_path=path+'/'+pic_name_list[0]
# print(file_path)

#读取图片内容
def get_file_content(file_path):
    with open(file_path,'rb') as fp:
        return fp.read()
#读取图片中的文字
def image2text(file_name):
    image = get_file_content(file_name)
    dic_result = client.basicGeneral(image)
    # print(dic_result)
    res=dic_result['words_result']
    # print(res)  #由字典作为元素构成的列表：[{'words': '美团'}, {'words': '美团金融服务'}, {'words': '-348.16'},...
    result = []   #每张图片的文字信息，都保留在一个列表中
    for i in res :
         # print(i['words'])
         result.append(i['words'])
    # print(result)
    return result

#批量读取图片中的文字信息
pic_words=[]   #所有图片所对应的文字信息 都保存在该二维列表中
for pic in pic_name_list:
    pic_words.append(image2text(pic))
print(pic_words)



df=pd.DataFrame(columns=["服务名称：","金额：","订单号：","公司：","支付时间："])  #声明空数据帧
# print(df)
i=0
for mes in pic_words:   #提取每张图片中的相应数据，并插入数据帧
    df.loc[i]=[mes[1],mes[2],mes[4],mes[5],mes[6]]
    i+=1
print(df)

excel_name= path+'/'+'图片信息汇总表.xlsx'
print(excel_name)
df.to_excel(excel_name)