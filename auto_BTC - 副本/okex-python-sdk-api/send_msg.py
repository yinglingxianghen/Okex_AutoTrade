#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import traceback
from threading import Timer
from itchat.content import *
import requests
import itchat

#发送消息
def sendNews():
	while True:
		try:
			my_friend = itchat.search_friends(name = r'重生')
			my_love = my_friend[0].UserName
			itchat.send('11111111111111111', toUserName=my_love)
			itchat.send('22222222222222222', toUserName='filehelper')
			time.sleep(3)
		except:
			print("except:",traceback.format_exc())
		#itchat.logout()


if __name__ == '__main__':
	itchat.auto_login()
	sendNews()
	# itchat.send("msg", toUserName="filehelper")