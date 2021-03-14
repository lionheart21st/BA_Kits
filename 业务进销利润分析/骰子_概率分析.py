import random

#投掷一颗骰子（1000次）的概率分析
print("投掷一颗骰子（1000次）的各点数概率分析:")
num1=[] #结果集
times=1000
for i  in range(0,times):
    num1.append(random.randint(1,6))
# print(num1)
print("1点的概率：\t",num1.count(1)/times,"\t:","#"*int((num1.count(1)/times)*100))
print("2点的概率：\t",num1.count(2)/times,"\t:","#"*int((num1.count(2)/times)*100))
print("3点的概率：\t",num1.count(3)/times,"\t:","#"*int((num1.count(3)/times)*100))
print("4点的概率：\t",num1.count(4)/times,"\t:","#"*int((num1.count(4)/times)*100))
print("5点的概率：\t",num1.count(5)/times,"\t:","#"*int((num1.count(5)/times)*100))
print("6点的概率：\t",num1.count(6)/times,"\t:","#"*int((num1.count(6)/times)*100))

print()

#投掷两颗颗骰子（1000次）的概率分析
print("投掷两颗骰子（1000次）的各点数概率分析:")
num2=[]  #结果集
times=1000
for i  in range(0,times):
    num2.append(random.randint(1,6)+random.randint(1,6))
# print(num2)
print("1点的概率：\t",num2.count(1)/times,"\t:","#"*int((num2.count(1)/times)*100))
print("2点的概率：\t",num2.count(2)/times,"\t:","#"*int((num2.count(2)/times)*100))
print("3点的概率：\t",num2.count(3)/times,"\t:","#"*int((num2.count(3)/times)*100))
print("4点的概率：\t",num2.count(4)/times,"\t:","#"*int((num2.count(4)/times)*100))
print("5点的概率：\t",num2.count(5)/times,"\t:","#"*int((num2.count(5)/times)*100))
print("6点的概率：\t",num2.count(6)/times,"\t:","#"*int((num2.count(6)/times)*100))
print("7点的概率：\t",num2.count(7)/times,"\t:","#"*int((num2.count(7)/times)*100))
print("8点的概率：\t",num2.count(8)/times,"\t:","#"*int((num2.count(8)/times)*100))
print("9点的概率：\t",num2.count(9)/times,"\t:","#"*int((num2.count(9)/times)*100))
print("10点的概率：\t",num2.count(10)/times,"\t:","#"*int((num2.count(10)/times)*100))
print("11点的概率：\t",num2.count(11)/times,"\t:","#"*int((num2.count(11)/times)*100))
print("12点的概率：\t",num2.count(12)/times,"\t:","#"*int((num2.count(12)/times)*100))