import unittest
from mock import Mock

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

        mock_smpt_instance = Mock()
        mock_smtp_class = Mock(return_value=mock_smpt_instance)
        n = Notifier(mock_smtp_class)
        n.notify(expected_smtp_setting, expected_to_adds, message)

        mock_smtp_class.assert_called_once_with()
        mock_smpt_instance.connect.assert_called_with(expected_smtp_setting.server)
        mock_smpt_instance.login.assert_called_with(expected_smtp_setting.user, expected_smtp_setting.password)
        mock_smpt_instance.sendmail.assert_called_with(expected_smtp_setting.from_addr, expected_to_adds, expected_message.as_string())
        mock_smpt_instance.quit.assert_called_with()
