#coding:utf8
import winsound
import okex.lever_api as lever
import okex.spot_api as spot
import datetime,time
import itchat
import okex.swap_api as swap

passphrase = "xxxx"
api_key = "xxxx"
secret_key = "xxxx"
IP = "xxxx"

spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
levelAPI = lever.LeverAPI(api_key, secret_key, passphrase, False)

BTC_low =30000
BTC_high=293500

ETH_low=720
ETH_high=757


# LTC_low=60
# LTC_high=119

# BCH_low=3
# BCH_high=3750

Break=0
def namestr(obj, namespace):
 return [name for name in namespace if namespace[name] is obj]
def judge_high(kind):
    global Break
    print("---------------------------------------------------------------" + datetime.datetime.now().strftime('%H:%M:%S')
        +"------"+ namestr(kind,globals())[0]+"------" + str(kind)+"--------------------------------------------------")
    winsound.Beep(1100, 15000)
    Break=1
def judge_low(kind):
    global Break
    print("---------------------------------------------------------------" + datetime.datetime.now().strftime('%H:%M:%S')
        +"------"+ namestr(kind,globals())[0]+"------" + str(kind)+"--------------------------------------------------")
    winsound.Beep(400, 15000)
    Break=1


swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, False)
result = spotAPI.get_specific_ticker('BTC-USDT')
print(float(result['last']))
exit()
while True:
    try:
        result_xian = spotAPI.get_specific_ticker('BTC-USDT')
        BTC_now_price = float(result_xian["last"])
        time.sleep(3)
        # result_xian = spotAPI.get_specific_ticker('ETH-USDT')
        # ETH_now_price = float(result_xian["last"])
        # result_xian = spotAPI.get_specific_ticker('LTC-USDT')
        # LTC_now_price = float(result_xian["last"])
        # result_xian = spotAPI.get_specific_ticker('BCH-USDT')
        # BCH_now_price = float(result_xian["last"])
        # print("\t现价\t\t"+datetime.datetime.now().strftime('%H:%M:%S')+"\t\t\t"+"BTC——"+str(BTC_now_price)+"\t\t\t"+"ETH——"+str(ETH_now_price)
        #       +"\t\t\t"+"LTC——"+str(LTC_now_price)+"\t\t\t"+"SUSHI——"+str(SUSHI_now_price)+"\t\t\t"+"BCH——"+str(BCH_now_price)+"\t\t\t"+"XRP——"+str(XRP_now_price)+"\t\t\t")
        print("\t现价\t\t" + datetime.datetime.now().strftime('%H:%M:%S') + "\t\t\t" + "BTC——" + str(
            BTC_now_price)+"\t\t\t"+"ETH——")#str(ETH_now_price)

        # if LTC_now_price>=LTC_high:
        #     judge_kind(LTC_high)
        # elif LTC_now_price<=LTC_low:
        #     judge_kind(LTC_low)

        if BTC_now_price>=BTC_high:
            judge_high(BTC_high)
        elif BTC_now_price<=BTC_low:
            judge_low(BTC_low)
        # elif ETH_now_price>=ETH_high:
        #     judge_high(ETH_high)
        # elif ETH_now_price<=ETH_low:
        #     judge_low(ETH_low)
        # elif BCH_now_price>=BCH_high:
        #     judge_kind(BCH_high)
        # elif BCH_now_price<=BCH_low:
        #     judge_kind(BCH_low)
        if Break==1:
            break
    except Exception as e:
        print(e)
    time.sleep(10)


