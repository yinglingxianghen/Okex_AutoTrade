### 如何使用？

`python版本：3.6+`

`WebSocketAPI：建议websockets库版本为6.0`

#### 第一步：下载SDK，安装相关所需库

1.1 下载`python SDK`
* 将SDK目录`Clone`或者`Download`到本地，选择使用`okex-python-sdk-api`即可

1.2 安装所需库
```python
pip install requests
pip install websockets==6.0
```

#### 第二步：配置个人信息

2.1 如果还未有API，可[点击](https://www.okex.com/account/users/myApi)前往官网进行申请

2.2 将各项信息在`example.py（RestAPI）`和`websocket_example.py（WebSocketAPI）`中填写
```python
api_key = ""
secret_key = ""
passphrase = ""
```
#### 第三步：调用接口

* RestAPI
    
    * 运行`example.py`
    
    * 解开相应方法的注释传参调用各接口即可
    
* WebSocketAPI
    
    * 运行`websocket_example.py`
        
    * 根据个人/公共频道选择对应启动方法，解开相应频道的注释即可
    
    ```python
    # 公共数据 不需要登录（行情，K线，交易数据，资金费率，限价范围，深度数据，标记价格等频道）
    loop.run_until_complete(subscribe_without_login(url, channels))
    
    # 个人数据 需要登录（用户账户，用户交易，用户持仓等频道）
    loop.run_until_complete(subscribe(url, api_key, passphrase, secret_key, channels))
    ```

附言：

* 如果对API尚不了解，建议参考`OKEx`官方[API文档](https://www.okex.com/docs/zh/)

* 若使用`WebSocketAPI`遇到问题建议参考相关链接

    * `asyncio`、`websockets`文档/`github`：
    
            https://docs.python.org/3/library/asyncio-dev.html
            https://websockets.readthedocs.io/en/stable/intro.html
            https://github.com/aaugustin/websockets
    
    * 关于`code=1006`：
    
            https://github.com/Rapptz/discord.py/issues/1996
            https://github.com/aaugustin/websockets/issues/587