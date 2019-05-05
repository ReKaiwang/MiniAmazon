import smtplib
from email.mime.text import MIMEText

class miniamazon(object):
    def __init__(self):
        self._mail_host = 'smtp.gmail.com'
        self._mail_user = '2019dukeece568uber@gmail.com'
        self._mail_pwd = 'pwforece568'

    def mailsend(self,userid):
        username = userid.username
        receivers = []
        receivers.append(userid.email)
        content = 'Hi ' + username + ' your package has been delivered. Go to your order history make some comments and earn rewards!'
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = username + ': Your Recent Order Update'
        message['From'] = self._mail_user
        message['To'] = receivers[0]

        try:
            s = smtplib.SMTP()
            s.connect(self._mail_host,587)
            s.login(self._mail_user,self._mail_pwd)
            s.sendmail(self._mail_user,receivers,message.as_string())
            s.quit()
            print('success')
        except smtplib.SMTPException as e:
            print('error',e)