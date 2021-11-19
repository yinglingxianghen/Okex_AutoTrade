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

preK=61.1630
preD=70.1845

First=True
while True:
    try:
        kXian = swapAPI.get_kline(instrument_id='FIL-USDT-SWAP', start='', end='', granularity='180')
    except:
        time.sleep(10)
        continue
    print(kXian[0],datetime.datetime.now())
    if First!=True:
        if int(kXian[0][0][14:16]) != datetime.datetime.now().minute:
            time.sleep(10)
            continue
    First=False

    kNums = kXian[1:10]
    Low = float(min([i[-4] for i in kNums]))
    High = float(max([i[-5] for i in kNums]))
    ShouPan = float(kXian[1][-3])
    RSV = (ShouPan - Low) / (High - Low) * 100
    K = 2 / 3 * preK + 1 / 3 * RSV
    D = 2 / 3 * preD + 1 / 3 * K
    print( kXian[1][0][14:16] + "分的:","K——", round(K,4), "D——", round(D,4))
    if preK<preD and K>D :
        print("金叉了")
        winsound.Beep(1100, 15000)
    elif preK>preD and K<D:
        print("死叉了")
        winsound.Beep(700, 15000)
    # if preK<preD and K>D and preK<=50 and preD<=50:
    #     print("金叉了")
    #     winsound.Beep(1100, 15000)
    # elif preK>preD and K<D and preK>=50 and preD>=50:
    #     print("死叉了")
    #     winsound.Beep(1100, 15000)
    # elif preK>preD and K<D and preK<=50 and preD<=50:
    #     print("金叉该平了")
    #     winsound.Beep(600, 15000)
    # if preK<preD and K>D and preK>=50 and preD>=50:
    #     print("死叉该平了")
    #     winsound.Beep(600, 15000)
    preK = K
    preD = D

    sleepTime=210-int(time.time())%180
    # print("等",sleepTime,"秒")
    time.sleep(sleepTime)
