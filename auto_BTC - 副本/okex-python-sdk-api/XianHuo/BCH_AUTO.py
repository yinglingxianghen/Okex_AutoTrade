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

name="BCHH"
orderNum=0
lock=False
fallNum=4 #瀑布值
interval=2 #间隔价
top=390
maxbuied=374
sleepTime=10
prePendList=[]
order2Prices={}
def take_order(side,price):
    global orderNum,prePendList,order2Prices
    if side=='buy':
        if price>=top:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t","不买|接近顶值:",top,"\t","预买价:",price)
            time.sleep(sleepTime)
            return
        else:
            takeOrder = levelAPI.take_order(instrument_id='BCH-USDT', side=side, margin_trading='2',
                                    client_oid=name + str(orderNum), price=str(price), size='0.011')
            if takeOrder['error_code'] == '33017':
                print("可买余额不足")
                time.sleep(sleepTime)
            else:
                order2Prices[name+str(orderNum)]=price
                print("买入记录:",order2Prices)
                prePendList.append(name + str(orderNum))
    else:
        takeOrder = levelAPI.take_order(instrument_id='BCH-USDT', side=side, margin_trading='2',
                                        client_oid=name + str(orderNum), price=str(price), size=canSell)
        if takeOrder['error_code']=='33024':
            print("可卖不足最小单位")

    orderNum += 1
    print("此单买卖明细:","\t",side,"\t",price,"\t",name+str(orderNum-1),"\t",takeOrder)

while True:
    try:
        result_xian = spotAPI.get_specific_ticker('BCH-USDT')
        now_price = float(result_xian["last"])
        # 起始先手动下单
        # take_order('buy', 14)
        # time.sleep(1000)
        print("---------------------------------------------------------------"+datetime.datetime.now().strftime('%H:%M:%S'),
              "BCH现价------"+str(now_price)+"---------------------------------------------------------------------")

        info = levelAPI.get_specific_account('BCH-USDT')
        canSell = info['currency:BCH']['available']
        canBuy=round(float(info['currency:USDT']['available'])/now_price,3)

        pendOrders = levelAPI.get_order_pending(instrument_id='BCH-USDT', after='', before='', limit='')
        pendOrders = [i for i in pendOrders[0] if i['side'] == 'buy']
        pendList=[i['client_oid'] for i in pendOrders]
        print("当前买入挂单数——", len(pendOrders),"——",pendList)

        succCidList=list(set(prePendList).difference(set(pendList)))
        print("上波成功买入单号:",succCidList)
        succPriceList=[]
        for i in succCidList:
            succPriceList.append(order2Prices[i])
        maxSuccBuied=max(succPriceList) if len(succCidList) else maxbuied
        maxbuied=maxSuccBuied
        print("\t\t\t\t\t\t\t\t\t","最后一次买入价:",maxSuccBuied,"\t","上一轮成功买入价表:",succPriceList,"\t","可买数:",canBuy,"\t","可卖数:",canSell)
        prePendList=pendList

        if lock==False and maxSuccBuied-now_price>fallNum:
            #下单卖(最小值+间隔)
            result=take_order('sell',maxSuccBuied+interval)
            print(datetime.datetime.now(),"已处理尾单！暴跌了！！！！！！！锁上！！！！！！！！",result)
            #下3单买(当前价-暴跌值)
            take_order('buy',now_price)
            take_order('buy',now_price-fallNum)
            take_order('buy',now_price-fallNum*2)
            lock = True
            time.sleep(sleepTime)
            continue
        elif lock==False and now_price-maxSuccBuied>fallNum:
            #撤掉全部单
            result = levelAPI.revoke_orders([{'instrument_id': 'BCH-USDT', 'client_oids': pendList}])
            print(datetime.datetime.now(),"已撤销全部订单！暴涨了！！！！！！！锁上！！！！！！！！",result)
            #下3单买(当前价+暴涨值)
            take_order('buy',now_price)
            take_order('buy',now_price+fallNum)
            take_order('buy',now_price+fallNum*2)
            prePendList=list(set(prePendList).difference(set(pendList)))
            lock=True
            time.sleep(sleepTime)
            continue
        if len(pendOrders)==0:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t上一波已买成三单")
            #下单卖(按最大值第三个价格)
            take_order('sell', maxSuccBuied+interval)
            #买入三单
            take_order('buy',now_price- interval)
            take_order('buy',now_price- interval*2)
            take_order('buy',now_price - interval*3)
            lock = False
        elif len(pendOrders)==1:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t上一波已买成两单")
            #下单卖（找到已成交第一个的价格）
            take_order('sell', maxSuccBuied+interval)
            #下单买(当前价-interval)
            take_order('buy',now_price- interval)
            take_order('buy', now_price- interval*2)
            lock = False
        elif len(pendOrders)==2:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t上一波已买成一单")
            #下单卖（找到已成交第一个也就是最新成交的价格）
            take_order('sell',maxSuccBuied + interval)
            nowPendDict={}
            for i in prePendList:
                nowPendDict[i]=order2Prices[i]
            sortedPendDict=sorted(nowPendDict.items(),key=lambda x:x[1])
            # if 当前价-最大订单>间隔:
            if now_price-sortedPendDict[-1][1]>interval:
                #下单买(当前价)
                take_order('buy', now_price-interval)
            else:
                #下单买(最小订单-interval)
                take_order('buy', sortedPendDict[0][1] - interval)
            lock=False

        else:
            #if 当前价-最大订单>间隔:

            nowPendDict = {}
            for i in prePendList:
                nowPendDict[i] = order2Prices[i]
            sortedPendDict = sorted(nowPendDict.items(), key=lambda x: x[1])
            maxPrice = sortedPendDict[-1][1]
            minPrice = sortedPendDict[0][1]
            print("\t\t\t\t\t\t\t\t\t\t","上一波没买成单","\t\t","挂单最高价:",maxPrice,"\t","挂单最低价:",minPrice,"\t","现价:",now_price,"\t","瀑布值:",fallNum)

            if now_price-minPrice  > interval * 3 or maxPrice - minPrice > fallNum * 2 or now_price - maxPrice > interval:#包含暴涨
                #撤掉最小订单
                Oid=sortedPendDict[0][0]
                revokeOrder = levelAPI.revoke_order(instrument_id='BCH-USDT', client_oid=Oid)
                print("撤单|价格:",sortedPendDict[0][1],revokeOrder)
                prePendList=prePendList.remove(Oid)
                #下单买(当前价)
                take_order('buy', now_price-interval)
                lock = False
            #else:
            #	pass

    except Exception as e:
        print("出错了!",e)#traceback.format_exc()
    time.sleep(sleepTime)
