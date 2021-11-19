#coding:utf8
import traceback
import winsound
import okex.lever_api as lever
import okex.spot_api as spot
import datetime,time
import okex.option_api as option

passphrase = "xxxx"
api_key = "xxxx"
secret_key = "xxxx"
IP = "xxxx"
spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
levelAPI = lever.LeverAPI(api_key, secret_key, passphrase, False)
optionAPI = option.OptionAPI(api_key, secret_key, passphrase, False)



# 单个标的指数持仓信息
def getCost(instrument_id):
    time.sleep(15)
    try:
        holding = optionAPI.get_specific_position(underlying='ETH-USD', instrument_id=instrument_id)
        print(holding)
        avg_cost=float(holding['holding'][0]['avg_cost'])
        print("持仓均价:",avg_cost)
        size = holding['holding'][0]['avail_position']
        print("可出售数",size)
        return avg_cost,size
    except:
        print("getbuyTop出错！",traceback.format_exc())
        time.sleep(15)
        return getCost(instrument_id)
    
def getbuyTop(instrument_id):
    time.sleep(15)
    try:
        result = optionAPI.get_option_instruments_summary(underlying='ETH-USD', instrument_id=instrument_id)
        buyTop = float(result['best_bid'])
        print("最大买价:", buyTop)
        return buyTop
    except:
        print("getbuyTop出错！",traceback.format_exc())
        time.sleep(15)
        return getbuyTop(instrument_id)
    
def getNowPrice():
    time.sleep(1)
    try:
        result_xian = spotAPI.get_specific_ticker('ETH-USDT')
        now_price = float(result_xian["last"])
        if now_price<650 or now_price>760:
            time.sleep(60)
            return getNowPrice()
        return now_price
    except:
        print("getNowPrice！", traceback.format_exc())
        time.sleep(10)
        return getNowPrice()
    
def takeOrder(instrument_id,side):
    time.sleep(0.5)
    try:
        orderResult = optionAPI.take_order(instrument_id=instrument_id, side=side,price='',size='1', match_price='1')
        if orderResult['error_code']=='0':
            print("下单成功",instrument_id,side)
    except:
        print("takeOrder出错！",traceback.format_exc())
        time.sleep(3)
        return takeOrder(instrument_id,side)

InstrumentId_P='ETH-USD-210108-720-P'
InstrumentId_C='ETH-USD-210108-760-C'
avg_cost_P=0.051
avg_cost_C=0.0537

