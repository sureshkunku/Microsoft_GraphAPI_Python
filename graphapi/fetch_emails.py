import logging
from graphapi.token import Token
from graphapi.constants import Access_Keys, GraphAPIEndpoints, Message_Keys
import requests
import os

log = logging.getLogger(__name__)


class FetchEmails():
    def __init__(self, mail_id, data):
        self.GRAPH_ENDPOINT = GraphAPIEndpoints.fetch_mails_endpoint.value.format(mail_id)
        self.graph_users_endpoint = GraphAPIEndpoints.user_end_point.value
        self.token = Token(data)
        self.response = self.token.post()
        self.mail_id = mail_id
        self.authorization_token = f"{self.response[Access_Keys.TokenType.value]} {self.response[Access_Keys.AccessToken.value]}"
        self.email_header = {
            Access_Keys.Authorization.value: self.authorization_token,
            Access_Keys.ContentType.value: "application/json",
        }

    def get_all_emails_from_inbox_with_subject(self, subject: str = None, isread: bool = False):
        """
        This method is used to get all emails from inbox based on subject and read status
        :param subject:  Subject of the email
        :param isread: is read or not
        :return: It willl return the list of emails in dict
        """
        response = requests.get(
            url=self.GRAPH_ENDPOINT + f"$filter=subject eq '{subject}' and isRead eq {str(isread).lower()} ",
            headers=self.email_header)
        return response.json()

    def get_first_n_emails_from_inbox_with_subject(self, n: int = 10, subject: str = None, isread: bool = False):
        """
                This method is used to get all emails from inbox based on subject and read status
                :param subject:  Subject of the email
                :param isread: is read or not
                :return: It will return first n mails in dict
                """
        response = requests.get(
            url=self.GRAPH_ENDPOINT + f"$filter=subject eq '{subject}' and isRead eq {str(isread).lower()}&$top={n} ",
            headers=self.email_header)
        return response.json()

    def get_all_emails_from_inbox_startswith_subject(self, subject: str = None, isread: bool = False):
        """
        This method is used to get all emails from inbox based on subject and read status
        :param subject:  Subject of the email
        :param isread: is read or not
        :return: It willl return the list of emails in dict
        """
        response = requests.get(
            url=self.GRAPH_ENDPOINT + f"$filter=startsWith(subject, '{subject}') and isRead eq {str(isread).lower()} ",
            headers=self.email_header)
        return response.json()

    def get_first_n_emails_from_inbox_startswith_subject(self, n: int = 10, subject: str = None, isread: bool = False):
        """
                This method is used to get all emails from inbox based on subject and read status
                :param subject:  Subject of the email
                :param isread: is read or not
                :return: It will return first n mails in dict
                """
        response = requests.get(
            url=self.GRAPH_ENDPOINT + f"$filter=startsWith(subject, '{subject}') and isRead eq {str(isread).lower()}&$top={n} ",
            headers=self.email_header)
        return response.json()

    def get_all_emails_from_inbox_which_contains_subject(self, subject: str = None, isread: bool = False):
        """
                This method is used to get all emails from inbox based on subject and read status
                :param subject:  Subject of the email
                :param isread: is read or not
                :return: It will return all mails which contains subject in dict
                """
        response = requests.get(
            url=self.GRAPH_ENDPOINT + f"$filter=contains(subject, '{subject}') and isRead eq {str(isread).lower()}",
            headers=self.email_header)
        return response.json()

    def get_all_emails_from_inbox_which_contains_subject(self, subject: str = None, isread: bool = False):
        """
                This method is used to get all emails from inbox based on subject and read status
                :param subject:  Subject of the email
                :param isread: is read or not
                :return: It will return all mails which contains subject in dict
                """
        response = requests.get(
            url=self.GRAPH_ENDPOINT + f"$filter=contains(subject, '{subject}') and isRead eq {str(isread).lower()}",
            headers=self.email_header)
        return response.json()

    def get_first_n_emails_from_inbox_contains_subject(self, n: int = 10, subject: str = None, isread: bool = False):
        """
                This method is used to get all emails from inbox based on subject and read status
                :param subject:  Subject of the email
                :param isread: is read or not
                :return: It will return first n mails in dict
                """
        response = requests.get(
            url=self.GRAPH_ENDPOINT + f"$filter=contains(subject, '{subject}') and isRead eq {str(isread).lower()}&$top={n} ",
            headers=self.email_header)
        return response.json()

    def download_email_attachments(self, message_id: str, save_folder: str) -> (bool, list):
        """
                This method is used to get all emails from inbox based on subject and read status
                :param subject:  Subject of the email
                :param isread: is read or not
                :return: It will return first n mails in dict
                """
        try:
            GRAPH_API_ATTACHMENT = GraphAPIEndpoints.attachment_endpoint.value.format(self.mail_id, message_id)
            response = requests.get(
                url=GRAPH_API_ATTACHMENT,
                headers=self.email_header)
            attachment_items = response.json()['value']
            saved_fullpath = []
            for attachment in attachment_items:
                file_name = attachment['name']
                attachment_id = attachment['id']
                attachment_content = requests.get(
                    url=GRAPH_API_ATTACHMENT + f"/{attachment_id}/$value",
                    headers=self.email_header
                )
                if not os.path.exists(save_folder):
                    os.makedirs(save_folder)
                report_path = os.path.join(save_folder, file_name)
                with open(report_path, 'wb') as _f:
                    _f.write(attachment_content.content)
                saved_fullpath.append(os.path.abspath(report_path))
            return True, saved_fullpath
        except Exception as e:
            return False, []

    def get_user_info_with_name(self, name):
        """
        :param name:name of the user
        :return: Detials of the users with provided name
        """
        response = requests.get(
            url=self.graph_users_endpoint + f"?$filter=startsWith(displayName,'{name}')",
            headers=self.email_header)
        return response.json()

    def get_emails_for_last_day(self, subject: str = None, isread: bool = False, time_delta: str = None):
        """
            This method is used to get all the emails within a timeframe based on timedelta
            :param subject: Subject of the email
            :param isread: is read or not
            :param time_delta: threshold time
            :return: It will return emails with the subject with received time greater than the time_delta
        """
        response = requests.get(
            url=self.GRAPH_ENDPOINT + f"$filter=contains(subject, '{subject}') and isRead eq {str(isread).lower()} and receivedDateTime gt {time_delta} ",
            headers=self.email_header)
        return response.json()

    def download_email_hli_attachments(self, message_id: str) -> (bool, list):
        """
                This method is used to get all emails from inbox based on subject and read status
                :param subject:  Subject of the email
                :param isread: is read or not
                :return: It will return first n mails in dict
                """
        try:
            graph_api_attachment = GraphAPIEndpoints.attachment_endpoint.value.format(self.mail_id, message_id)
            response = requests.get(
                url=graph_api_attachment,
                headers=self.email_header)
            attachment_items = response.json()['value']
            return attachment_items
        except Exception as e:
            log.info(msg=f'error message while downloading attachment {e}')
            return False, []

    def save_attachment(self, attachment_id, message_id: str):
        graph_api_attachment = GraphAPIEndpoints.attachment_endpoint.value.format(self.mail_id, message_id)
        attachment_content = requests.get(
            url=graph_api_attachment + f"/{attachment_id}/$value",
            headers=self.email_header
        )
        return attachment_content
