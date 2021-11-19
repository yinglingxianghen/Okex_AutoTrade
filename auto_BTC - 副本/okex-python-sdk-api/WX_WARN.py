#coding:utf8
import winsound
import okex.lever_api as lever
import okex.spot_api as spot
import datetime,time
import itchat

passphrase = "xxxx"
api_key = "xxxx"
secret_key = "xxxx"
IP = "xxxx"

spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
levelAPI = lever.LeverAPI(api_key, secret_key, passphrase, False)


Break=0
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

itchat.auto_login()
my_friend = itchat.search_friends(name = r'重生')
my_love = my_friend[0].UserName

BTC_low=0
BTC_high=10
ETH_low=0
ETH_high=10
while True:
    try:
        result_xian_BTC = spotAPI.get_specific_ticker('BTC-USDT')
        BTC_now_price = float(result_xian_BTC["last"])
        print("\t现价\t\t" + datetime.datetime.now().strftime('%H:%M:%S') + "\t\t\t" + "BTC——" + str(BTC_now_price))
        if not BTC_low<=BTC_now_price<BTC_high:
            BTC_low=BTC_now_price//100*100
            BTC_high=(BTC_now_price//100+1)*100
            itchat.send("大饼——"+str(BTC_now_price), toUserName=my_love)

        # time.sleep(10)
        #
        # result_xian_ETH = spotAPI.get_specific_ticker('ETH-USDT')
        # ETH_now_price = float(result_xian_ETH["last"])
        # print("\t现价\t\t" + datetime.datetime.now().strftime('%H:%M:%S') + "\t\t\t" + "ETH——" + str(ETH_now_price))
        # if not ETH_low<=ETH_now_price<ETH_high:
        #     ETH_low = ETH_now_price//10*10
        #     ETH_high = (ETH_now_price//10+1)*10
        #     itchat.send("以太——"+str(ETH_now_price), toUserName=my_love)

    except Exception as e:
        print(e)

    time.sleep(10)

