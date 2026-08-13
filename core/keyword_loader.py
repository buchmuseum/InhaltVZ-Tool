"""
Lädt und validiert die Stichwortdefinitionen.

Quelle:
data/stichworte.xlsx

Erwartete Spalten:
- Begriff
- Gewichtung
"""


from __future__ import annotations


import logging
from pathlib import Path


import pandas as pd



logger = logging.getLogger(__name__)




class KeywordLoadError(Exception):
    """
    Fehler beim Laden der Stichwörter.
    """
    pass




class KeywordLoader:
    """
    Lädt Keyword-Definitionen aus Excel.
    """



    REQUIRED_COLUMNS = {
        "Begriff",
        "Gewichtung"
    }



    def load(
        self,
        file_path: Path
    ) -> dict[str, int]:
        """
        Liest Stichwörter und Gewichtungen.

        Rückgabe:

        {
            "begriff": gewicht
        }
        """



        if not file_path.exists():

            raise KeywordLoadError(
                f"Datei nicht gefunden: {file_path}"
            )



        try:

            df = pd.read_excel(
                file_path,
                dtype=str
            )



        except Exception as exc:

            logger.exception(
                "Stichwortdatei konnte nicht gelesen werden"
            )

            raise KeywordLoadError(
                "Excel-Datei ungültig"
            ) from exc



        df.columns = (
            df.columns
            .str.strip()
        )



        missing = (
            self.REQUIRED_COLUMNS
            -
            set(df.columns)
        )


        if missing:

            raise KeywordLoadError(
                f"Fehlende Spalten: {missing}"
            )



        result: dict[str, int] = {}



        for _, row in df.iterrows():


            term = str(
                row["Begriff"]
            ).strip().lower()



            if not term:

                continue



            try:

                weight = int(
                    row["Gewichtung"]
                )


            except ValueError:

                logger.warning(
                    "Ungültige Gewichtung für %s",
                    term
                )

                continue



            result[term] = weight



        logger.info(
            "%s Stichwörter geladen",
            len(result)
        )


        return result