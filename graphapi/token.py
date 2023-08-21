from typing import Dict, Union
import requests
import logging
from requests.exceptions import HTTPError
from graphapi.constants import GraphAPIEndpoints, Access_Keys

log = logging.getLogger(__name__)


class Token:
    """
    Generate bearer token to access the Graph API
    """

    def __init__(self, data):
        """
        Intialise the url
        Args:
            url : URL
        """
        self.url = GraphAPIEndpoints.get_token_endpoint.value
        self.data = data
        self.header = {
            Access_Keys.host.value: GraphAPIEndpoints.host.value,
        }

    def post(self) -> Union[Dict, str]:
        """
        Sends GET Request.
        Args:
            header (dict) : headerdata
        Returns:
            Response
        Raises:
            Http Error Exceptions.
        """
        try:
            response = requests.post(self.url, headers=self.header, data=self.data, timeout=60)  # no
            log.info(f"Response:{response.text}")
        except HTTPError as http_err:
            log.info(f"HTTP error occurred: {http_err}")
            raise GraphapiException(f"HTTP error occurred: {http_err}")
        except Exception as err:
            log.info(f"Other error occurred: {err}")
            raise GraphapiException(f"Other error occurred: {err}")
        return response.json()


class GraphapiException(Exception):
    """Graphapi Exception"""
    pass
