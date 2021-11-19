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

name="ETHH"
orderNum=0
lock=False
fallNum=6 #瀑布值
interval=3 #间隔价
top=662
maxbuied=650.56
sleepTime=30
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
            takeOrder = levelAPI.take_order(instrument_id='ETH-USDT', side=side, margin_trading='2',
                                    client_oid=name + str(orderNum), price=str(price), size='0.011')
            if takeOrder['error_code'] == '33017':
                print("可买余额不足")
                time.sleep(sleepTime)
            else:
                order2Prices[name+str(orderNum)]=price
                print("买入记录:",order2Prices)
                prePendList.append(name + str(orderNum))
    else:
        takeOrder = levelAPI.take_order(instrument_id='ETH-USDT', side=side, margin_trading='2',
                                        client_oid=name + str(orderNum), price=str(price), size=canSell)
        if takeOrder['error_code']=='33024':
            print("可卖不足最小单位")

    orderNum += 1
    print("此单买卖明细:","\t",side,"\t",price,"\t",name+str(orderNum-1),"\t",takeOrder)

while True:
    try:
        result_xian = spotAPI.get_specific_ticker('ETH-USDT')
        now_price = float(result_xian["last"])
        # 起始先手动下单
        # take_order('buy', 14)
        # time.sleep(1000)
        print("---------------------------------------------------------------"+datetime.datetime.now().strftime('%H:%M:%S'),
              "ETH现价------"+str(now_price)+"---------------------------------------------------------------------")

        info = levelAPI.get_specific_account('ETH-USDT')
        canSell = info['currency:ETH']['available']
        canBuy=round(float(info['currency:USDT']['available'])/now_price,3)

        pendOrders = levelAPI.get_order_pending(instrument_id='ETH-USDT', after='', before='', limit='')
        pendOrders = [i for i in pendOrders[0] if i['side'] == 'buy']
        sortedPendOrder = sorted(pendOrders, key=lambda x: x["price"])
        pendList=[i['client_oid'] for i in sortedPendOrder]
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
        elif lock==False and now_price-maxSuccBuied>fallNum:
            #撤掉全部单
            result = levelAPI.revoke_orders([{'instrument_id': 'ETH-USDT', 'client_oids': pendList}])
            prePendList=list(set(prePendList).difference(set(pendList)))
            print(datetime.datetime.now(),"已撤销全部订单！暴涨了！！！！！！！锁上！！！！！！！！",result)
            #下3单买(当前价+暴涨值)
            take_order('buy',now_price)
            take_order('buy',now_price+fallNum)
            take_order('buy',now_price+fallNum*2)
            lock=True
        if len(pendOrders)==0:
            #下单卖(按最大值第三个价格)
            take_order('sell', maxSuccBuied+interval)
            #买入三单
            take_order('buy',now_price)
            take_order('buy',now_price- interval)
            take_order('buy',now_price - interval*2)
            lock = False
        elif len(pendOrders)==1:
            #下单卖（找到已成交第一个的价格）
            take_order('sell', maxSuccBuied+interval)
            #下单买(当前价-interval)
            take_order('buy',now_price)
            take_order('buy', now_price- interval)
            lock = False
        elif len(pendOrders)==2:
            #下单卖（找到已成交第一个也就是最新成交的价格）
            take_order('sell',maxSuccBuied + interval)
            #if 当前价-最大订单>间隔:
            if now_price-float(sortedPendOrder[-1]['price'])>interval:
                #下单买(当前价)
                take_order('buy', now_price)
            else:
                #下单买(最小订单-interval)
                take_order('buy', float(sortedPendOrder[0]['price']) - interval)
            lock=False

        else:
            #if 当前价-最大订单>1:
            maxPrice=float(sortedPendOrder[-1]['price'])
            minPrice=float(sortedPendOrder[0]['price'])
            print("\t\t\t\t\t\t\t\t\t\t","挂单最高价:",maxPrice,"\t","挂单最低价:",minPrice,"\t","现价:",now_price,"\t","瀑布值:",fallNum)

            if now_price-minPrice  > interval * 3 or maxPrice - minPrice > fallNum * 2 or now_price - maxPrice > interval:
                #撤掉最小订单
                Oid=sortedPendOrder[0]['client_oid']
                revokeOrder = levelAPI.revoke_order(instrument_id='ETH-USDT', client_oid=Oid)
                prePendList.remove(Oid)
                print("撤单|价格:",sortedPendOrder[0]['price'],revokeOrder)
                #下单买(当前价)
                take_order('buy', now_price-interval)
                lock = False
            #else:
            #	pass

    except Exception as e:
        print("出错了!",e)#traceback.format_exc()
    time.sleep(sleepTime)
