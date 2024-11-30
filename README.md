# LoDaLe Group

LoDaLe is a Python client for the Ashton Tablut game developed for the tablut-challenge at University of Bologna. 

## Project Structure

```
.
├── LoDaLe_tablut
│   ├── PLAYER.py          # Main player logic and game loop
│   ├── board.py           # Board representation and utility functions
│   ├── heuristics.py      # Heuristic functions for evaluating board states
│   ├── search.py          # Search algorithms like Breadth-first and Alpha-Beta Pruning
│   ├── socket_manager.py  # Socket communication with the game server
│   └── utils.py           # General utility functions
|
├── Test
│   ├── Server.jar         # Game server for testing the client
│   └── logs               # Logs generated during gameplay
|
├── dataset                # Parsed dataset given from previous years
│   ├── ...
├── games_executor         # Application for comparing different players
│   ├── ...
|
├── run_game.sh            # Script for launching the game
├── run_game.bat           # Script for launching the game
```

## Launching

In order to launch the player type 
```
python3 PLAYER.py <color_player> <timeout> <server_ip>
```

## Contribution

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of the changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
Developed with ❤️ by Lorenzo Pellegrino, Leonardo Massaro and Davide Ligabue.
