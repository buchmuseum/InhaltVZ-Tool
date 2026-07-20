"""
Keyword-Analyse Modul

Verantwortlich:
- Laden von Schlagwortdefinitionen
- Analyse von Dokumenttexten
- Berechnung von Gewichtungen

Keine GUI!
Keine direkte Dateiverarbeitung!
"""


from __future__ import annotations


import logging
import re
import threading

from dataclasses import dataclass
from typing import Callable


from bs4 import BeautifulSoup


from infrastructure.http_client import HttpClient


logger = logging.getLogger(__name__)



ProgressCallback = Callable[[str], None]



@dataclass
class KeywordResult:
    """
    Ergebnis einer Keywordanalyse.
    """

    idn: str
    url: str
    keywords: list[str]
    score: int



class KeywordEngine:
    """
    Führt die Schlagwortanalyse durch.
    """



    def __init__(
        self,
        http_client: HttpClient | None = None
    ):

        self.http = (
            http_client
            if http_client
            else HttpClient()
        )



    def analyse_text(
        self,
        text: str,
        keywords: dict[str, int]
    ) -> tuple[list[str], int]:
        """
        Durchsucht Text nach Schlagwörtern.

        Treffer auch innerhalb von Wortbestandteilen.
        Beispiel:
        Begriff: "recht"
        Treffer:
        - Rechtswissenschaft
        - Urheberrecht
        - Arbeitsrecht
        """

        text = text.lower()

        hits = []
        score = 0


        for word, weight in keywords.items():

            pattern = (
                rf"\b\w*{re.escape(word.lower())}\w*\b"
            )


            matches = re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )


            if matches:

                hits.append(word)

                score += weight


        return hits, score


    def analyse_document(
        self,
        idn: str,
        keywords: dict[str, int]
    ) -> KeywordResult:
        """
        Analysiert ein DNB Dokument.
        """


        url = (
            f"https://d-nb.info/{idn}/04/text"
        )


        try:

            response = self.http.get(
                url
            )


            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )


            text = soup.get_text(
                separator=" "
            )


            hits, score = self.analyse_text(
                text,
                keywords
            )


            return KeywordResult(
                idn=idn,
                url=url,
                keywords=hits,
                score=score
            )


        except Exception:

            logger.exception(
                "Keywordanalyse fehlgeschlagen für %s",
                idn
            )


            return KeywordResult(
                idn=idn,
                url=url,
                keywords=[],
                score=0
            )



    def analyse_many(
        self,
        ids: list[str],
        keywords: dict[str, int],
        minimum_score: int = 0,
        cancel_event: threading.Event | None = None,
        progress: ProgressCallback | None = None
    ) -> list[KeywordResult]:
        """
        Analysiert mehrere Dokumente.
        """



        results = []



        total = len(ids)



        for index, idn in enumerate(ids, start=1):


            if cancel_event and cancel_event.is_set():

                logger.warning(
                    "Keywordanalyse abgebrochen"
                )

                break



            result = self.analyse_document(
                idn,
                keywords
            )



            if result.score >= minimum_score:

                results.append(
                    result
                )



            if progress:

                progress(
                    f"{index}/{total} analysiert"
                )



        logger.info(
            "Keywordanalyse beendet: %s Treffer",
            len(results)
        )


        return results