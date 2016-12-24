from email.mime.text import MIMEText


class Notifier(object):
    def __init__(self, smtp):
        self.smtp = smtp

    def notify(self, smtp_setting, to_addrs, message):
        msg = MIMEText(message)
        msg['From'] = smtp_setting.from_addr
        msg['To'] = ','.join(to_addrs)
        msg['Subject'] = smtp_setting.subject
        # self.smtp.set_debuglevel(True)
        self.smtp.connect(smtp_setting.server)
        self.smtp.login(smtp_setting.user, smtp_setting.password)
        self.smtp.sendmail(smtp_setting.from_addr, to_addrs, msg.as_string())
        self.smtp.quit()
