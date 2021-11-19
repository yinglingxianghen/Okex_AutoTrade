# coding:utf8
import traceback
import winsound
import okex.lever_api as lever
import okex.spot_api as spot
import datetime, time
import  itchat
itchat.auto_login()
my_friend = itchat.search_friends(name = r'重生')
my_love = my_friend[0].UserName

passphrase = "xxxx"
api_key = "xxxx"
secret_key = "xxxx"
IP = "xxxx"

spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
# levelAPI = lever.LeverAPI(api_key, secret_key, passphrase, False)

'''
当日RSV=（Ct收盘价－L9最低）÷（H9最高－L9最低）×100
当日K值=2/3×前一日K值+1/3×当日RSV
当日D值=2/3×前一日D值+1/3×当日K值
若无前一日K 值与D值，则可分别用50来代替。
J值=3*当日K值-2*当日D值
                                    开盘价格   最高价格 	最低价格 	 收盘价格 	交易量
'''
Ls = [['2021-01-07T08:55:00.000Z', '37217', '37260.6', '37170', '37204.6', '42.7624588'],
      ['2021-01-07T08:50:00.000Z', '37272', '37324.3', '37213.1', '37217', '57.63380553'],
      ['2021-01-07T08:45:00.000Z', '37216', '37346.9', '37121', '37275.6', '79.65638403'],
      ['2021-01-07T08:40:00.000Z', '37036.9', '37232.2', '37011.2', '37215.9', '94.81103458'],
      ['2021-01-07T08:35:00.000Z', '36929.8', '37035', '36929.8', '37035', '35.71941604'],
      ['2021-01-07T08:30:00.000Z', '36876.6', '36964.1', '36811', '36929.8', '72.07464176'],
      ['2021-01-07T08:25:00.000Z', '36514.3', '36899.6', '36514.3', '36870.3', '83.70254863'],
      ['2021-01-07T08:20:00.000Z', '36512.7', '36639.8', '36300', '36519.1', '144.91225086'],
      ['2021-01-07T08:15:00.000Z', '36842.6', '36850.4', '36505', '36512.6', '135.94234877']]

# Low = float(min([i[-2] for i in Ls]))
# High = float(max([i[-2] for i in Ls]))
# Now = 37250
# RSV = (Now - Low) / (High - Low) * 100
# K = 2 / 3 * 86.17 + 1 / 3 * RSV
# D = 2 / 3 * 75.475 + 1 / 3 * K
# J = 3 * K - 2 * D

preK=43.585077
preD=51.708523
lastFen=1
Haved=False
status=1
while True:
      try:
            kXian = spotAPI.get_kline(instrument_id='BTC-USDT', start='', end='', granularity='60')
            # print(len(kXian))
            # print(kXian[0])
            if int(kXian[0][0][-10:-8])-lastFen==2 or int(kXian[0][0][-10:-8])-lastFen==-58:
                  kNums = kXian[1:22]
                  # print(kNums)
                  Low = float(min([i[-3] for i in kNums]))
                  High = float(max([i[2] for i in kNums]))
                  ShouPan=float(kXian[1][-2])
                  RSV = (ShouPan - Low) / (High - Low) * 100
                  preK = 2 / 3 * preK + 1 / 3 * RSV
                  preD = 2 / 3 * preD + 1 / 3 * preK
                  preJ = 3 * preK - 2 * preD

                  if 20<preK<80:
                        Haved=False
                  # RSV = (float(kXian[0][-2]) - Low) / (High - Low) * 100
                  # K = 2 / 3 * preK + 1 / 3 * RSV
                  # D = 2 / 3 * preD + 1 / 3 * K
                  # J = 3 * K - 2 * D
                  print(str(lastFen+1)+"","K——",round(preK,6),"D——",round(preD,6),"J——",round(preJ,6))
                  # print(str(lastFen+2)+" 现在","K——",round(K,6),"D——",round(D,6),"J——",round(J,6))
                  if Haved==False and preK>80 and preK-preD<5:
                        time.sleep(5)
                        result_xian_BTC = spotAPI.get_specific_ticker('BTC-USDT')
                        BTC_now_price = result_xian_BTC["last"]
                        if status==1:
                              print("平掉所有的多")
                        print("该空了——"+BTC_now_price)
                        itchat.send("该空了——"+BTC_now_price, toUserName=my_love)
                        Haved=True
                        status=0
                  elif Haved==False and preK<20 and preD-preK<5:
                        time.sleep(5)
                        result_xian_BTC = spotAPI.get_specific_ticker('BTC-USDT')
                        BTC_now_price = result_xian_BTC["last"]
                        if status==0:
                              print("平掉所有的空")
                        print("该多了——"+BTC_now_price)
                        itchat.send("该多了——"+BTC_now_price, toUserName=my_love)
                        Haved=True
                        status=1
                  lastFen += 1
                  if lastFen==60:
                        lastFen=0
      except:
            print(traceback.format_exc())
      time.sleep(20)


