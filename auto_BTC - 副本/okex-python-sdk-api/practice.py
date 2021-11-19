import time,json
nowPendDict={"a":1,"b":2,"c":0.1}
sortedPendDict = sorted(nowPendDict.items(), key=lambda x: x[1])
print(sortedPendDict)
print("-----------------------------------------------------------------")
num=1
# while True:
#     num+=1
#     print(num)
#     if num>4:
#         continue
#     time.sleep(3)

list0=[1,2,3,"4","5"]
list0.remove("4")
print(list0)
instrument='BTC-USD-210108-'+str(18956//500*500)+'-P'
print(instrument)

# while True:
#
#     print("现在盈利率:", a / b)
#
#
#     a,b=1,2
#     time.sleep(4)
print(298//250*250)
print(float('1'))
a='12345'
b=[1,2,3,4,5]
print(b[1:3])
print(round(12.3456123323,6))

import time
t = "2020-10-31 12:44:27"
t1 ="2021-01-18T08:57:00.000Z"
print(t1[:-5].replace('T',' '))
# 将字符串形式的时间转换为时间元组
t = time.strptime(t, "%Y-%m-%d %H:%M:%S")
# 将时间元组转换为时间戳
t = time.mktime(t)
# 1604119467.0
print(t)
aa='asdf'
print(eval('aa'))

