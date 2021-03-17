import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  #用来实现 邮件带附件 //附件可以是文档 也可以是图片 等等
from email.mime.image import MIMEImage   #用来实现正文带图片  //需要 MIMEImage来生成图片对象，来嵌入到“html页”中
import getpass

import pandas as pd
import matplotlib.pyplot as plt


def send_mail(email_name:str      #注意： 形参:指定数值类型   #这里 形参比较多，所以“竖”着写
              ,pas:str
              ,msg_to:list
              ,subject:str
              ,content:str
              ,image_html:bool=False   #我的理解：image_html是一个标签位，False就是表示 正文（内容）是普通文本，True就表示 正文（内容）是“html页” 图片、文本内容就嵌在“html页”中
              ,image_path:dict=None
              ,acc_to:list=None   #注意： 形参:指定数值类型=啥啥啥  形参默认值  #有了默认值，函数调用的时候 实参可以不用传
              ,att_file:list=None
              ,from_name:str=None
              )->bool:  # ->bool 表示返回值类型是布尔值
    """
    :param email_name:发送者邮箱
    :param pas:发送者邮箱pas
    :param msg_to:收件人邮箱列表，参数类型是列表
    :param subject:邮件主题，字符串类型
    :param content:邮件内容，字符串类型
    :param image_html:布尔值，默认为True，如果为True则意味着包含图片
    :param image_path:图片路径，字典类型{'图片id':'图片路径'},默认为空，这个参数只有在image_html为True的才生效
    :param acc_to:抄送人邮箱列表，参数类型是列表，默认值是None
    :param att_file:附件列表，参数类型是列表，默认值是None
    :param from_name:显示发件人的名字，字符串类型，默认值是None
    :return:成功返回True 失败返回False
    """
    msg = MIMEMultipart()  # 生成邮件对象，该对象可以包含附件 并且包含多样式内容

    # 邮件正文内容
    # 判断邮件正文是带图片（即html）形式，还是普通文本形式
    if image_html:  # 条件相当于 image_html==True
        msg.attach(MIMEText(content, 'html', 'utf-8'))  # 将邮件正文 以“html”的形式 添加到msg对象中
        for image_id, image_path in image_path.items():  # 读取 图片字典中的key、value
            file = open(image_path, 'rb')  # 打开图片文件 读取图片信息
            img_data = file.read()
            file.close()  # 读取之后 关闭图片文件
            img = MIMEImage(img_data)  # 生成图片对象
            img.add_header("Content-ID",
                           image_id)  # 将图片字典中的key 写入“图片头” //我的理解：key的作用，在html的“src='cid:imageid”的对应位置 嵌入图片
            msg.attach(img)  # 将图片对象 添加到msg对象中
    else:  # 如果 邮件正文是普通形式（即文本），“直接”添加邮件正文 到msg对象中
        msg.attach(MIMEText(content))

    # 设置邮件
    msg['Subject'] = subject
    msg['From'] = from_name
    msg['To'] = ";".join(msg_to)
    msg['Cc'] = ";".join(acc_to)

    # 判断是否包含附件
    if len(att_file) > 0:  # len(att_file) >0 就说明有附件
        for file in att_file:  # 加载 附件列表中的所有附件
            print("加载附件" + file)
            # 获取文件名
            file_name_list = file.split('/')  # 注意：file保存的是“带路径文件名”
            file_number = len(file.split('/')) - 1
            file_name = file_name_list[file_number]  # 切出“文件名本身”

            att = MIMEText(open(file, 'rb').read(), 'plain', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att.add_header("Content-Disposition", 'attachment', filename=('gbk', "", file_name))
            msg.attach(att)

    s = smtplib.SMTP('smtp.189.cn', 25)
    # 登录发件人的邮箱
    s.login(email_name, pas)  # “自己”
    # 发送邮件
    s.sendmail(email_name, msg_to + acc_to, msg.as_string())
    s.quit()  # 断开smtp连接

    print("邮件发送成功")



###
content="""
<html>
    <body>
        <h1>聚类分析</h>
        <p>线性回归</p>
        <img src='cid:imageid' alt='imageid'>  
        <p>K近邻</p>          
        <img src='cid:imageid2' alt='imageid2'>
        <p>K近邻_鸠尾花</p>          
        <img src='cid:imageid3' alt='imageid2'>
        <p>KMeans_1_1</p>          
        <img src='cid:imageid4' alt='imageid2'>
        <p>KMeans_1_2</p>          
        <img src='cid:imageid5' alt='imageid2'>
        <p>KMeans_2_1</p>          
        <img src='cid:imageid6' alt='imageid2'>
        <p>KMeans_2_2</p>          
        <img src='cid:imageid7' alt='imageid2'>
        <p>日PV</p>          
        <img src='cid:imageid8' alt='imageid2'>
        <p>日UV</p>          
        <img src='cid:imageid9' alt='imageid2'>
        <p>每小时PV</p>          
        <img src='cid:imageid10' alt='imageid2'>
        <p>每小时UV</p>          
        <img src='cid:imageid11' alt='imageid2'>
        <p>用户行为漏斗</p>          
        <img src='cid:imageid12' alt='imageid2'>
    </body>
</html>
"""
#特别注意：html中 不能写Python注释 #，否则Python注释会当做内容 显示在“html页”中
#alt是局部属性，尽可以用在img、input等元素中，提供在图片为载入或加载失败时的替代文本
#p标签是换行

image_path={
    "imageid":"./线性回归.png"
    ,"imageid2":"./K近邻.png"
    ,"imageid3":"./K近邻_鸠尾花.png"
    ,"imageid4":"./KMeans_1_1.png"
    ,"imageid5":"./KMeans_1_2.png"
    ,"imageid6":"./KMeans_2_1.png"
    ,"imageid7":"./KMeans_2_2.png"
    ,"imageid8":"./日PV.png"
    ,"imageid9":"./日UV.png"
    ,"imageid10":"./每小时PV.png"
    ,"imageid11":"./每小时UV.png"
    ,"imageid12":"./用户行为漏斗.png"

}

#发件人的邮箱名称
email_name = "18012613680@189.cn"
#发件人的邮箱pas
pas=getpass.getpass("请输入：")
#收件人列表
msg_to=["sg513208@mail.ustc.edu.cn"]
#邮件主题
subject= '邮件自动发送'

#抄送列表
acc_to=["237725015@qq.com"]
#附件列表
att_file=["./线性回归.png","./K近邻.png","./K近邻_鸠尾花.png","./KMeans_1_1.png","./KMeans_1_2.png","./KMeans_2_1.png","./KMeans_2_2.png","./线性回归.py","./K近邻.py","./K近邻_鸠尾花.py","./KMeans.py"
          ,"./日PV.png","./日UV.png","./每小时PV.png","./每小时UV.png","./用户行为漏斗.png"]  #注意：这里的图片是附件图片，与正文图片 即“html页”中嵌入图片，是两回事！
#“显示”发件人名称
from_name='来恩哈特189'

###调用函数   ##特别注意:因为 形参赋值与函数调用解耦，所以 函数调用的时候 看起来特别清晰
send_mail(email_name=email_name,pas=pas
          ,msg_to=msg_to
          ,subject=subject
          ,content=content
          ,image_html=True
          ,image_path=image_path
          ,acc_to=acc_to
          ,att_file=att_file
          ,from_name=from_name
         )