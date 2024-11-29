#!/bin/bash

# Running hyperparameters
NUM_TESTS=1                                     # each run should be deterministic
H_FLAGS=("grey" "flag_1" "flag_2" "flag_3")     # TODO: aggiungere le flags
player_flag="search"

# Paths
# Server is in current directory to simplify the process
PLAYER_PATH="../LoDaLe_tablut"

# Create and empty dir for the player outputs
OUTPUTS_DIR="./outputs"
if [ -d "$OUTPUTS_DIR" ]; then
    echo "Cleaning outputs directory..."
    rm -R "$OUTPUTS_DIR"
fi
mkdir -p "$OUTPUTS_DIR"

LOG_DIR="./logs"
if [ -d "$LOG_DIR" ]; then
    echo "Cleaning logs directory..."
    rm -R "$LOG_DIR"
fi
mkdir -p "$LOG_DIR"

# Extracy the list of competing heuristics
for ((i = 0; i < ${#H_FLAGS[@]}; i++)); do
    for ((j = i + 1; j < ${#H_FLAGS[@]}; j++)); do
        PAIRS+=("${H_FLAGS[i]} ${H_FLAGS[j]}")
        # We also have to switch them since black and white are not symmetrical
        PAIRS+=("${H_FLAGS[j]} ${H_FLAGS[i]}") 
    done
done

# Start executing matches
echo "Starting games..."
TOTAL_MATCHES=$((NUM_TESTS * ${#PAIRS[@]}))
CURRENT_MATCH=0
BAR_WIDTH=50

for ((i=1; i<=NUM_TESTS; i++)); do
    for pair in "${PAIRS[@]}"; do 
        # Update progress bar
        ((CURRENT_MATCH++))
        PERCENT=$((CURRENT_MATCH * 100 / TOTAL_MATCHES))
        FILLED=$((PERCENT * BAR_WIDTH / 100))
        EMPTY=$((BAR_WIDTH - FILLED))

        # Extract the single heuristics
        heuristic_1=$(echo "$pair" | awk '{print $1}')
        heuristic_2=$(echo "$pair" | awk '{print $2}')

        # REAL LOADING BAR WITHOUT DEBUG
        printf "\r[%-${BAR_WIDTH}s] %d%% (%d/%d)" \
            "$(printf '#%.0s' $(seq 1 $FILLED))" "$PERCENT" "$CURRENT_MATCH" "$TOTAL_MATCHES"
        
        # debug loading bar
        # printf "\r[%-${BAR_WIDTH}s] %d%% (%d/%d) - Launching %s vs %s..." \
        #     "$(printf '#%.0s' $(seq 1 $FILLED))" "$PERCENT" "$CURRENT_MATCH" "$TOTAL_MATCHES" "$heuristic_1" "$heuristic_2"

        # Paths for log files
        SERVER_LOG="$OUTPUTS_DIR/server_${heuristic_1}_${heuristic_2}.log"
        WHITE_LOG="$OUTPUTS_DIR/white_${heuristic_1}_in_match_${heuristic_1}_vs_${heuristic_2}.log"
        BLACK_LOG="$OUTPUTS_DIR/black_${heuristic_2}_in_match_${heuristic_1}_vs_${heuristic_2}.log"

        # Create files 
        touch "$SERVER_LOG" "$WHITE_LOG" "$BLACK_LOG"

        # Run the server
        java -jar "Server.jar" > "$SERVER_LOG" 2>&1 &
        SERVER_PID=$!

        # Give time to the server to fully initialize
        sleep 1

        # Run the players
        python3 "$PLAYER_PATH/PLAYER.py" WHITE 60 127.0.0.1 "$player_flag" "$heuristic_1" > "$WHITE_LOG" 2>&1 &
        WHITE_PID=$!
        python3 "$PLAYER_PATH/PLAYER.py" BLACK 60 127.0.0.1 "$player_flag" "$heuristic_2" > "$BLACK_LOG" 2>&1 &
        BLACK_PID=$!
        
        # Wait server and players
        wait $SERVER_PID
        wait $WHITE_PID
        wait $BLACK_PID

        # debug loading bar
        # printf "\r[%-${BAR_WIDTH}s] %d%% (%d/%d) - Match %s vs %s... done\n" \
        #     "$(printf '#%.0s' $(seq 1 $FILLED))" "$PERCENT" "$CURRENT_MATCH" "$TOTAL_MATCHES" "$heuristic_1" "$heuristic_2"
    done
done

# New line after the bar
echo 

# Server writes all in /logs, we delete non useful (noisy) files for parsing
echo "Deleting non-gamelogs..."
find "./logs" -type f ! -name "*_vs_*" -delete

# Parse the file to obtain the dataset
echo "Start parsing log files:"
python3 extractor.py
