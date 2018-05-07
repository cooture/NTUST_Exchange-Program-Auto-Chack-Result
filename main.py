# -*- coding: UTF-8 -*-
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from bs4 import BeautifulSoup

while 1:
    loginurl = 'http://stu88.ntust.edu.tw/inboundchina/stu/login.do'
    homeurl = "http://stu88.ntust.edu.tw/inboundchina/stu/review.result"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Host": 'stu88.ntust.edu.tw',
        "Accept-Language": 'zh-cn',
        "Content-Type": 'application/x-www-form-urlencoded',
        'Referer': 'http://stu88.ntust.edu.tw/inboundchina/stu',
        "Upgrade-Insecure-Requests": "1",
        "Origin": 'http://jwk.lzu.edu.cn',
        "DNT": '1',
        "Connection": 'keep-alive'

    }

    session = requests.Session()

    payload = {
        'email': 'ranxuebin@ranxb.cn',
        'password': '*****',
        'captcha': ''
    }


    def send_mail(sub, text):
        # 第三方 SMTP 服务
        mail_host = "smtp.lzu.edu.cn"  # 设置服务器
        mail_user = "******"  # 用户名
        mail_pass = "*****"  # 口令

        sender = 'ranxb16@lzu.cn'
        # receivers = ['ranxuebin@ranxb.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        receivers = ','.join(['ranxuebin@ranxb.cn'])
        message = MIMEText(text, 'plain', 'utf-8')
        message['From'] = Header("自动发送", 'utf-8')
        message['To'] = Header("Rankin", 'utf-8')

        subject = sub
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("send mail error!")


    try:
        response_login = session.post(loginurl, headers=headers, data=payload)
        response_home = session.get(homeurl, headers=headers)

    except:
        print("login error!")

    result = BeautifulSoup(response_home.text, "html.parser")
    result = result.find(class_="alert alert-info")
    print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) + "    " + result.span.string)

    if result.span.string != 'Pass the first stage':
        send_mail("台科大信息", result.span.string)

    time.sleep(600)
