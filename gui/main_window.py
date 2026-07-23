"""
Tkinter Oberfläche

Verantwortlich:
- Benutzerinteraktion
- Anzeige
- Start von Hintergrundaufgaben

Keine Fachlogik!
"""


from __future__ import annotations


import logging
import threading
import tkinter as tk
import platform
from datetime import datetime
from tkinter import ttk, messagebox


from pathlib import Path

from config.version import VERSION
from core.harvest import OAIHarvester
from core.keyword import KeywordEngine
from core.sru import SRUClient
from core.idn import IDNManager
from core.sru_service import SRUService

from core.keyword_service import KeywordService


from infrastructure.storage import StorageManager


from config.settings import (
    DATA_DIR,
    IDN_FILE,
    DEFAULT_OUTPUT,
    KEYWORD_FILE,
    HARVEST_OUTPUT,
    KEYWORD_OUTPUT,
    RESULT_OUTPUT
)



logger = logging.getLogger(__name__)




class MainWindow:


    def __init__(self, root: tk.Tk):

        self.root = root

        self.root.title(
            "InhaltsVZ-Tool"
        )

        self.root.geometry(
            "900x750"
        )


        self.cancel_event = threading.Event()



        self.storage = StorageManager(
            DATA_DIR
        )
        self.sru_service = SRUService(
            self.storage
        )

        self.harvester = OAIHarvester()

        self.keyword_engine = KeywordEngine()

        self.keyword_service = KeywordService(
            self.storage
        )

        self.sru = SRUClient()

        self.idn = IDNManager()

        self.sru_title = tk.BooleanVar()
        self.sru_subtitle = tk.BooleanVar()
        self.sru_author = tk.BooleanVar()
        self.sru_publisher = tk.BooleanVar()
        self.root.title(f"InhaltsVZ-Tool {VERSION}"
)



        self.build_ui()



    # -------------------------------------------------
    # GUI
    # -------------------------------------------------

    def build_ui(self):

        # Hauptframe
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=50, pady=10)

        # Spaltenbreiten
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)

# =========================
# Info Button
# =========================
        header = ttk.Frame(main_frame)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")

        header.columnconfigure(0, weight=1)

        ttk.Label(
        header,
        text=f"InhaltsVZ-Tool {VERSION}",
        font=("Segoe UI", 12, "bold")
    ).grid(row=0, column=0, sticky="w")

        ttk.Button(
            header,
            text="ℹ",
            width=3,
            command=self.show_about
        ).grid(row=0, column=1, sticky="e")

# =========================
# OAI HARVEST
# =========================


        ttk.Label(
            main_frame,
            text="OAI HARVEST",
            font=("Segoe UI", 10, "bold")
        ).grid(row=1, column=0, columnspan=2, pady=(0,10))

        harvest_text = (
                "1. Start- und Enddatum eingeben\n"
                "2. Harvest starten“ anklicken.\n" 
                "   Es werden alle Datensätze des TOC-Sets (Inhaltsverzeichnisse) innerhalb des gewählten Zeitraums ermittelt\n"
                "3. Abfrage idn.txt\n"
                "   Nach Abschluss können die ermittelten IDNs mit der Datei idn.txt abgeglichen werden.\n"
                "   Bereits bekannte IDNs werden entfernt, neue IDNs in die idn.txt gespeichert.\n" 
     
        )


        ttk.Label(
            main_frame,
            text=harvest_text,
            justify="left"
        ).grid(row=2, column=0, sticky="w", padx=(0,40))


        harvest_input = ttk.Frame(main_frame)
        harvest_input.grid(row=2, column=1, sticky="nw")


        ttk.Label(
            harvest_input,
            text="Startdatum (YYYY-MM-DD)"
        ).pack(anchor="w")

        self.start_date = ttk.Entry(
            harvest_input
        )
        self.start_date.pack(
            pady=2
        )


        ttk.Label(
            harvest_input,
            text="Enddatum (YYYY-MM-DD)"
        ).pack(anchor="w")

        self.end_date = ttk.Entry(
            harvest_input
        )
        self.end_date.pack(
            pady=2
        )


        ttk.Button(
            harvest_input,
            text="Harvest starten",
            command=self.start_harvest
        ).pack(
            pady=5
        )

