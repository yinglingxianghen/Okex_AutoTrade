# coding:utf8
import traceback
import winsound
import okex.lever_api as lever
import okex.spot_api as spot
import datetime, time

passphrase = "xxxx"
api_key = "xxxx"
secret_key = "xxxx"
IP = "xxxx"

spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
levelAPI = lever.LeverAPI(api_key, secret_key, passphrase, False)
'''
当日RSV=（Cn收盘价－Ln最低）÷（Hn最高－Ln）×100
当日K值=2/3×前一日K值+1/3×当日RSV
当日D值=2/3×前一日D值+1/3×当日K值
若无前一日K 值与D值，则可分别用50来代替。
J值=3*当日K值-2*当日D值
                            开盘价格  	最高价格 	最低价格 	收盘价格 	交易量
'''
Ls = [['2021-01-07T08:55:00.000Z', '37217', '37260.6', '37170', '37204.6', '42.7624588'],
      ['2021-01-07T08:50:00.000Z', '37272', '37324.3', '37213.1', '37217', '57.63380553'],
      ['2021-01-07T08:45:00.000Z', '37216', '37346.9', '37121', '37275.6', '79.65638403'],
      ['2021-01-07T08:40:00.000Z', '37036.9', '37232.2', '37011.2', '37215.9', '94.81103458'],
      ['2021-01-07T08:35:00.000Z', '36929.8', '37035', '36929.8', '37035', '35.71941604'],
      ['2021-01-07T08:30:00.000Z', '36876.6', '36964.1', '36811', '36929.8', '72.07464176'],
      ['2021-01-07T08:25:00.000Z', '36514.3', '36899.6', '36514.3', '36870.3', '83.70254863'],
      ['2021-01-07T08:20:00.000Z', '36512.7', '36639.8', '36300', '36519.1', '144.91225086'],
      ['2021-01-07T08:15:00.000Z', '36842.6', '36850.4', '36505', '36512.6', '135.94234877']]

Low = float(min([i[-2] for i in Ls]))
High = float(max([i[-2] for i in Ls]))
Now = 37250
RSV = (Now - Low) / (High - Low) * 100
K = 2 / 3 * 86.17 + 1 / 3 * RSV
D = 2 / 3 * 75.475 + 1 / 3 * K
J = 3 * K - 2 * D
print(J)

while True:

    result_xian = spotAPI.get_specific_ticker('BTC-USDT')
    now_price = float(result_xian["last"])
    print(datetime.datetime.now(),now_price)
    time.sleep(1)