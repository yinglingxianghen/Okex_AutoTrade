import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.index_api as index
import okex.option_api as option
import okex.system_api as system
import okex.information_api as information
import json
import datetime
import winsound
def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"

time = get_timestamp()

if __name__ == '__main__':
    '''apikey = "90ae9efc-a27c-46a9-8071-deeb0581c6f9"
secretkey = "7F32148EBBAC5300EF04C3697FDBC125"
IP = "125.119.191.97,103.66.216.93,118.115.42.208"
备注名 = "yingling"
权限 = "只读/提币/交易"'''
    passphrase = "369Zsx4218"
    api_key = "90ae9efc-a27c-46a9-8071-deeb0581c6f9"
    secret_key = "7F32148EBBAC5300EF04C3697FDBC125"
    IP = "125.119.191.97,103.66.216.93,118.115.42.208"
    #备注名 = "yingling"
    #权限 = "只读/提币/交易"
    # param use_server_time's value is False if is True will use server timestamp
    # param test's value is False if is True will use simulative trading

# account api test
# 资金账户API
#     accountAPI = account.AccountAPI(api_key, secret_key, passphrase, False)
    # 资金账户信息
    # result = accountAPI.get_wallet()

    # 单一币种账户信息
    # result = accountAPI.get_currency('BTC')
    # print("result:",result)
    # 资金划转
    # result = accountAPI.coin_transfer(currency='', amount='', account_from='', account_to='', type='', sub_account='', instrument_id='', to_instrument_id='')
    # 提币
    # result = accountAPI.coin_withdraw(currency='', amount='', destination='', to_address='', trade_pwd='', fee='')
    # 账单流水查询
    # result = accountAPI.get_ledger_record(currency='', after='', before='', limit='', type='')
    # 获取充值地址
    # result = accountAPI.get_top_up_address('')
    # 获取账户资产估值
    # result = accountAPI.get_asset_valuation(account_type='1', valuation_currency='btc')

    # 获取子账户余额信息
    # result = accountAPI.get_sub_account('')
    # 查询所有币种的提币记录
    # result = accountAPI.get_coins_withdraw_record()
    # 查询单个币种提币记录
    # result = accountAPI.get_coin_withdraw_record('')
    # 获取所有币种充值记录
    # result = accountAPI.get_top_up_records()
    # 获取单个币种充值记录
    # result = accountAPI.get_top_up_record(currency='', after='', before='', limit='')
    # 获取币种列表
    # result = accountAPI.get_currencies()
    # 提币手续费
    # result = accountAPI.get_coin_fee('')

# spot api test
# 币币API
    spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
    # 币币账户信息
    # result = spotAPI.get_account_info()
    # 单一币种账户信息
    # result = spotAPI.get_coin_account_info('')
    # 账单流水查询
    # result = spotAPI.get_ledger_record(currency='', after='', before='', limit='', type='')
    # 下单
    # result = spotAPI.take_order(instrument_id='', side='', client_oid='', type='', size='', price='', order_type='0', notional='')
    # 批量下单
    # result = spotAPI.take_orders([
    #     {'instrument_id': '', 'side': '', 'type': '', 'price': '', 'size': ''},
    #     {'instrument_id': '', 'side': '', 'type': '', 'price': '', 'size': ''}
    # ])
    # 撤销指定订单
    # result = spotAPI.revoke_order(instrument_id='', order_id='', client_oid='')
    # 批量撤销订单
    # result = spotAPI.revoke_orders([
    #     {'instrument_id': '', 'order_ids': ['', '']},
    #     {'instrument_id': '', 'order_ids': ['', '']}
    # ])
    # 获取订单列表
    # result = spotAPI.get_orders_list(instrument_id='', state='', after='', before='', limit='')
    # 获取所有未成交订单
    # result = spotAPI.get_orders_pending(instrument_id='', after='', before='', limit='')
    # 获取订单信息
    # result = spotAPI.get_order_info(instrument_id='', order_id='', client_oid='')
    # 获取成交明细
    # result = spotAPI.get_fills(instrument_id='', order_id='', after='', before='', limit='')
    # 委托策略下单
    # result = spotAPI.take_order_algo(instrument_id='', mode='', order_type='', size='', side='', trigger_price='', algo_price='', algo_type='')
    # 委托策略撤单
    # result = spotAPI.cancel_algos(instrument_id='', algo_ids=['',''], order_type='')
    # 获取当前账户费率
    # result = spotAPI.get_trade_fee()
    # 获取委托单列表
    # result = spotAPI.get_order_algos(instrument_id='', order_type='', status='', algo_id='', before='', after='', limit='')
    # 公共-获取币对信息
    # result = spotAPI.get_coin_info()
    # 公共-获取深度数据
    # result = spotAPI.get_depth(instrument_id='', size='', depth='')
    # 公共-获取全部ticker信息
    # result = spotAPI.get_ticker()
    # 公共-获取某个ticker信息
    result = spotAPI.get_specific_ticker('BTC-USDT')
    print("BTC现价:", result["last"])

    # 公共-获取成交数据
    # result = spotAPI.get_deal(instrument_id='BTC-USDT', limit='')
    # print("公共-获取成交数据",result)
    # 公共-获取K线数据
    # result = spotAPI.get_kline(instrument_id='BTC-USDT', start='2020-12-10T07:05:00.000Z', end='2020-12-10T07:06:00.000Z', granularity='')
    # print("公共-获取K线数据", result)
    # 公共-获取历史K线数据
    # result = spotAPI.get_history_kline(instrument_id='BTC-USDT', start='', end='', granularity='900')
    # print("公共-获取历史K线数据", result)
