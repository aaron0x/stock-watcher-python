import unittest
from mock import mock

from model.notification import Notifier
from model.configuration import SMTPSetting

from email.mime.text import MIMEText


class NotifierTestCase(unittest.TestCase):
    def test_notify(self):
        expected_to_adds = ['aaron1126@gmail.com', 'silver@yahoo.com']
        message = 'goodday'
        expected_smtp_setting = SMTPSetting('smtp.gmail.com:587', 'aaron', 'haveaniceday', 'aaron@gmail.com', 'subject')
        expected_message = MIMEText(message)
        expected_message['From'] = expected_smtp_setting.from_addr
        expected_message['To'] = ','.join(expected_to_adds)
        expected_message['Subject'] = expected_smtp_setting.subject

        fake_smtp = mock.Mock()
        n = Notifier(fake_smtp)
        n.notify(expected_smtp_setting, expected_to_adds, message)

        fake_smtp.connect.assert_called_with(expected_smtp_setting.server)
        fake_smtp.login.assert_called_with(expected_smtp_setting.user, expected_smtp_setting.password)
        fake_smtp.sendmail.assert_called_with(expected_smtp_setting.from_addr, expected_to_adds, expected_message.as_string())
        fake_smtp.quit.assert_called_with()
