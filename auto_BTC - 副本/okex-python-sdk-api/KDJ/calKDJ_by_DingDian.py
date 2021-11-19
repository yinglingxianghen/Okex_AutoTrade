# coding:utf8
import traceback
import winsound
import okex.lever_api as lever
import okex.spot_api as spot
import datetime, time
import  itchat

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

# itchat.auto_login()
# my_friend = itchat.search_friends(name = r'重生')
# my_love = my_friend[0].UserName

preK=40.506804
preD=49.187002
preJ=23.146407
lastFen=18

HaveDuo=False
HaveKong=False

lastPrice=0

def getNowPrice():
      try:
            result_xian_BTC = spotAPI.get_specific_ticker('BTC-USDT')
            return float(result_xian_BTC["last"])
      except:
            time.sleep(10)
            return getNowPrice()
def getKXian():
      try:
            return spotAPI.get_kline(instrument_id='BTC-USDT', start='', end='', granularity='180')
      except:
            time.sleep(10)
            return getKXian()

while True:
      try:
            nowPrice=getNowPrice()
            if HaveDuo==True and lastPrice-nowPrice>150:
                  print("亏了，清掉所有的多")
                  HaveDuo=False
            elif HaveKong==True and nowPrice-lastPrice>150:
                  print("亏了，清掉所有的空")
                  HaveKong = False
            kXian = getKXian()
            print(kXian[0])
            if int(kXian[0][0][-10:-8])-lastFen==6 or int(kXian[0][0][-10:-8])-lastFen==-54:
                  next_t = kXian[0][0][:-5].replace('T', ' ')
                  t = time.strptime(next_t, "%Y-%m-%d %H:%M:%S")
                  t = time.mktime(t)
                  sleepTime=t + 28800 + 180+5

                  kNums = kXian[1:10]
                  Low = float(min([i[-3] for i in kNums]))
                  High = float(max([i[2] for i in kNums]))
                  ShouPan=float(kXian[1][-2])
                  RSV = (ShouPan - Low) / (High - Low) * 100
                  K = 2 / 3 * preK + 1 / 3 * RSV
                  D = 2 / 3 * preD + 1 / 3 * K
                  J = 3 * K - 2 * D
                  print(lastFen+3,K,D,J)
                  if D>K>J and J>preJ and D-K<=8:# K<40 and
                        if HaveKong==True:
                              print("清掉所有的空")
                        elif HaveDuo==True and J<preJ:
                              HaveDuo=False
                        elif HaveDuo==True and J>preJ:
                              preK = K
                              preD = D
                              preJ = J
                              lastFen += 3
                              if lastFen == 60:
                                    lastFen = 0
                              print("多等待时间",sleepTime- time.time())
                              time.sleep(sleepTime - time.time())
                              continue

                        print("该多了——" , nowPrice,K,D,J)
                        lastPrice=nowPrice
                        HaveDuo=True
                  if J>K>D and J<preJ and K-D<=8:# K>60 and
                        if HaveDuo==True:
                              print("清掉所有的多")
                        elif HaveKong==True and J>preJ:
                              HaveKong=False
                        elif HaveKong==True and J<preJ:
                              preK = K
                              preD = D
                              preJ = J
                              lastFen += 3
                              if lastFen == 60:
                                    lastFen = 0
                              print("空等待时间", sleepTime - time.time())
                              time.sleep(sleepTime - time.time())
                              continue
                        print("该空了——" , nowPrice,K,D,J)
                        lastPrice = nowPrice
                        HaveKong=True
                  preK=K
                  preD=D
                  preJ=J
                  lastFen += 3
                  if lastFen==60:
                        lastFen=0
                  # print("等待时间", sleepTime - time.time())
                  time.sleep(sleepTime - time.time())

      except:
            print(traceback.format_exc())
            break
