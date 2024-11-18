#!/bin/bash

# Running hyperparameters
NUM_TESTS=5
H_FLAGS=("grey" "b/w")

# Paths
SERVER_PATH="$(pwd)/../Test"
PLAYER_PATH="$SERVER_PATH/../LoDaLe_tablut"

# Svuota o crea la cartella Test/outputs
OUTPUTS_DIR="./outputs"
if [ -d "$OUTPUTS_DIR" ]; then
    echo "Cleaning outputs directory..."
    rm -R "$OUTPUTS_DIR"
fi
mkdir -p "$OUTPUTS_DIR"

# Esegui le partite
echo "Starting games..."
for ((i=1; i<=NUM_TESTS; i++)); do
    for h_flag in "${H_FLAGS[@]}"; do
        echo "Test $i with flag $h_flag"

        # Percorsi dei file di log per questa run
        SERVER_LOG="$OUTPUTS_DIR/server_test${i}_${h_flag}.log"
        WHITE_LOG="$OUTPUTS_DIR/white_test${i}_${h_flag}.log"
        BLACK_LOG="$OUTPUTS_DIR/black_test${i}_${h_flag}.log"

        # Avvia il server
        java -jar "$SERVER_PATH/Server.jar" > "$SERVER_LOG" 2>&1 &
        SERVER_PID=$!

        # Dai tempo al server per avviarsi completamente
        sleep 1

        # Avvia i giocatori
        python3 "$PLAYER_PATH/PLAYER.py" WHITE 60 127.0.0.1 "$h_flag" > "$WHITE_LOG" 2>&1 &
        WHITE_PID=$!
        python3 "$PLAYER_PATH/PLAYER.py" BLACK 60 127.0.0.1 "$h_flag" > "$BLACK_LOG" 2>&1 &
        BLACK_PID=$!

        # DEBUG
        echo "Listening enabled. Logs are being written to:"
        echo "  Server log: $SERVER_LOG"
        echo "  White player log: $WHITE_LOG"
        echo "  Black player log: $BLACK_LOG"
        
        # Aspetta che i processi completino
        wait $SERVER_PID
        wait $WHITE_PID
        wait $BLACK_PID
    done
done

# 3. Copia la cartella in games_executor/logs
echo "Copying logs to ./logs directory..."
mkdir -p "./logs"
cp -R "$OUTPUTS_DIR/"* "./logs/"

echo "All tests completed!"
