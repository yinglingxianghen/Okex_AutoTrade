#coding:utf8
import traceback
import winsound
import okex.lever_api as lever
import okex.spot_api as spot
import datetime,time
passphrase = "xxxx"
api_key = "xxxx"
secret_key = "xxxx"
IP = "xxxx"
spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
levelAPI = lever.LeverAPI(api_key, secret_key, passphrase, False)

name="BTC2"
orderNum=0
# interval=250 #间隔价
top=398000
maxbuied=34750
prePendList=[]
order2Prices={}
counts=0
canSell='1'
nowTwoPend_lastPrice=0
sleepTime = 10

def take_order(side,price,size='0.01'):
    global orderNum,prePendList,order2Prices

    time.sleep(5)
    if side=='buy':
        if price>=top:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t","不买|接近顶值:",top,"\t","预买价:",price)
            # winsound.Beep(1100, 1500)
            exit()
        else:
            takeOrder = levelAPI.take_order(instrument_id='BTC-USDT', side=side, margin_trading='2',
                                    client_oid=name + str(orderNum), price=str(price), size=size)
            if takeOrder['error_code'] == '33017':
                print("可买余额不足没买成")
                time.sleep(30)
                return take_order(side, price)
            else:
                order2Prices[name+str(orderNum)]=price
                print("\t\t\t","记录:",order2Prices)
                prePendList.append(name + str(orderNum))
    else:
        takeOrder = levelAPI.take_order(instrument_id='BTC-USDT', side=side, margin_trading='2',
                                        client_oid=name + str(orderNum), price=str(price), size=size)
        if takeOrder['error_code']=='33024':
            print("可卖不足最小单位")

    orderNum += 1
    print("此单买卖明细:","\t",side,"\t",price,"\t",name+str(orderNum-1),"\t",takeOrder)
    time.sleep(5)
while True:
    try:
        result_xian = spotAPI.get_specific_ticker('BTC-USDT')
        now_price = float(result_xian["last"])
        # 起始先手动下单
        # take_order('buy', 14)
        # time.sleep(1000)
        print("---------------------------------------------------------------"+datetime.datetime.now().strftime('%H:%M:%S'),
              "BTC现价------"+str(now_price)+"---------------------------------------------------------------------")

        time.sleep(5)
        pendOrders = levelAPI.get_order_pending(instrument_id='BTC-USDT', after='', before='', limit='')
        pendOrders = [i for i in pendOrders[0] if i['side'] == 'buy']
        pendList=[i['client_oid'] for i in pendOrders]
        print("当前买入挂单数——", len(pendOrders),"——",pendList)

        succCidList=list(set(prePendList).difference(set(pendList)))
        if len(succCidList):
            time.sleep(5)
            info = levelAPI.get_specific_account('BTC-USDT')
            canSell = info['currency:BTC']['available']
            canBuy = round(float(info['currency:USDT']['available']) / now_price, 3)
            print("\t","可买数:",canBuy,"\t","可卖数:",canSell)
        counts+=len(succCidList)
        # top -= 10*len(succCidList)
        print("\t\t\t","已成功买入单数:",counts,"\t\t\t","上波成功买入单号:",succCidList,"\t\t\t","此时上限值:",top)
        succPriceList=[]
        for i in succCidList:
            succPriceList.append(order2Prices[i])
        maxSuccBuied=max(succPriceList) if len(succCidList) else maxbuied
        maxbuied=maxSuccBuied
        print("\t\t\t\t\t\t\t\t\t","最后一次买入价:",maxSuccBuied,"\t","上一轮成功买入价表:",succPriceList,)
        prePendList=pendList

        nowPendDict = {}
        for i in prePendList:
            nowPendDict[i] = order2Prices[i]
        sortedPendDict = sorted(nowPendDict.items(), key=lambda x: x[1])
        if len(sortedPendDict):
            maxPrice = sortedPendDict[-1][1]
            minPrice = sortedPendDict[0][1]
            print("\t\t\t\t\t\t\t\t\t\t", "上一波买单:", "\t\t", "当前挂单最高价:", maxPrice, "\t", "挂单最低价:", minPrice, "\t", "现价:",
                  now_price, "\t")
        if len(pendOrders)==0:
            if len(succPriceList)==3:
                print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t上一波已买成一或二或三单")
                take_order('sell', succPriceList[0]+250,str(float(canSell)/3))
                take_order('sell', succPriceList[1]+250,str(float(canSell)/3))
                take_order('sell', succPriceList[2]+250,str(float(canSell)/3))
            elif len(succPriceList)==2:
                take_order('sell', succPriceList[0] + 250, str(float(canSell) / 2))
                take_order('sell', succPriceList[1] + 250, str(float(canSell) / 2))
            elif len(succPriceList)==1:
                take_order('sell', succPriceList[0] + 250, canSell)
            elif len(succPriceList)==0:
                pass
            take_order('buy', now_price // 250 * 250+250)
            take_order('buy', now_price // 250 * 250)
            take_order('buy', now_price // 250 * 250 - 250 )
            nowTwoPend_lastPrice = now_price // 250 * 250+250
        elif len(pendOrders)==1:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t上一波已买成一或两单")
            if len(succPriceList)==1:
                take_order('sell', succPriceList[0] + 250, canSell)
                take_order('buy', minPrice - 250)
            elif len(succPriceList)==2:
                take_order('sell', succPriceList[0]+250,str(float(canSell)/2))
                take_order('sell', succPriceList[1]+250,str(float(canSell)/2))
                take_order('buy',minPrice-250)
                take_order('buy',minPrice-250*2)
            nowTwoPend_lastPrice = minPrice
        elif len(pendOrders)==2:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t上一波已买成一单")
            if len(succPriceList):
                take_order('sell',succPriceList[0]+250,canSell)
            if now_price//250*250== nowTwoPend_lastPrice:
                time.sleep(sleepTime)
                continue
            elif now_price<nowTwoPend_lastPrice:
                take_order('buy', minPrice-250)
                nowTwoPend_lastPrice=maxPrice
            elif now_price-nowTwoPend_lastPrice>=250:
                take_order('buy', nowTwoPend_lastPrice)
        else:
            if now_price- maxPrice >=250*2:
                print("三单间隔较大全撤掉")
                revokeOrder1 = levelAPI.revoke_order(instrument_id='BTC-USDT', client_oid=prePendList[0])
                print("撤单掉三个中1:", revokeOrder1)
                revokeOrder2 = levelAPI.revoke_order(instrument_id='BTC-USDT', client_oid=prePendList[1])
                print("撤单掉三个中2:", revokeOrder2)
                revokeOrder3 = levelAPI.revoke_order(instrument_id='BTC-USDT', client_oid=prePendList[2])
                print("撤单掉三个中3:", revokeOrder3)
                # print("暴涨了!已撤单三单价格分别是:",minPrice,sortedPendDict[1][1],maxPrice,revokeOrder)
                prePendList=[]
                take_order('buy', now_price//250*250)
                take_order('buy', now_price//250*250-250)
                take_order('buy', now_price//250*250-250*2)
                nowTwoPend_lastPrice =now_price//250*250
    except Exception as e:
        print("出错了!",traceback.format_exc())#traceback.format_exc()
    time.sleep(sleepTime)
