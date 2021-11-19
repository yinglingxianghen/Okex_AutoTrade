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

name="ETHf"
orderNum=0
interval=6 #间隔价
top=398000
maxbuied=1266
sleepTime=15
prePendList=[]
order2Prices={}
rise=False
counts=0
unionPrice=[]
canSell='1'
def take_order(side,price):
    global orderNum,prePendList,order2Prices
    time.sleep(3)
    if side=='buy':
        if price>=top:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t","不买|接近顶值:",top,"\t","预买价:",price)
            # winsound.Beep(1100, 1500)
            exit()
        else:
            takeOrder = levelAPI.take_order(instrument_id='ETH-USDT', side=side, margin_trading='2',
                                    client_oid=name + str(orderNum), price=str(price), size='0.1')
            if takeOrder['error_code'] == '33017':
                print("可买余额不足没买成")
                time.sleep(30)
                return take_order(side, price)
            else:
                order2Prices[name+str(orderNum)]=price
                print("\t\t\t","记录:",order2Prices)
                prePendList.append(name + str(orderNum))
    else:
        takeOrder = levelAPI.take_order(instrument_id='ETH-USDT', side=side, margin_trading='2',
                                        client_oid=name + str(orderNum), price=str(price), size=canSell)
        if takeOrder['error_code']=='33024':
            print("可卖不足最小单位")

    orderNum += 1
    print("此单买卖明细:","\t",side,"\t",price,"\t",name+str(orderNum-1),"\t",takeOrder)
    time.sleep(3)
while True:
    sleepTime=3 if rise==True else 8
    try:
        result_xian = spotAPI.get_specific_ticker('ETH-USDT')
        now_price = float(result_xian["last"])
        # 起始先手动下单
        # take_order('buy', 14)
        # time.sleep(1000)
        print("---------------------------------------------------------------"+datetime.datetime.now().strftime('%H:%M:%S'),
              "ETH现价------"+str(now_price)+"---------------------------------------------------------------------")

        time.sleep(3)
        pendOrders = levelAPI.get_order_pending(instrument_id='ETH-USDT', after='', before='', limit='')
        pendOrders = [i for i in pendOrders[0] if i['side'] == 'buy']
        pendList=[i['client_oid'] for i in pendOrders]
        print("当前买入挂单数——", len(pendOrders),"——",pendList)

        succCidList=list(set(prePendList).difference(set(pendList)))
        if len(succCidList):
            time.sleep(3)
            info = levelAPI.get_specific_account('ETH-USDT')
            canSell = info['currency:ETH']['available']
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
        print("此时瀑布了吗？",rise)
        if len(pendOrders)==0:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t上一波已买成三单")
            #下单卖(按最大值第三个价格)
            take_order('sell', maxSuccBuied+interval)   if rise==False else take_order('sell', maxSuccBuied+interval*1.5)
            #买入三单
            take_order('buy',now_price- interval)
            take_order('buy',now_price- interval*2)
            take_order('buy',now_price - interval*3)
            rise=False
        elif len(pendOrders)==1:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t上一波已买成两单")
            #下单卖（找到已成交第一个的价格）
            take_order('sell', maxSuccBuied+interval)   if rise==False else take_order('sell', maxSuccBuied+interval*1.5)
            #下单买(当前价-interval)
            take_order('buy',now_price- interval)
            take_order('buy', now_price- interval*2)
            rise = False
        elif len(pendOrders)==2:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t上一波已买成一单")
            #下单卖（找到已成交第一个也就是最新成交的价格）
            take_order('sell',maxSuccBuied + interval)  if rise==False else take_order('sell', maxSuccBuied+interval*1.5)

            # if 当前价-当前最大订单>间隔:
            if now_price-maxPrice>interval:

                #下单买(当前价)
                take_order('buy', now_price-interval)

            else:
                #下单买(最小订单-interval)
                take_order('buy', minPrice - interval)
            rise = False
        else:

            #if 当前价-最大订单>间隔:
            if now_price-minPrice  >= interval * 3.5  or now_price - maxPrice >= interval*1.5:
                print("三单间隔较大全撤掉")
                #撤掉所有订单
                rise=True
                # revokeOrder = levelAPI.revoke_orders([{'instrument_id': 'BCH-USDT', 'client_oids': prePendList}])
                revokeOrder1 = levelAPI.revoke_order(instrument_id='ETH-USDT', client_oid=prePendList[0])
                print("撤单掉三个中1:", revokeOrder1)
                revokeOrder2 = levelAPI.revoke_order(instrument_id='ETH-USDT', client_oid=prePendList[1])
                print("撤单掉三个中2:", revokeOrder2)
                revokeOrder3 = levelAPI.revoke_order(instrument_id='ETH-USDT', client_oid=prePendList[2])
                print("撤单掉三个中3:", revokeOrder3)

                # print("暴涨了!已撤单三单价格分别是:",minPrice,sortedPendDict[1][1],maxPrice,revokeOrder)
                prePendList=[]
                take_order('buy', now_price)
                take_order('buy', now_price-interval)
                take_order('buy', now_price-interval*2)
                continue
            elif now_price-minPrice  >= interval * 3 or maxPrice - minPrice > interval * 2 or now_price - maxPrice >= interval:
                print("三单间隔较小想撤最小单")
                if maxPrice+interval in unionPrice:
                    print("最大值买过了，不买也不撤，再次循环，等瀑布或者等最大值买过")
                    time.sleep(sleepTime)
                    continue
                print("最大值没买过，买")

                #撤掉最小订单
                Oid=sortedPendDict[0][0]
                revokeOrder = levelAPI.revoke_order(instrument_id='ETH-USDT', client_oid=Oid)
                print("撤单掉三个中最小价格:",minPrice,revokeOrder)
                prePendList.remove(Oid)
                #下单买(当前价-间隔)
                take_order('buy', maxPrice+interval)
                unionPrice.append(maxPrice+interval)
                rise = False
            print("三单依然健在与世无争")

    except Exception as e:
        print("出错了!",traceback.format_exc())#traceback.format_exc()
    time.sleep(sleepTime)

