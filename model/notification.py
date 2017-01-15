from email.mime.text import MIMEText

from retrying import retry


class Notifier(object):
    def __init__(self, smtp_class):
        self.smtp_class = smtp_class

    @retry(stop_max_attempt_number=3, wait_fixed=3000)
    def notify(self, smtp_confing, to_addrs, message):
        msg = MIMEText(message)
        msg['From'] = smtp_confing.from_addr
        msg['To'] = ','.join(to_addrs)
        msg['Subject'] = smtp_confing.subject
        # self.smtp.set_debuglevel(True)
        smtp_obj = self.smtp_class()
        smtp_obj.connect(smtp_confing.server)
        smtp_obj.login(smtp_confing.user, smtp_confing.password)
        smtp_obj.sendmail(smtp_confing.from_addr, to_addrs, msg.as_string())
        smtp_obj.quit()


__all__ = ['Notifier']
