"""
OAI-PMH Harvest Modul

Verantwortlich:
- Abfrage der DNB OAI-Schnittstelle
- Verarbeitung von ListIdentifiers
- Rückgabe von IDNs

Keine GUI!
Keine Dateischreiboperationen!
"""

from __future__ import annotations


import logging
import threading
from typing import Callable


import xml.etree.ElementTree as ET


from infrastructure.http_client import HttpClient
from config.settings import DNB_OAI_URL



logger = logging.getLogger(__name__)



OAI_NAMESPACE = {
    "oai": "http://www.openarchives.org/OAI/2.0/"
}



ProgressCallback = Callable[[str], None]



class OAIHarvester:


    def __init__(
        self,
        http_client: HttpClient | None = None
    ):

        self.http = (
            http_client
            if http_client
            else HttpClient()
        )



    def harvest(
        self,
        start_date: str,
        end_date: str,
        cancel_event: threading.Event | None = None,
        progress: ProgressCallback | None = None
    ) -> list[str]:
        """
        Führt einen OAI-PMH Harvest aus.

        Gibt eine Liste von DNB-IDNs zurück.
        """


        identifiers: list[str] = []

        token: str | None = None



        logger.info(
            "OAI Harvest gestartet %s - %s",
            start_date,
            end_date
        )



        while True:


            if cancel_event and cancel_event.is_set():

                logger.warning(
                    "Harvest durch Benutzer abgebrochen"
                )

                break



            if token:

                url = (
                    f"{DNB_OAI_URL}"
                    f"?verb=ListIdentifiers"
                    f"&resumptionToken={token}"
                )

            else:

                url = (
                    f"{DNB_OAI_URL}"
                    f"?verb=ListIdentifiers"
                    f"&from={start_date}T00:00:00Z"
                    f"&until={end_date}T23:59:59Z"
                    f"&metadataPrefix=oai_dc"
                    f"&set=dnb:toc"
                )



            response = self.http.get(url)



            try:

                root = ET.fromstring(
                    response.text
                )


            except ET.ParseError:

                logger.exception(
                    "Ungültiges XML erhalten"
                )

                raise



            for header in root.findall(
                ".//oai:header",
                OAI_NAMESPACE
            ):

                identifier = header.find(
                    "oai:identifier",
                    OAI_NAMESPACE
                )


                if identifier is not None:

                    value = identifier.text


                    if value:

                        idn = value.split("/")[-1]

                        identifiers.append(idn)



            token_element = root.find(
                ".//oai:resumptionToken",
                OAI_NAMESPACE
            )



            if (
                token_element is None
                or not token_element.text
            ):

                break



            token = (
                token_element.text.strip()
            )



            if progress:

                progress(
                    f"{len(identifiers)} IDNs geladen"
                )



        logger.info(
            "OAI Harvest beendet: %s IDNs",
            len(identifiers)
        )


        return identifiers