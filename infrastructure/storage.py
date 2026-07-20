"""
Zentrale Speicherfunktionen.

Verantwortlich:
- Excel-Dateien lesen/schreiben
- IDN-Dateien verwalten
- sichere Dateipfade
- Backup vorhandener Dateien

Keine GUI!
Keine Fachlogik!
"""


from __future__ import annotations


import logging
import shutil
from datetime import datetime
from pathlib import Path

from typing import Iterable


import openpyxl
import pandas as pd



logger = logging.getLogger(__name__)




class StorageError(Exception):
    """
    Eigener Fehler für Speicherprobleme.
    """
    pass





class StorageManager:


    def __init__(
        self,
        base_path: Path
    ):

        self.base_path = base_path

        self.base_path.mkdir(
            exist_ok=True
        )



    # -------------------------------------------------
    # BACKUP
    # -------------------------------------------------

    def create_backup(
        self,
        file_path: Path
    ) -> None:
        """
        Erstellt eine Sicherheitskopie,
        bevor Dateien überschrieben werden.
        """


        if not file_path.exists():

            return



        timestamp = (
            datetime.now()
            .strftime("%Y%m%d_%H%M%S")
        )


        backup = (
            file_path.parent
            /
            f"{file_path.stem}_{timestamp}.bak"
        )


        try:

            shutil.copy2(
                file_path,
                backup
            )


            logger.info(
                "Backup erstellt: %s",
                backup
            )


        except OSError:

            logger.exception(
                "Backup konnte nicht erstellt werden"
            )

            raise StorageError(
                "Backup fehlgeschlagen"
            )



    # -------------------------------------------------
    # IDN EXCEL
    # -------------------------------------------------

    def save_idns_excel(
        self,
        idns: Iterable[str],
        file_path: Path
    ) -> None:
        """
        Speichert IDNs als XLSX.
        """


        self.create_backup(
            file_path
        )


        try:

            workbook = openpyxl.Workbook()

            sheet = workbook.active

            sheet.title = "DNB_IDNs"


            sheet.append(
                ["IDN"]
            )


            for idn in idns:

                sheet.append(
                    [idn]
                )


            workbook.save(
                file_path
            )


            workbook.close()



            logger.info(
                "%s IDNs gespeichert",
                len(list(idns))
            )



        except Exception:

            logger.exception(
                "Excel speichern fehlgeschlagen"
            )

            raise StorageError(
                "Excel-Datei konnte nicht gespeichert werden"
            )



    # -------------------------------------------------
    # IDN TXT
    # -------------------------------------------------

    def load_idn_file(
        self,
        file_path: Path
    ) -> set[str]:
        """
        Liest vorhandene IDNs.
        """


        if not file_path.exists():

            return set()



        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return {
                    line.strip()
                    for line in file
                    if line.strip()
                }



        except OSError:

            logger.exception(
                "IDN-Datei konnte nicht gelesen werden"
            )

            raise StorageError(
                "IDN-Datei Lesefehler"
            )



    def append_idns(
        self,
        file_path: Path,
        idns: Iterable[str]
    ) -> int:
        """
        Fügt neue IDNs hinzu.

        Rückgabe:
        Anzahl neuer Einträge.
        """


        existing = self.load_idn_file(
            file_path
        )


        new_entries = (
            set(idns)
            -
            existing
        )


        if not new_entries:

            return 0



        try:

            with open(
                file_path,
                "a",
                encoding="utf-8"
            ) as file:


                for idn in sorted(new_entries):

                    file.write(
                        idn + "\n"
                    )



            logger.info(
                "%s neue IDNs geschrieben",
                len(new_entries)
            )


            return len(new_entries)



        except OSError:

            logger.exception(
                "IDN Schreiben fehlgeschlagen"
            )

            raise StorageError(
                "IDN-Datei konnte nicht gespeichert werden"
            )



    # -------------------------------------------------
    # EXCEL LESEN
    # -------------------------------------------------

    def read_excel(
        self,
        file_path: Path
    ) -> pd.DataFrame:
        """
        Liest Excel-Datei.
        """


        try:

            return pd.read_excel(
                file_path,
                dtype=str
            )


        except Exception:

            logger.exception(
                "Excel Lesen fehlgeschlagen"
            )

            raise StorageError(
                "Excel-Datei konnte nicht gelesen werden"
            )
        
    def replace_excel(
        self,
        file_path: Path,
        idns: list[str]
    ) -> None:
        """
        Erstellt eine neue Excel-Datei.
        
        Vorhandene Datei wird ersetzt.
        """

        if file_path.exists():

            self.create_backup(
                file_path
            )

            file_path.unlink()


        self.save_idns_excel(
            idns,
            file_path
        )

    def save_dataframe(
        self,
        dataframe: pd.DataFrame,
        file_path: Path
    ) -> None:
        """
        Speichert ein DataFrame als Excel.

        Vorhandene Datei wird gesichert.
        """


        self.create_backup(
            file_path
        )


        try:

            dataframe.to_excel(
                file_path,
                index=False
            )


            logger.info(
                "Excel gespeichert: %s",
                file_path
            )


        except Exception:

            logger.exception(
                "DataFrame konnte nicht gespeichert werden"
            )

            raise StorageError(
                "Excel Export fehlgeschlagen"
            )