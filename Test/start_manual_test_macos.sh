#!/bin/bash

# Apri una nuova finestra e avvia il server
osascript -e 'tell application "Terminal" to do script "cd '$(pwd)' && java -jar ./Server.jar"'

# Apri una nuova finestra e avvia il client WHITE
osascript -e 'tell application "Terminal" to do script "cd '$(pwd)/..' && python3 LoDaLe_tablut WHITE 60 127.0.0.1"'

# Apri una nuova finestra e avvia il client BLACK
osascript -e 'tell application "Terminal" to do script "cd '$(pwd)/..' && python3 LoDaLe_tablut BLACK 60 127.0.0.1"'