while True:
    buyTop_P=getbuyTop(InstrumentId_P)
    print("现在买跌的盈利率:", buyTop_P / avg_cost_P)
    # print("现在买跌的最后位:",InstrumentId_P[-1:])

    if buyTop_P / avg_cost_P > 1.08:
        #下单卖
        takeOrder(InstrumentId_P,'sell')
        #再下单买
        now_price=getNowPrice()
        InstrumentId_P = 'BTC-USD-210108-' + str(now_price // 20 * 20) + '-P'
        print("------------------------------------------"+"此时已改标的P："+InstrumentId_P+"--------------------------------------------")
        takeOrder(InstrumentId_P,'buy')
        avg_cost_P, size=getCost(InstrumentId_P)

    print("----------------------------")

    buyTop_C = getbuyTop(InstrumentId_C)
    print("现在买涨的盈利率:", buyTop_C / avg_cost_C)
    # print("现在买涨的最后位:",InstrumentId_C[-1:])
    if buyTop_C / avg_cost_C >= 1.08:
        # 下单卖
        takeOrder(InstrumentId_C, 'sell')
        # 再下单买
        now_price = getNowPrice()
        InstrumentId_C = 'BTC-USD-210108-' + str((now_price // 20 + 1) * 20) + '-C'
        print("------------------------------------------"+"此时已改标的："+InstrumentId_C+"--------------------------------------------")
        takeOrder(InstrumentId_C, 'buy')
        avg_cost_C, size = getCost(InstrumentId_C)

    time.sleep(15)
    print("|||||||||||||||||||||||||||||||||||||||||||")
    # takeOrder = optionAPI.take_order(instrument_id='ETH-USD-210108-34500-C', side='sell', price='', size='1', client_oid='', order_type='', match_price='1')
    # print(takeOrder)
    # if takeOrder["error_code"]=="0":
    #     holdList.remove('ETH-USD-210108-34500-C')

# while True:
#     try:
#         result_xian = spotAPI.get_specific_ticker('BCH-USDT')
#         now_price = float(result_xian["last"])
#         print("---------------------------------------------------------------"+datetime.datetime.now().strftime('%H:%M:%S'),
#               "BCH现价------"+str(now_price)+"---------------------------------------------------------------------")
#     except:
#         time.sleep(sleepTime)


'''
每30s循环一次
先查实时价大于最大值或小于最小值
符合条件了在那个到期日里查所有卖一价-标记价最小的
下单买入
最大值+100 最小值-100

查一次挂单盈利
如果>=50%,就按对手价卖掉
'''

# result = optionAPI.get_instruments_summary(underlying='ETH-USD', delivery='201229')
# print(result)
#
# zhangMarketList={}
# for i in result:
#     if i['instrument_id'][-2:]=='-C':
#         zhangMarketList[i['instrument_id']]=float(i['best_ask'])-float(i['mark_price'])
# print(zhangMarketList)
# zhangSortedList = sorted(zhangMarketList.items(), key=lambda x: x[1])
# buyZhangKind=zhangSortedList[0][0]
# print(zhangSortedList)
# print(buyZhangKind)
# print("-------------------------")
# dieMarketList={}
# for i in result:
#     if i['instrument_id'][-2:]=='-P':
#         dieMarketList[i['instrument_id']]=float(i['best_ask'])-float(i['mark_price'])
# print(dieMarketList)
# buyDieSortedList = sorted(dieMarketList.items(), key=lambda x: x[1])
# buyDieKind=buyDieSortedList[0][0]
# print(buyDieSortedList)
# print(buyDieKind)
# 下单
# takeOrder = optionAPI.take_order(instrument_id='ETH-USD-210108-34500-C', side='buy', price='', size='1', client_oid='', order_type='', match_price='1')
# print(takeOrder)

# option api test
# 期权合约API
#     optionAPI = option.OptionAPI(api_key, secret_key, passphrase, False)
    # 单个标的指数持仓信息
    # result = optionAPI.get_specific_position(underlying='', instrument_id='')
    # 单个标的物账户信息
    # result = optionAPI.get_underlying_account('')
    # 下单
    # result = optionAPI.take_order(instrument_id='', side='', price='', size='', client_oid='', order_type='0', match_price='0')
    # 批量下单
    # result = optionAPI.take_orders('', [
    #     {'instrument_id': '', 'side': '', 'price': '', 'size': '', 'order_type': '0', 'match_price': '0'},
    #     {'instrument_id': '', 'side': '', 'price': '', 'size': '', 'order_type': '0', 'match_price': '0'}
    # ])
    # 撤单
    # result = optionAPI.revoke_order(underlying='', order_id='', client_oid='')
    # 批量撤单
    # result = optionAPI.revoke_orders(underlying='', order_ids=['', ''], client_oids=['', ''])
    # 修改订单
    # result = optionAPI.amend_order(underlying='', order_id='', client_oid='', request_id='', new_size='', new_price='')
    # 批量修改订单
    # result = optionAPI.amend_batch_orders('', [
    #     {'order_id': '', 'new_size': ''},
    #     {'client_oid': '', 'request_id': '', 'new_size': ''}
    # ])
    # 获取单个订单状态
    # result = optionAPI.get_order_info(underlying='', order_id='', client_oid='')
    # 获取订单列表
    # result = optionAPI.get_order_list(underlying='', state='', instrument_id='', after='', before='', limit='')
    # 公共-获取期权合约详细定价
    # result = optionAPI.get_instruments_summary(underlying='', delivery='')
    # 公共-获取单个期权合约详细定价
    # result = optionAPI.get_option_instruments_summary(underlying='', instrument_id='')