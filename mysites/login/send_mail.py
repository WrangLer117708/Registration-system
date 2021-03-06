#!/usr/bin/python3
import os
from django.core.mail import EmailMultiAlternatives, send_mail


os.environ['DJANGO_SETTINGS_MODULE'] = 'mysites.settings'

if __name__ == '__main__':

    subject, from_email, to = '来自www.liujiangblog.com的测试邮件', '13598581279@sina.com', '835314672@qq.com'
    text_content = '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！'
    html_content = '<p>欢迎访问<a href="http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a>，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
