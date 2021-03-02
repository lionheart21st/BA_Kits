import os
from aip import AipOcr
import pandas as pd


#配置AI参数(访问鉴权)    
config={'appId':''
        ,'apiKey':''
        ,'secretKey':''
}
#关键字参数的先行赋值 //因为是使用关键字参数（不是使用位置参数），所以需要对AipOcr函数的参数有准确的了解

#生成AI对象
client=AipOcr(**config)  #通过“逆向收集传参”

#输入图片路径
#path="."    #为了方便调试，可以将path赋值为当前路径，把该代码模块 放到图片的相同目录中 运行即可
path=input("请输入路径：")

#判断出目标目录下的所有png图片
def get_all_pics(path):
    pic_name_list = []  #保存图片文件名
    files=os.listdir(path)  #读取目录下的文件列表
    for file in files:
        if os.path.isfile(path+"/"+file):
            # print('"' + file + '"' + ">>>>>>是文件")
            filename, extension = os.path.splitext(file)
            if extension == ".png":
                # print('"' + filename + '"' + " 是png图片")
                pic_name_list.append(path+"/"+file)
    return pic_name_list

# pic_name_list = get_all_pics(path)   #这两行用于调试
# print(pic_name_list)  #['./微信图片1.png', './微信图片2.png']


#读取图片内容
def get_file_content(file_path):
    with open(file_path,'rb') as fp:
        return fp.read()
#读取图片中的文字
def image2text(file_name):
    image = get_file_content(file_name)     #调用自己定义的get_file_content函数，读取图片内容
    image_data = client.basicGeneral(image) #调用百度AI结构 处理图片内容
    # print(image_data) #{'words_result': [{'words': '美团'}, {'words': '美团金融服务'}, {'words': '-348.16'}, {'words': '当前状态支付成功'}, {'words': '美团订单210227101000000000061540'}, {'words': '商户全称重庆有限公司'}, {'words': '支付时间2021-022718:5728'}, {'words': '支付方式零钱'}, {'words': '交易单号42000008982021'}, {'words': '商户单号210227101000'}, {'words': '发起群收款'}, {'words': '在此商户的交易账单'}], 'log_id': 1366586240970784768, 'words_result_num': 12}
    image_words=image_data['words_result']  #按照key 提取所需要的信息
    # print(image_words)  #由字典作为元素构成的列表：[{'words': '美团'}, {'words': '美团金融服务'}, {'words': '-348.16'},...
    text = []   #每张图片的文字信息，都保留在一个列表中
    for i in image_words :
         # print(i['words'])
         text.append(i['words'])
    # print(text)
    return text

#批量读取图片中的文字信息
def batch_image_parse(pic_name_list):
    images_infos=[]   #所有图片所对应的文字信息 都保存在该二维列表中
    for pic in pic_name_list:
        images_infos.append(image2text(pic))
    return  images_infos

# images_infos=batch_image_parse(pic_name_list)  #这两行用于调试
# print(images_infos) #[['美团', '美团金融服务', '-348.16', '当前状态支付成功', '美团订单210227101000000000061540', '商户全称重庆有限公司', '支付时间2021-022718:5728', '支付方式零钱', '交易单号42000008982021', '商户单号210227101000', '发起群收款', '在此商户的交易账单'], ['美团', '美团金融服务', '-888.16', '当前状态支付成功', '美团订单210227101000000000061546', '商户全称重庆有限公司', '支付时间2021-022718:5728', '支付方式零钱', '交易单号42000008982028', '商户单号21022710100000000002', '发起群收款', '在此商户的交易账单']]


def infos_to_excel(images_infos):
    df=pd.DataFrame(columns=["服务名称：","金额：","订单号：","公司：","支付时间："])  #声明空数据帧
    # print(df)
    i=0
    for mes in images_infos:   #提取每张图片中的相应数据，并插入数据帧 作为其中一行
        df.loc[i]=[mes[1],mes[2],mes[4],mes[5],mes[6]]
        i+=1
    print(df)

    excel_name= path+'/'+'图片信息汇总表.xlsx'
    print(excel_name)      # ./图片信息汇总表.xlsx
    df.to_excel(excel_name)


if __name__ == "__main__" :
    pic_name_list = get_all_pics(path)
    images_infos = batch_image_parse(pic_name_list)
    infos_to_excel(images_infos)
