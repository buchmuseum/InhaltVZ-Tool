"""
Zusammenführung der Keyword-Komponenten.

Steuert:
- Laden der IDNs
- Laden der Schlagwörter
- Analyse
- Ergebnisaufbereitung
"""


from __future__ import annotations


import logging

import pandas as pd


from pathlib import Path


from core.keyword import KeywordEngine
from core.keyword_loader import KeywordLoader


from infrastructure.storage import StorageManager



logger = logging.getLogger(__name__)




class KeywordService:


    def __init__(
        self,
        storage: StorageManager
    ):

        self.storage = storage

        self.loader = KeywordLoader()

        self.engine = KeywordEngine()



    def execute(
        self,
        input_file: Path,
        keyword_file: Path,
        output_file: Path,
        minimum_score: int,
        cancel_event=None,
        progress=None
    ):
        """
        Führt komplette Keywordanalyse aus.
        """


        logger.info(
            "Keyword Workflow gestartet"
        )


        # -----------------------------
        # IDNs laden
        # -----------------------------

        df = self.storage.read_excel(
            input_file
        )


        if "IDN" not in df.columns:

            raise ValueError(
                "Keine IDN-Spalte gefunden"
            )


        ids = (
            df["IDN"]
            .dropna()
            .astype(str)
            .tolist()
        )



        # -----------------------------
        # Schlagwörter laden
        # -----------------------------


        keywords = self.loader.load(
            keyword_file
        )



        # -----------------------------
        # Analyse
        # -----------------------------


        results = self.engine.analyse_many(
            ids,
            keywords,
            minimum_score,
            cancel_event,
            progress
        )



        # -----------------------------
        # Ergebnis erzeugen
        # -----------------------------


        rows = []


        for result in results:

            rows.append({

                "IDN":
                    result.idn,

                "Schlagwörter":
                    "; ".join(
                        result.keywords
                    ),

                "Gewichtung":
                    result.score,

                "URL":
                    result.url

            })



        result_df = pd.DataFrame(
            rows
        )


        self.storage.save_dataframe(
            result_df,
            output_file
        )


        logger.info(
            "Keyword Workflow beendet"
        )


        return len(results)