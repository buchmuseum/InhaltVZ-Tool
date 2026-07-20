"""
IDN-Verwaltung

Verantwortlich:
- Vergleich von DNB-IDNs
- Ermittlung neuer Datensätze
- Bereinigung von Listen

Keine GUI!
Keine direkte Dateiverarbeitung!
"""


from __future__ import annotations


import logging

from typing import Iterable


logger = logging.getLogger(__name__)




class IDNManager:
    """
    Verwaltung von DNB-IDN-Listen.
    """



    def compare(
        self,
        remote_ids: Iterable[str],
        local_ids: Iterable[str]
    ) -> dict[str, set[str]]:
        """
        Vergleicht externe und lokale IDNs.

        Rückgabe:

        {
            "neu": {...},
            "vorhanden": {...},
            "entfernen": {...}
        }

        """


        remote = set(
            str(x).strip()
            for x in remote_ids
            if str(x).strip()
        )


        local = set(
            str(x).strip()
            for x in local_ids
            if str(x).strip()
        )


        result = {

            "neu":
                remote - local,

            "vorhanden":
                remote & local,

            "entfernen":
                local - remote
        }



        logger.info(
            "IDN Vergleich: %s neu, %s vorhanden",
            len(result["neu"]),
            len(result["vorhanden"])
        )


        return result




    def merge(
        self,
        existing: Iterable[str],
        additions: Iterable[str]
    ) -> set[str]:
        """
        Führt zwei IDN-Mengen zusammen.
        """


        merged = set(existing)


        merged.update(
            additions
        )


        logger.info(
            "IDN Merge: %s Einträge",
            len(merged)
        )


        return merged




    def filter_existing(
        self,
        ids: Iterable[str],
        existing: Iterable[str]
    ) -> list[str]:
        """
        Entfernt bereits bekannte IDNs.
        """


        known = set(existing)


        result = [
            i
            for i in ids
            if i not in known
        ]


        logger.info(
            "%s IDNs nach Filter übrig",
            len(result)
        )


        return result