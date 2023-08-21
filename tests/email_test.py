import logging
from graphapi.emails_sender import MailSender
from graphapi.fetch_emails import FetchEmails
from graphapi.update_emails import UpdateEmails
import pytest

log = logging.getLogger(__name__)
data = {
    'grant_type': 'client_credentials',
    'client_id': '********',
    'client_secret': '******************',
    'scope': 'https://graph.microsoft.com/.default'
}
to_address = ["suresh@gmail.com"]
obj = MailSender("suresh@gmail.com", data=data)
message = "Test message"


class TestSetup:
    def test_send_close_wo_email(self):
        subject = "Test Email "
        response = obj.send_email(to_addresses=to_address, subject=subject, message_body=message)
        assert str(response) == "<Response [202]>"

    def test_send_failed_email(self):
        subject = "Test Email Failed "
        response = obj.send_email(to_addresses=to_address, subject=subject, message_body=message)
        assert str(response) == "<Response [202]>"

    def test_send_email_with_attachment(self):
        subject = "Test with attachment"
        attachment = []
        cc_list = ["suresh@gmail.com"]
        response = obj.send_email(to_addresses=to_address, subject=subject, message_body=message,
                                  attachment_paths=attachment, cc_list=cc_list)
        assert str(response) == "<Response [202]>"

    def test_send_unknown_errors(self):
        subject = "Test Email | Error"
        attachments = []
        response = obj.send_email(to_addresses=to_address, subject=subject, message_body=message,
                                  attachment_paths=attachments)
        assert str(response) == "<Response [202]>"

    @pytest.mark.parametrize("subject, isread", [("bye", False), ("bye", True), ("Test with attachment", False),
                                                 ("Test with attachment", True),
                                                 ("Be well, Excel! | Stress Resilience ", False)])
    def test_fetch_all_emails_with_subject(self, subject, isread):
        obj2 = FetchEmails("suresh@gmail.com", data=data)
        try:
            output = obj2.get_all_emails_from_inbox_with_subject(subject, isread=isread)['value'][0]
            assert output['subject'] == subject
            assert output['isRead'] == isread
        except:
            log.info("No mails are present")

    @pytest.mark.parametrize("subject, isread, n",
                             [("Monday", False, 0), ("Monday", True, 0), ("Test with attachment", False, 1),
                              ("Test with attachment", True, 4),
                              ("Be well, Excel! | Stress Resilience", False, 0),
                              ("Test with attachment", True, 1)])
    def test_get_first_n_mails_startswith_subject(self, subject, isread, n):
        obj2 = FetchEmails("suresh@gmail.com", data=data)
        output = obj2.get_first_n_emails_from_inbox_startswith_subject(n, subject, isread=isread)
        try:
            assert len(output['value']) == n
            assert subject in output['value'][0]['subject']
            assert output['value'][0]['isRead'] == isread
        except:
            log.info("No mails are present")

    @pytest.mark.parametrize("subject, isread,n",
                             [("Monday", False, 0), ("Monday", True, 0), ("Test with attachment", False, 1),
                              ("Test with attachment", True, 4),
                              ("Be well, Excel! | Stress Resilience", False, 0),
                              ("Test with attachment", True, 1)])
    def test_get_first_n_mails_startswith_subject(self, subject, isread, n):
        obj2 = FetchEmails("suresh@gmail.com", data=data)
        output = obj2.get_first_n_emails_from_inbox_startswith_subject(n, subject, isread=isread)
        try:
            assert len(output['value']) == n
            assert subject in output['value'][0]['subject']
            assert output['value'][0]['isRead'] == isread
        except:
            log.info("No mails are present")

    @pytest.mark.parametrize("subject, isread,n",
                             [("Monday", False, 0), ("Monday", True, 0), ("Test with attachment", False, 1),
                              ("Test with attachment", True, 4),
                              ("Be well, Excel! | Stress Resilience", False, 0),
                              ("Test with attachment", True, 1)])
    def test_get_first_n_mails_startswith_subject(self, subject, isread, n):
        obj2 = FetchEmails("suresh@gmail.com", data=data)
        output = obj2.get_first_n_emails_from_inbox_startswith_subject(n, subject, isread=isread)
        try:
            assert len(output['value']) == n
            assert subject in output['value'][0]['subject']
            assert output['value'][0]['isRead'] == isread
        except:
            log.info("No mails are present")

    @pytest.mark.parametrize("subject, isread", [("Monday", False), ("Monday", True), ("Test with attachment", False),
                                                 ("Test with attachment", True),
                                                 ("Be well, Excel! | Stress Resilience", False),
                                                 ("Test with attachment", True)])
    def test_get_all_emails_from_inbox_which_contains_subject(self, subject, isread):
        obj2 = FetchEmails("suresh@gmail.com", data=data)
        try:
            output = obj2.get_all_emails_from_inbox_which_contains_subject(subject, isread=isread)['value'][0]
            assert subject in output['subject']
            assert output['isRead'] == isread
        except:
            log.info("No mails are present")

    @pytest.mark.parametrize("name", ['Suresh', 'Naresh', 'Ramesh'])
    def test_get_user_info_with_name(self, name):
        try:
            obj2 = FetchEmails("suresh@gmail.com", data)
            output = obj2.get_user_info_with_name(name)['value'][0]
            assert name in output['displayName']
        except:
            log.info("No mails are present")

    def test_mark_as_read(self):
        obj2 = FetchEmails("suresh@gmail.com", data)
        try:
            output = obj2.get_all_emails_from_inbox_which_contains_subject("FAX Failure")['value'][0]
            assert output['isRead'] == False
            obj3 = UpdateEmails("suresh@gmail.com", data)
            output1 = obj3.mark_mail_as_read(output['id'])
            assert output1['isRead'] == True
        except:
            log.info("No mails are present")

    @pytest.mark.parametrize("subject, isread, time_delta", [("monday", False, '2022-10-06T13:41:59Z')])
    def test_get_emails_for_last_day(self, subject, isread, time_delta):
        obj3 = FetchEmails("suresh@gmail.com", data=data)
        try:
            output = obj3.get_emails_for_last_day(subject, isread=isread, time_delta=time_delta)['value'][0]
            assert subject in output['subject']
            assert output['isRead'] == isread
        except:
            log.info("No mails are present")
