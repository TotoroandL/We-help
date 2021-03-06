from random import Random

from Login.models import EmailVerifyRecord
from django.core.mail import send_mail         # 导入Django自带的邮件模块
from WeHelp20.settings import EMAIL_FROM       # 导入setting中发送邮件的配置


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送注册邮件
def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()  # 实例化一个EmailVerifyRecord对象
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 定义邮件内容:
    email_title = ""
    email_body = ""

    if send_type == "forget":
        email_title = "WeHelp找回密码链接"
        email_body = "请点击下面的链接找回你的密码: http://118.24.114.197/reset/{0}".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass