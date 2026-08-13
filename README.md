
# InhaltsVZ-Tool

Version 1.0.0


## Zweck

Daa InhaltsVZ-Tool unterstützt die Verarbeitung von
bibliografischen Daten der Deutschen Nationalbibliothek. Es bildet eine Ergebnissmenge von Datensätzen mit
Inhaltsverzeichnissen. Danach durchsucht es diese nach festgelegten Stichwörtern und gibt anhand einer Gewichtung 
Treffer in Excel aus. 

Funktionen:

- OAI-PMH Harvest
- IDN Verwaltung
- Stichwortanalyse
- SRU/MARC21 Aktualisierung
- Excel Export


---

# Systemanforderungen


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

│ └── stichwort.xlsx

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

idn.txt.gz bitte entpacken. Diese enthält den Stand 14.Juli 2026

## schlagworte.xlsx

Benötigte Spalten:

| Begriff | Gewichtung |
|-|-|
| künstliche intelligenz | 5 |
| datenbank | 2 |


---

# Ablauf

## 1. Harvest

Der OAI-Harvester lädt neue Datensätze im gewählten Zeitraum.
Ergebnis:
data/DNB_OAI.xlsx

Abfrage mit idn.txt um schon einmal bearbeitete Datensätze rauszufiltern.

## 2. Keyword Analyse

Die Datei:
data/stichwort.xlsx
wird geladen.

Inhaltsverzeichnise der IDN aus DNB_OAI.xlsx werden geöffnet und mit den Stichwörtern abgeglichen.

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


Aktuelle Struktur:

InhaltsVZ-Tool/

├── main.py
├── config.ini
├── requirements.txt
├── README.md

├── data/
│   ├── idn.txt
│   └── stichwort.xlsx

├── logs/

├── config/
│   └── settings.py
│   └── version.py

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


# Hinweis: Das Tool wird ohne Gewähr zur Verfügung gestellt. Die Nutzung erfolgt auf eigene Verantwortung. Bitte prüfen Sie die erzeugten Ergebnisse vor einer weiteren Verwendung.