# =========================
# KEYWORD ANALYSE
# =========================

        ttk.Label(
            main_frame,
            text="Keyword Analyse",
            font=("Segoe UI", 10, "bold")
        ).grid(row=3, column=0, columnspan=2, pady=(20,5))


        keyword_text = (
                "1. Mindestgewichtung festlegen (Standard: 3)\n"
                "2. „Analyse starten“ anklicken\n"
                " - Die Inhaltsverzeichnisse werden nach den definierten Stichwörtern durchsucht.\n" 
                "   Treffer werden auch innerhalb von Wortbestandteilen erkannt.\n" 
                "   Nur Datensätze mit ausreichender Gesamtgewichtung werden gespeichert.\n"
        )

        ttk.Label(
            main_frame,
            text=keyword_text,
            justify="left"
        ).grid(row=4, column=0, sticky="w", padx=(0,40))


        keyword_input = ttk.Frame(main_frame)
        keyword_input.grid(row=4, column=1, sticky="nw")


        self.minimum_score = ttk.Entry(keyword_input)
        self.minimum_score.pack()

        self.minimum_score.insert(
            0,
            "3"
        )    

        ttk.Button(
            keyword_input,
            text="Analyse starten",
            command=self.start_keyword
        ).pack(pady=5)

# =========================
# SRU UPDATE
# =========================

        ttk.Label(
            main_frame,
            text="SRU Update",
            font=("Segoe UI", 10, "bold")
        ).grid(row=5, column=0, columnspan=2, pady=(20,5))


        sru_text = (
                "1. Gewünschte Metadaten auswählen\n"
                "2. „SRU Update starten“ anklicken.\n"
                " - Die ausgewählten bibliografischen Angaben werden über die\n"
                "   SRU-Schnittstelle ergänzt und in der Ergebnisdatei gespeichert"
        )

        ttk.Label(
            main_frame,
            text=sru_text,
            justify="left"
        ).grid(row=6, column=0, sticky="w", padx=(0,40))


        sru_input = ttk.Frame(main_frame)
        sru_input.grid(row=6, column=1, sticky="nw")


        ttk.Checkbutton(
            sru_input,
            text="Titel",
            variable=self.sru_title
        ).pack(anchor="w")


        ttk.Checkbutton(
            sru_input,
            text="Zusatztitel",
            variable=self.sru_subtitle
        ).pack(anchor="w")


        ttk.Checkbutton(
            sru_input,
            text="Autor",
            variable=self.sru_author
        ).pack(anchor="w")


        ttk.Checkbutton(
            sru_input,
            text="Verlag",
            variable=self.sru_publisher
        ).pack(anchor="w")


        ttk.Button(
            sru_input,
            text="SRU Update starten",
            command=self.start_sru
        ).pack(pady=5)


        self.status = tk.Text(
            self.root,
            height=10
        )

        self.status.pack(
            fill="both",
            expand=True
        )



        ttk.Button(
            self.root,
            text="STOP",
            command=self.stop
        ).pack(
            pady=10
        )



    # -------------------------------------------------
    # STATUS
    # -------------------------------------------------

    def log(
        self,
        text: str
    ):

        self.root.after(
            0,
            lambda:
            self.status.insert(
                "1.0",
                text + "\n"
            )
        )



    # -------------------------------------------------
    # HARVEST
    # -------------------------------------------------

    def start_harvest(self):

        start = self.start_date.get().strip()
        ende = self.end_date.get().strip()

        # Datum prüfen
        try:
            datetime.strptime(start, "%Y-%m-%d")
            datetime.strptime(ende, "%Y-%m-%d")

        except ValueError:
            messagebox.showerror(
                "Ungültiges Datum",
                "Bitte Start- und Enddatum im Format YYYY-MM-DD eingeben.\n\n"
                "Beispiel: 2026-07-23"
            )
            return


        self.cancel_event.clear()

        self.log(
            "Harvest gestartet..."
        )

        thread = threading.Thread(
            target=self.harvest_worker,
            daemon=True
        )

        thread.start()



    def harvest_worker(self):

        try:

            ids = self.harvester.harvest(
                self.start_date.get(),
                self.end_date.get(),
                self.cancel_event,
                self.log
            )


            self.storage.replace_excel(
                HARVEST_OUTPUT,
                ids
            )


            self.log(
                f"{len(ids)} IDNs gespeichert"
            )


            # ---------------------------------
            # IDN Vergleich
            # ---------------------------------

            answer = messagebox.askyesno(
                "IDN Vergleich",
                "Ermittelte IDNs mit idn.txt vergleichen?"
            )


            if answer:

                self.log(
                    "IDN-Abgleich gestartet..."
                )


                existing_ids = self.storage.load_idn_file(
                    IDN_FILE
                )


                comparison = self.idn.compare(
                    ids,
                    existing_ids
                )


                new_ids = sorted(
                    comparison["neu"]
                )


                duplicates = len(
                    comparison["vorhanden"]
                )


                result = {
                    "duplicates": duplicates,
                    "new_ids": len(new_ids)
                }


                # Excel auf neue Datensätze reduzieren

                self.storage.replace_excel(
                    HARVEST_OUTPUT,
                    new_ids
                )


                # idn.txt aktualisieren

                self.storage.append_idns(
                    IDN_FILE,
                    new_ids
                )


                self.log(
                    f"IDN-Abgleich fertig:"
                )

                self.log(
                    f"{result['duplicates']} Duplikate entfernt"
                )

                self.log(
                    f"{result['new_ids']} neue IDNs übernommen"
                )

            else:

                self.log(
                    "IDN-Abgleich übersprungen"
                )


        except Exception as exc:

            logger.exception(
                "Harvest Fehler"
            )

            messagebox.showerror(
                "Fehler",
                str(exc)
            )

    # -------------------------------------------------
    # KEYWORDS
    # -------------------------------------------------

    def start_keyword(self):

        self.cancel_event.clear()


        thread = threading.Thread(
            target=self.keyword_worker,
            daemon=True
        )

        thread.start()



    def keyword_worker(self):

        try:

            minimum = int(
                self.minimum_score.get()
            )


            count = self.keyword_service.execute(

                HARVEST_OUTPUT,

                KEYWORD_FILE,

                KEYWORD_OUTPUT,

                minimum,

                self.cancel_event,

                self.log
            )


            self.log(
                f"{count} Treffer gespeichert"
            )


        except Exception as exc:

            logger.exception(
                "Keyword Workflow Fehler"
            )


            messagebox.showerror(
                "Fehler",
                str(exc)
            )
    # -------------------------------------------------
    # SRU
    # -------------------------------------------------

    def start_sru(self):

        self.cancel_event.clear()


        threading.Thread(
            target=self.sru_worker,
            daemon=True
        ).start()



    def sru_worker(self):

        try:

            count = self.sru_service.execute(

                RESULT_OUTPUT,

                RESULT_OUTPUT,

                self.sru_title.get(),

                self.sru_subtitle.get(),

                self.sru_author.get(),

                self.sru_publisher.get(),

                self.cancel_event,

                self.log
            )

            self.log(
                f"SRU abgeschlossen: {count} Datensätze"
            )


        except Exception as exc:

            logger.exception(
                "SRU Fehler"
            )


            messagebox.showerror(
                "Fehler",
                str(exc)
            )

    # -------------------------------------------------
    # STOP
    # -------------------------------------------------

    def stop(self):

        self.cancel_event.set()

        self.log(
            "Abbruch angefordert"
        )
    # -------------------------------------------------
    # Infobox Text
    # -------------------------------------------------

    def show_about(self):

        messagebox.showinfo(
            "Über InhaltsVZ-Tool",
            f"""InhaltsVZ-Tool

    Version: {VERSION}

    Entwickelt von:
    Isabell Sickert

    Deutsche Nationalbibliothek
    Deutsches Buch- und Schriftmuseum

    Python: {platform.python_version()}
    """
        )