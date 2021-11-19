#coding:utf8
apikey = "90ae9efc-a27c-46a9-8071-deeb0581c6f9"
secretkey = "7F32148EBBAC5300EF04C3697FDBC125"
passphrase = "369Zsx4218"

IP = "125.119.191.97"
#备注名 = "yingling"
#权限 = "只读/提币/交易"

import requests
# r=requests.get("https://www.okexcn.com/api/spot/v3/instruments/BTC-USDT/ticker")#BTC-USDT
proxies = {'http': 'http://localhost:10080', 'https': 'http://localhost:10080'}

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
r=requests.get("https://202020.ip138.com/",headers=headers,proxies=proxies,verify=False)
r.encoding="utf8"
print(r.text)

