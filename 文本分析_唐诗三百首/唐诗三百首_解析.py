from collections import Counter
import re
import jieba

with open("./唐诗三百首.txt") as f :
    poem_data=f.readlines()  #readlines 注意有“s”结尾，一次性读取文件的所有行，返回一个“字符串 列表”（一行对应一个“字符串元素”）
    # print(poem_data)


name_re=re.compile(r"\d+(.*?)：")

def get_person_count(poem_data,name_re):
    person_count=Counter()
    for data in poem_data:
        if name_re.findall(data) != []:
            person_name=name_re.findall(data)[0]
            person_count=person_count+Counter({person_name:1})
    return person_count

person_count=get_person_count(poem_data,name_re)
# print(person_count)


print("诗人姓名为（排名不计先后）：")
for i in list(person_count):
    print(i,end=" ")
print("\n\n总共 "+str(len(list(person_count)))+"位 诗人")

print("\n数量前十的诗人 分别为：")
pr_list=person_count.most_common(10)
for i in pr_list:
    print(i[0]+" "+str(i[1])+"首")


poem_name_re=re.compile(r'\d+\w+：(\w+)')
poem_content_re=re.compile(r'(\w+)[，|。]')

def poem_analysis(poem_data,poem_re,n):
    list_data=[]
    for data in poem_data:
        if poem_re.findall(data) != []:
            list_data.append(poem_re.findall(data)[0])
    # print(list_data)
    words_list=[]
    for i in list_data:
        words_list.extend(list(jieba.cut(i)))
    # print(words_list)
    words_count=Counter(words_list)
    # print(words_count)
    top_n=words_count.most_common(n)
    # print(top_n)
    return top_n

print("\n\n诗名 前十 高频词汇 分别为：")
top_10=poem_analysis(poem_data,poem_name_re,10)
for i in top_10:
    print(i[0]+" "+str(i[1])+"次")

print("\n\n诗句 前十 高频词汇 分别为：")
top_10=poem_analysis(poem_data,poem_content_re,10)
for i in top_10:
    print(i[0]+" "+str(i[1])+"（加权）次")




