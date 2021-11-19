#coding:utf8

import winsound
import datetime,time
import okex.swap_api as swap

passphrase = "xxxx"
api_key = "xxxx"
secret_key = "xxxx"
IP = "xxxx"

d={"BTC-USDT-SWAP":[55000,56460],"LTC-USDT-SWAP":[165,237],"ETH-USDT-SWAP":[1480,1980],"DOGE-USDT-SWAP":[0.0495,0.0695]}

def judge_high(kind):
    print(kind+"暴涨了")
    winsound.Beep(1100, 15000)
def judge_low(kind):
    print(kind+"暴跌了")
    winsound.Beep(600, 15000)

swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, False)

def judge_now(kind):
    result_xian = swapAPI.get_specific_ticker(kind)
    now_price = float(result_xian["last"])
    print("\t现价\t\t" + datetime.datetime.now().strftime('%H:%M:%S') + "\t\t\t" + kind.split('-')[0] +  "———" +str(now_price))
    if now_price>=d[kind][1]:
        judge_high(kind)
    elif now_price<=d[kind][0]:
        judge_low(kind)
    time.sleep(60)

while True:
    try:
        judge_now("BTC-USDT-SWAP")
        judge_now("LTC-USDT-SWAP")
        judge_now("ETH-USDT-SWAP")
        judge_now("DOGE-USDT-SWAP")
    except Exception as e:
        print(e)
        # winsound.Beep(1100, 15000)
        time.sleep(60)
