"""
SRU / MARC21 Modul

Verantwortlich:
- Abfrage der DNB SRU-Schnittstelle
- Verarbeitung von MARC21-XML
- Extraktion bibliografischer Daten

Keine GUI!
Keine Dateiverarbeitung!
"""


from __future__ import annotations


import logging
from dataclasses import dataclass


import xml.etree.ElementTree as ET


from infrastructure.http_client import HttpClient
from config.settings import DNB_SRU_URL



logger = logging.getLogger(__name__)



@dataclass
class BibliographicRecord:
    """
    Bibliografische Grunddaten.
    """

    idn: str

    titel: str = ""

    zusatztitel: str = ""

    autor: str = ""

    verlag: str = ""



class SRUClient:
    """
    SRU-Client für DNB MARC21 Daten.
    """



    MARC_NAMESPACE = {
        "marc": "http://www.loc.gov/MARC21/slim"
    }



    def __init__(
        self,
        http_client: HttpClient | None = None
    ):

        self.http = (
            http_client
            if http_client
            else HttpClient()
        )



    def fetch(
        self,
        idn: str
    ) -> BibliographicRecord:
        """
        Holt einen MARC21 Datensatz.
        """



        url = (
            f"{DNB_SRU_URL}"
            f"?version=1.1"
            f"&operation=searchRetrieve"
            f"&query=idn={idn}"
            f"&recordSchema=MARC21-xml"
        )



        try:

            response = self.http.get(
                url
            )


            return self.parse_marc(
                idn,
                response.text
            )



        except Exception:

            logger.exception(
                "SRU Fehler bei IDN %s",
                idn
            )


            return BibliographicRecord(
                idn=idn
            )



    def parse_marc(
        self,
        idn: str,
        xml_text: str
    ) -> BibliographicRecord:
        """
        Parst MARC21 XML.
        """


        try:

            root = ET.fromstring(
                xml_text
            )


        except ET.ParseError:

            logger.exception(
                "Ungültiges MARC XML"
            )

            return BibliographicRecord(
                idn=idn
            )



        record = root.find(
            ".//marc:record",
            self.MARC_NAMESPACE
        )


        if record is None:

            return BibliographicRecord(
                idn=idn
            )



        return BibliographicRecord(

            idn=idn,

            titel=self.get_subfield(
                record,
                "245",
                "a"
            ),

            zusatztitel=self.get_subfield(
                record,
                "245",
                "b"
            ),

            autor=(
                self.get_subfield(
                    record,
                    "100",
                    "a"
                )
                or
                self.get_subfield(
                    record,
                    "110",
                    "a"
                )
            ),

            verlag=(
                self.get_subfield(
                    record,
                    "264",
                    "b"
                )
                or
                self.get_subfield(
                    record,
                    "260",
                    "b"
                )
            )
        )



    def get_subfield(
        self,
        record,
        tag: str,
        code: str
    ) -> str:
        """
        Liest ein MARC21 Unterfeld.
        """


        for field in record.findall(
            "marc:datafield",
            self.MARC_NAMESPACE
        ):

            if field.attrib.get(
                "tag"
            ) != tag:

                continue



            for subfield in field.findall(
                "marc:subfield",
                self.MARC_NAMESPACE
            ):

                if subfield.attrib.get(
                    "code"
                ) == code:

                    return (
                        subfield.text.strip()
                        if subfield.text
                        else ""
                    )


        return ""