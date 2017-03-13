# -*- encoding:utf-8 -*-
# --------------------------------
# author : dbird
# create_time : 2017/3/12 13:24
# --------------------------------
from random import Random

from django.core.mail import send_mail

from Mxonline2.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    email_title = ""
    email_body = ""
    if send_type == 'register':
        code = random_str(16)
        email_record.code = code
        email_record.email = email
        email_record.send_type = send_type
        email_record.save()
        email_title = "慕学在线网注册激活"
        email_body = "请点击下面的链接激活你的账号： http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type  == 'forget':
        code = random_str(4)
        email_record.code = code
        email_record.email = email
        email_record.send_type = send_type
        email_record.save()
        email_title = "慕学在线网找回密码"
        email_body = "您的邮箱激活码为{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


def random_str(random_len=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    random = Random()
    for i in range(random_len):
        str += chars[random.randint(0, len(chars) - 1)]
    return str


if __name__ == "__main__":
    print random_str(10)
