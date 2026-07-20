"""
Zentrale Anwendungseinstellungen.

Keine Fachlogik!
Nur Konfiguration.
"""

from pathlib import Path


APP_NAME = "DNB Tool"
APP_VERSION = "2.0.0"


BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

DATA_DIR = BASE_DIR / "data"


LOG_FILE = LOG_DIR / "dnb_tool.log"


# DNB Schnittstellen

DNB_OAI_URL = (
    "https://services.dnb.de/oai/repository"
)


DNB_SRU_URL = (
    "https://services.dnb.de/sru/dnb"
)


DEFAULT_TIMEOUT = 30


DEFAULT_OUTPUT = (
    DATA_DIR / "ergebnis.xlsx"
)


IDN_FILE = (
    DATA_DIR / "idn.txt"
)


KEYWORD_FILE = (
    DATA_DIR / "schlagworte.xlsx"
)

HARVEST_OUTPUT = (
    DATA_DIR / "DNB_OAI.xlsx"
)


KEYWORD_OUTPUT = (
    DATA_DIR / "ergebnis.xlsx"
)

RESULT_OUTPUT = (
    DATA_DIR / "ergebnis.xlsx"
)