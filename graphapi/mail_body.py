import os, base64
import logging
from typing import List
from graphapi.constants import Message_Keys

log = logging.getLogger(__name__)


def get_recipients_list(to_address: List[str]):
    """
    :param to_address: All recipients list
    :return: returns recipients in dict format
    """
    recipients_list = []
    for mail in to_address:
        recipients_list.append({Message_Keys.emailAddress.value: {Message_Keys.address.value: mail}})
    return recipients_list


def draft_attachment(file_path):
    """
    :param file_path: File location
    :return: Sends file/image in dict format
    """
    if not os.path.exists(file_path):
        log.info('file is not found')
        return
    with open(file_path, 'rb') as upload:
        media_content = base64.b64encode(upload.read())
        data_body = {
            '@odata.type': '#microsoft.graph.fileAttachment',
            'contentBytes': media_content.decode('utf-8'),
            'name': os.path.basename(file_path)
        }
    return data_body


def create_message_data(to_address: List[str], subject: str, message_body: str, attachments: List = [],
                        cc_recipients: List[str] = []):
    """
    :param to_address: emails to send
    :param subject: subject of mail
    :param message_body: body of the mail
    :param attachments: file/image attachments
    :param cc_recipients: cc_recipients if any
    :return: Returns complete mail in dict format
    """
    email_body = {
        Message_Keys.message.value: {
            Message_Keys.subject.value: subject,
            Message_Keys.body.value: {
                Message_Keys.content_type.value: Message_Keys.html.value,
                Message_Keys.content.value: message_body
            },
            Message_Keys.recipients.value: get_recipients_list(to_address),
            Message_Keys.ccRecipients.value: get_recipients_list(cc_recipients),
            Message_Keys.attachments.value: [draft_attachment(i) for i in attachments],
        },
    }
    return email_body
