
# DNB Tool

Version 2.0.0


## Zweck

Das DNB Tool unterstützt die Verarbeitung von
bibliografischen Daten der Deutschen Nationalbibliothek.

Funktionen:

- OAI-PMH Harvest
- IDN Verwaltung
- Schlagwortanalyse
- SRU/MARC21 Aktualisierung
- Excel Export


---

# Systemanforderungen

## Betriebssystem

- Windows 10 / Windows 11


## Python

Empfohlen:

Python 3.11 oder neuer


---

# Installation

Pakete installieren:
pip install -r requirements.txt


# Verzeichnisstruktur
├── data/

│ ├── idn.txt

│ └── schlagworte.xlsx

├── logs/

├── core/

├── gui/

└── infrastructure/

# Daten

## idn.txt

Enthält bereits bekannte DNB-IDNs.

Beispiel:
123456789
987654321

## schlagworte.xlsx

Benötigte Spalten:

| Begriff | Gewichtung |
|-|-|
| künstliche intelligenz | 5 |
| datenbank | 2 |


---

# Ablauf

## 1. Harvest

Der OAI-Harvester lädt neue Datensätze.

Ergebnis:
## schlagworte.xlsx

Benötigte Spalten:

| Begriff | Gewichtung |
|-|-|
| künstliche intelligenz | 5 |
| datenbank | 2 |


---

# Ablauf


## 1. Harvest

Der OAI-Harvester lädt neue Datensätze.

Ergebnis:
data/DNB_OAI.xlsx

## 2. Keyword Analyse

Die Datei:
data/schlagworte.xlsx
wird geladen.

Die Treffer werden gespeichert:
data/ergebnis.xlsx

## 3. SRU Aktualisierung

MARC21 Daten werden ergänzt:

- Titel
- Zusatztitel
- Autor
- Verlag


---

# Logging
Die Anwendung erzeugt:

logs/dnb_tool.log
Die Logdatei enthält:

- Start
- Fehler
- Netzwerkprobleme
- Verarbeitungsschritte

---

# Sicherheit
Umgesetzte Maßnahmen:

- zentrale Fehlerbehandlung
- Logging
- Timeout bei Netzwerkzugriffen
- Retry bei temporären Fehlern
- getrennte Module
- keine GUI-Fachlogik
- kontrollierte Dateiverarbeitung

---

# Architektur
GUI

↓

Services

↓

Core Module

↓

Infrastructure

↓

Dateien / Netzwerk

---

# Lizenz

Interne Nutzung.

5. Projektstand jetzt

Aktuelle Struktur:

DNB_Tool/

├── main.py
├── config.ini
├── requirements.txt
├── README.md

├── data/
│   ├── idn.txt
│   └── schlagworte.xlsx

├── logs/

├── config/
│   └── settings.py

├── core/
│   ├── harvest.py
│   ├── idn.py
│   ├── keyword.py
│   ├── keyword_loader.py
│   ├── keyword_service.py
│   ├── sru.py
│   └── sru_service.py

├── infrastructure/
│   ├── http_client.py
│   ├── logging_config.py
│   └── storage.py

├── gui/
│   └── main_window.py

└── tests/
    └── test_idn.py