# level api test
# 币币杠杆API
    levelAPI = lever.LeverAPI(api_key, secret_key, passphrase, False)
    # 币币杠杆账户信息
    # result = levelAPI.get_account_info()

    # 单一币对账户信息
    result = levelAPI.get_specific_account('BTC-USDT')
    print("杠杆BTC:",result)
    # 账单流水查询
    # result = levelAPI.get_ledger_record(instrument_id='', after='', before='', limit='', type='')
    # 杠杆配置信息
    # result = levelAPI.get_config_info()
    # 某个杠杆配置信息
    # result = levelAPI.get_specific_config_info('')
    # 获取借币记录
    # result = levelAPI.get_borrow_coin(status='', after='', before='', limit='')
    # 某币对借币记录
    # result = levelAPI.get_specific_borrow_coin(instrument_id='', status='', after='', before='', limit='')
    # 借币
    # result = levelAPI.borrow_coin(instrument_id='', currency='', amount='', client_oid='')
    # 还币
    # result = levelAPI.repayment_coin(instrument_id='', currency='', amount='', borrow_id='', client_oid='')

    # 下单
    # result = levelAPI.take_order(instrument_id='BTC-USDT', side='sell', margin_trading='2', client_oid='A0000', type='', order_type='0', price='19000', size='0.1', notional='')
    # result = levelAPI.take_order(instrument_id='BTC-USDT', side='sell', margin_trading='2', client_oid='A0001', price='19000', size='0.1')
    # print("下单结果",result)
    # 批量下单
    # result = levelAPI.take_orders([
    #     {'instrument_id': '', 'side': '', 'price': '', 'size': '', 'margin_trading': '2'},
    #     {'instrument_id': '', 'side': '', 'price': '', 'size': '', 'margin_trading': '2'}
    # ])
    # 撤销指定订单
    # result = levelAPI.revoke_order(instrument_id='BTC-USDT', order_id='', client_oid='A0001')
    # print("撤单结果",result)

    # 批量撤销订单
    # result = levelAPI.revoke_orders([
    #     {'instrument_id': '', 'order_ids': ['', '']},
    #     {'instrument_id': '', 'client_oids': ['', '']}
    # ])
    # 获取订单列表
    # result = levelAPI.get_order_list(instrument_id='', state='', after='', before='', limit='')
    # 获取订单信息
    # result = levelAPI.get_order_info(instrument_id='', order_id='', client_oid='')
    # 获取所有未成交订单
    # result = levelAPI.get_order_pending(instrument_id='', after='', before='', limit='')
    # 获取成交明细
    # result = levelAPI.get_fills(instrument_id='', order_id='', after='', before='', limit='')
    # 获取杠杆倍数
    #result = levelAPI.get_leverage('BTC-USDT')
    # 设置杠杆倍数
    # result = levelAPI.set_leverage(instrument_id='', leverage='')
    # 公共-获取标记价格
    # result = levelAPI.get_mark_price('')
