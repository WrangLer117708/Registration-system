#!/usr/bin/python
#-*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
 
my_sender='13598591279@163.com'    # 发件人邮箱账号
my_pass = 'wrangler1217'              # 发件人邮箱密码(当时申请smtp给的口令)
my_user='13598591279@sina.cn'      # 收件人邮箱账号，我这边发送给自己

msg=MIMEText('Hello,你好明dddddddddddddddddddddddddddddddddddddd天去爬山吗')
msg['From']=formataddr(["大卫",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
msg['To']=formataddr(["你的老朋友",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
msg['Subject']="你好"                # 邮件的主题，也可以说是标题
 
server=smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
server.quit()# 关闭连接
