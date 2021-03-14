import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import  Circle

###基于 蒙特卡罗 方法，计算圆周率
def Monte_Carlo_Pi(num=10000,radius=1.0): #num表示“点数”，radius表示半径
    r=radius
    a,b=(0.0,0.0) #原点坐标
    xmin, xmax = a - r, a + r  #x轴取值范围
    ymin, ymax = b - r, b + r  #y轴取值范围

    #在取值范围内 随机打点 //默认1万点
    x = np.random.uniform(xmin, xmax,num)
    y = np.random.uniform(ymin, ymax,num)

    #计算随机点到圆心的距离
    distance = np.sqrt((x - a) ** 2 + (y - b) ** 2)

    #记数 圆点的随机点
    count_in = sum(np.where(distance < r, 1, 0))

    #蒙特卡罗 算法：  内切圆与正方形面积之比 4:Pi
    Pi = 4*count_in/num  #这里使用仿真计算：以点数之比 代替 面积之比
    print("仿真模型计算的圆周率为：",Pi)

    #绘图
    fig=plt.figure(figsize=(6,6))
    axes=fig.add_subplot(1,1,1)
    axes.plot(x, y, 'ro', markersize=1)
    plt.axis('equal')

    circle = Circle(xy=(a, b), radius=r, alpha=0.5)   #圆心为(0,0),半径为r,透明度0.5
    axes.add_patch(circle) #在矩形上 叠加圆形
    plt.show()



if __name__ == "__main__" :
    Monte_Carlo_Pi()