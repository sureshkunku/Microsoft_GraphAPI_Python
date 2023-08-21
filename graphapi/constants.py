from enum import Enum


class Access_Keys(Enum):
    ClientID = 'client_id'
    ClientSecret = 'client_secret'
    Scope = 'scope'
    Authorization = 'Authorization'
    Bearer = 'Bearer '
    AccessToken = 'access_token'
    GrantType = 'grant_type'
    TokenType = 'token_type'
    ContentType = 'Content-Type'
    host = 'Host'


class Message_Keys(Enum):
    message = 'message'
    subject = 'subject'
    body = 'body'
    content_type = 'contentType'
    content = 'content'
    recipients = 'toRecipients'
    ccRecipients = 'ccRecipients'
    attachments = 'attachments'
    text = 'Text'
    html = 'HTML'
    emailAddress = 'emailAddress'
    address = "address"
    false = "false"
    true = "true"
    isRead = "isRead"
    value = 'value'


class GraphAPIEndpoints(Enum):
    host = 'login.microsoftonline.com'
    send_mail_endpoint = "https://graph.microsoft.com/v1.0/users/{}/sendMail"
    fetch_mails_endpoint = "https://graph.microsoft.com/v1.0/users/{}/messages? "
    attachment_endpoint = "https://graph.microsoft.com/v1.0/users/{}/messages/{}/attachments"
    get_token_endpoint = "https://login.microsoftonline.com/fffcdc91-d561-4287-aebc-78d2466eec29/oauth2/v2.0/token"
    update_mail_endoint = "https://graph.microsoft.com/v1.0/users/{}/messages/"
    user_end_point = "https://graph.microsoft.com/v1.0/users"
