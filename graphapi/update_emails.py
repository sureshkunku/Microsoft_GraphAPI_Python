from graphapi.token import Token
from graphapi.constants import Access_Keys, GraphAPIEndpoints, Message_Keys
import requests
import json


class UpdateEmails():
    def __init__(self, mail_id, data):
        self.GRAPH_ENDPOINT = GraphAPIEndpoints.update_mail_endoint.value.format(mail_id)
        self.token = Token(data)
        self.response = self.token.post()
        self.authorization_token = f"{self.response[Access_Keys.TokenType.value]} {self.response[Access_Keys.AccessToken.value]}"
        self.email_header = {
            Access_Keys.Authorization.value: self.authorization_token,
            Access_Keys.ContentType.value: "application/json",
        }

    def mark_mail_as_read(self, message_id):
        data = {Message_Keys.isRead.value: Message_Keys.true.value}
        response = requests.patch(url=self.GRAPH_ENDPOINT + f"{message_id}", headers=self.email_header,
                                  data=json.dumps(data))
        return response.json()
