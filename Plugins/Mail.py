import os
import smtplib
from configparser import ConfigParser
from email.mime.text import MIMEText

from Common import Get


def send_mail(sub, content, job):
    mail_conf_path = os.path.join(Get.base_dir(), 'Conf', 'Email.ini')
    cf = ConfigParser()
    cf.read(mail_conf_path, 'utf-8')
    mail_to = cf.items(job)
    mail_to_list = []
    for k, v in mail_to:
        mail_to_list.append(v)
    mail_host = cf.get('base', 'host')
    mail_user = cf.get('base', 'user')
    mail_pass = cf.get('base', 'pass')
    # mail_postfix = cf.get('base', 'postfix')
    me = "<" + mail_user + ">"
    msg = MIMEText(content, _subtype='html', _charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(mail_to_list)
    msg['CC'] = 'songjy@ehomepay.com.cn'
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, mail_to_list, msg.as_string())
        s.close()
        return True
    except Exception as e:
        print(str(e))
        return False
