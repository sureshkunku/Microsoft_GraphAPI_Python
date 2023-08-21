from typing import List
import requests
import logging
from graphapi.token import Token
from graphapi.mail_body import create_message_data
from graphapi.constants import Access_Keys, GraphAPIEndpoints
import json

log = logging.getLogger(__name__)


class MailSender:
    def __init__(self, mail_id: str, data: dict) -> None:
        """
            Create an connection client with all of the specified parameters.
        Args:
            mail_id: Mail id
            data: data containing confidentail info
        Returns:
            None
        """
        self.GRAPH_ENDPOINT = GraphAPIEndpoints.send_mail_endpoint.value.format(mail_id)
        self.token = Token(data)


def send_mail(self, message: str, ):
    """
    Send an e-mail using graph api.
    Args:
        message: str
    Returns:
        Response
    Raises:
        Exception: Raised when given to_address argument is of str type.
    """
    response = self.token.post()
    authorization_token = f"{response[Access_Keys.TokenType.value]} {response[Access_Keys.AccessToken.value]}"
    email_header = {
        Access_Keys.Authorization.value: authorization_token,
        Access_Keys.ContentType.value: "application/json",
    }
    iteration = 0
    exe = None
    while iteration < 5:
        try:
            response = requests.post(url=self.GRAPH_ENDPOINT, headers=email_header, data=json.dumps(message))
            log.info(f"email sent {response}")
            return response
        except Exception as e:
            exe = e
            log.info(f"email send retry {iteration}")
            iteration += 1
        else:
            log.error("unable to send email ", exe)


def send_email(self, to_addresses: List[str], subject: str, message_body: str, attachment_paths: List[str] = [],
               cc_list: List[str] = []):
    """
    Sends email for close wo
    Args:
        to_addresses (List[str]): emails to send
        subject (str): subject of mail
        message_body (str): body of mail
        cc_list (List[str]): List to email to put cc into.
    Returns:
        Response
    """
    mail_body = create_message_data(to_addresses, subject, message_body, attachment_paths, cc_recipients=cc_list)
    response = self.send_mail(message=mail_body)
    return response
