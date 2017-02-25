#!/usr/bin/env python
#coding=utf-8
import itchat
import os
import sys
import time
import spider_main

import socket
import struct

def to_hex_int(s):
    return int(s.upper(), 16)

mac = "9C5C8E895C67"
dest = ('192.168.1.103', 7)

reload(sys)
sys.setdefaultencoding('utf8')

if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess

#msg['Text'] is receive info
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):

    msgHeader = msg['Text'][0:2]

    #笑话
    if msgHeader == 'Xh':
        itchat.send('spider begin', toUserName='filehelper')

        root_url = "http://www.qiushibaike.com/8hr/page/" + msg["Text"][2:]
        obj_spider = spider_main.SpiderMain()
        all_data = obj_spider.craw(root_url)

        for key, value in all_data.iteritems():
            #print all_data[key]
            itchat.send('name:' + key + 'content:' + all_data[key], toUserName='filehelper')

    #系统命令
    if msgHeader == 'Xt':
        itchat.send('system begin', toUserName='filehelper')

        order = msg['Text'][3:]

        orderArr = order.split()

        child = subprocess.Popen(orderArr, stdout=subprocess.PIPE);
        output = child.stdout.read()

        #print output,type(output)
        itchat.send(output, toUserName='filehelper')

    #开机
    if msgHeader == 'Kj':
      data = ''.join(['FFFFFFFFFFFF', mac * 20])
      send_data = b''

      for i in range(0, len(data), 2):
        send_data = b''.join([send_data,struct.pack('B', int(data[i: i + 2], 16))])

      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
      s.sendto(send_data,dest)
        
      #print("WOL packet %s bytes sent !" % send_data)
      itchat.send("WOL packet bytes sent !", toUserName='filehelper')
    
    return msg['Text']

itchat.auto_login(enableCmdQR = 2, hotReload = True)
itchat.send('send Kj, 打开台式机', toUserName='filehelper')
itchat.send('send Xt + 空格 + [command], 操作系统', toUserName='filehelper')
itchat.send('send Xh + [page], 糗事百科笑话', toUserName='filehelper')
itchat.send('welcome', toUserName='filehelper')
itchat.run()
