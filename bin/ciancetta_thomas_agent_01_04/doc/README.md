# AGENT

**Tags**
*wmi, python, os, nic, usb, net, event, inventory, windows, uptime, update, software, agent, yaml, lan, database, server*

## Descrizione

- Il programma legge un file che contiene nomi di pc e scrive le informazioni delle schede di rete, del sistema operativo e delle porte usb utilizzate su file separati. 
- Inoltre le informazioni della scheda di rete vengono espense con il venditore della scheda di rete e gli indirizzi MAC normalizzati.
- Il programma scrive su un file di output le attività recenti svolte sulla macchina.
- Il programma scrive su un file di output i software installati sulla macchina sulla quale viene eseguito.
- Il programma scrive su un file di output update disponibili sulla macchina e uptime delle macchine in input.
- Il programma scrive alcune informazioni su un database.

## Esecuzione

- Fare doppio click sul file agent.bat oppure farlo partire da linea comando.
- Di default il programma non esegue la funzione event viewer, per eseguirla modificare il file config.yaml sostituendo il parametro eventviewer-yes-or-no da "no" a "yes".
- Di default il programma non esegue la funzione di sync, per eseguirla modificare il file config.yaml sostituendo il parametro sync-path da "sync_path" al path voluto.
- Il separatore di default per la standardizzazione dell'indirizzo MAC è ";", per modificarlo cambiare il parametro mac-spearator del file config.yaml da ";" a quello interessato.
- É possibile modificare i path dei file di output modificando i parametri del file config.yaml.

## Esempio di esecuzione

- agent.bat

## Output

- Tabelle csv nella cartella flussi
- Tabelle su database

## Autore

- Ciancetta Thomas, Francesco Maria Giacomi

## Directory

- ciancetta_thomas_agent_01_03
    - bin
        - agent.py
        - agent.ps1
        - agent.bat
        - config.yaml
        - USBDview.exe
    - doc
        - images
            - immagine
        - nicepage.css
        - nicepage.js
        - README.css
        - README.md
        - README.html
    - flussi
        - computers.csv
        - eventviewer.csv
        - logicaldisk.csv
        - netinfo.csv
        - osversion.csv
        - product.csv
        - updatepending.csv
        - uptime.csv
        - usb.csv
    - log
        - log.log
        - batch_log.log
    - sync
        - computers.csv
        - eventviewer.csv
        - logicaldisk.csv
        - netinfo.csv
        - osversion.csv
        - product.csv
        - updatepending.csv
        - uptime.csv
        - usb.csv

## Prerequisites

- python3
- wmi
- PyYAML
- requests

## Python version

- Coded and tested in: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
- To test: Python < 3.8.2

## Working OS

- Windows 10
- To test: Windows < 10

## Changelog

#### 01.03 - 2021-03-08

##### Added
- Upload informazioni su database

##### Changed
- README.md

##### Removed
- 

#### 01.02 - 2020-12-14

##### Added
- Normalizzazione MAC Address 
- Parametri di default
- Commenti nel codice
- Uptime e updatepending
- Inventory software

##### Changed
- README.md
- Funzione di ping
- Bellezza del codice python
- Bug fixes

##### Removed
- Spazi vuoti inutili

#### 01.01 - 2020-11-30

##### Added
- Creato

##### Changed
- 

##### Removed
- 