import datetime
from cn_workday import is_workday

start_date_str=input("输入开始时期（时间格式%Y-%m-%d）：")
# start_date_str='2020-10-01'
end_date_str=input("输入结束时期（时间格式%Y-%m-%d）：")
# end_date_str='2020-11-30'
start_date=datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
end_date=datetime.datetime.strptime(end_date_str, '%Y-%m-%d')

a_day=start_date
# print(a_day == end_date)
sum=0
i=1
while a_day != end_date:
    # print(a_day)
    if is_workday(a_day):
        sum+=1
        # print(a_day,"is workday")
    else:
        print(a_day,"is holiday")
    a_day=start_date+datetime.timedelta(days=i)
    i+=1


#最后一天，不在循环中判断，单独判断
if is_workday(end_date):
    sum+=1
    # print(end_date,'is workday')
else:
    print(end_date,'is holiday')
print("工作日共计：",sum,"天")

print("\n\n输入任意键 结束")   #一般，双击模块就会运行 但是运行速度很快（一闪而过），所以加入一个交互式的命名 让代码的执行暂停在这里 这样人眼就能看清输出结果了
input()