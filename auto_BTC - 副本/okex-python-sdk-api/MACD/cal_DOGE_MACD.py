# coding:utf8
import traceback
import winsound
import okex.lever_api as lever
import okex.spot_api as spot
import datetime, time
import itchat
import okex.swap_api as swap

passphrase = "xxxx"
api_key = "xxxx"
secret_key = "xxxx"
IP = "xxxx"

swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, False)
# result_xian = swapAPI.get_specific_ticker("BTC-USDT-SWAP")
# now_price = float(result_xian["last"])
# print(now_price)
'''
EMA（12）= 前一日EMA（12）×11/13＋今日收盘价×2/13   55843.4*11/13+55920.4*2/13=55855.24615384615
EMA（26）= 前一日EMA（26）×25/27＋今日收盘价×2/27   55674*25/27+55920.4*2/27=55692.25185185185
DIFF=今日EMA（12）- 今日EMA（26）                 上-下=162.99430199430208
DEA（MACD）= 前一日DEA×8/10＋今日DIFF×2/10         195.1*0.8+163*0.2=188.68
BAR=2×(DIFF－DEA)                              2*(163-188)=-51.37139601139586
                                    开盘价格   最高价格 	最低价格 	 收盘价格 	交易量
'''

def get_macd(qEMA12,qEMA26,qDEA,qBAR,instrument_id,sleeptime):
    def getNowPrice():
        try:
            result_xian = swapAPI.get_specific_ticker(instrument_id)
            now_price = float(result_xian["last"])
            return now_price
        except:
            time.sleep(5)
            return getNowPrice()
    qEMA12=qEMA12
    qEMA26=qEMA26
    qDEA=qDEA
    qBAR=qBAR

    DiffList=[]
    First=True
    while True:
        try:
            result = swapAPI.get_kline(instrument_id=instrument_id, start='', end='', granularity='180')
        except:
            time.sleep(10)
            continue
        # print(result[0],datetime.datetime.now())
        if First!=True:
            if int(result[0][0][14:16]) != datetime.datetime.now().minute:
                time.sleep(8)
                continue

        First=False
        Shou=float(result[1][-3])

        EMA12= qEMA12*11/13+Shou*2/13
        EMA26= qEMA26*25/27+Shou*2/27
        DIFF=EMA12-EMA26
        DEA= qDEA*8/10+DIFF*2/10
        BAR=2*(DIFF-DEA)
        print(result[1][0][14:16] + "分的:", DIFF, DEA, BAR)
        if len(DiffList)>1:
            if DiffList[-1]<DiffList[-2] and DiffList[-1]<DIFF:
                print("金叉了",getNowPrice())
                winsound.Beep(1600, 600)

            elif  DiffList[-1]>DiffList[-2] and DiffList[-1]>DIFF:
                print("死叉了",getNowPrice())
                winsound.Beep(600, 600)
            DiffList.pop(0)

        DiffList.append(DIFF)
        qEMA12 = EMA12
        qEMA26 = EMA26
        qDEA = DEA
        qBAR=BAR
        sleepTime=190-int(time.time())%180
        # print("等",sleepTime,"秒")
        time.sleep(sleepTime+sleeptime)

if __name__ == '__main__':

    get_macd(0.135029,0.136233,-0.000476,-1,'DOGE-USDT-SWAP',0)
