"""
SRU Workflow Service

Verantwortlich:
- Ergebnisdatei laden
- SRU Daten abrufen
- Datensätze erweitern
- Ergebnis zurückgeben

Keine GUI!
"""

from __future__ import annotations


import logging
from pathlib import Path


import pandas as pd


from core.sru import SRUClient
from infrastructure.storage import StorageManager


logger = logging.getLogger(__name__)



class SRUService:
    """
    Verbindet SRUClient und Storage.
    """



    def __init__(
        self,
        storage: StorageManager
    ):

        self.storage = storage
        self.client = SRUClient()



    def execute(
        self,
        input_file: Path,
        output_file: Path,
        update_title: bool = True,
        update_subtitle: bool = True,
        update_author: bool = True,
        update_publisher: bool = True,
        cancel_event=None,
        progress=None
    ) -> int:
        """
        Führt SRU Aktualisierung aus.
        """


        logger.info(
            "SRU Workflow gestartet"
        )



        df = self.storage.read_excel(
            input_file
        )


        if "IDN" not in df.columns:

            raise ValueError(
                "Keine IDN-Spalte vorhanden"
            )



        total = len(df)


        for index, row in df.iterrows():


            if (
                cancel_event
                and cancel_event.is_set()
            ):

                logger.warning(
                    "SRU abgebrochen"
                )

                break



            idn = str(
                row["IDN"]
            )


            record = self.client.fetch(
                idn
            )



            if update_title:

                df.at[
                    index,
                    "Titel"
                ] = record.titel



            if update_subtitle:

                df.at[
                    index,
                    "Zusatztitel"
                ] = record.zusatztitel



            if update_author:

                df.at[
                    index,
                    "Autor"
                ] = record.autor



            if update_publisher:

                df.at[
                    index,
                    "Verlag"
                ] = record.verlag



            if progress:

                progress(
                    f"SRU {index + 1}/{total}"
                )



        self.storage.save_dataframe(
            df,
            output_file
        )


        logger.info(
            "SRU Workflow beendet"
        )


        return total