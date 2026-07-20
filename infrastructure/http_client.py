"""
Zentrale HTTP-Komponente.

Alle Netzwerkzugriffe laufen hierüber.
"""

import logging

import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import DEFAULT_TIMEOUT


logger = logging.getLogger(
    __name__
)



class HttpClient:


    def __init__(self):

        self.session = requests.Session()


        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[
                500,
                502,
                503,
                504
            ],
            allowed_methods=[
                "GET"
            ]
        )


        adapter = HTTPAdapter(
            max_retries=retry
        )


        self.session.mount(
            "https://",
            adapter
        )



    def get(
        self,
        url: str
    ) -> requests.Response:

        try:

            logger.info(
                "GET %s",
                url
            )


            response = self.session.get(
                url,
                timeout=DEFAULT_TIMEOUT
            )


            response.raise_for_status()


            return response


        except requests.RequestException:

            logger.exception(
                "HTTP Fehler bei %s",
                url
            )

            raise