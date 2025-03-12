# Conway’s Game of Life Simulator

This project is a simulation of Conway's Game of Life using Python and Pygame. The Game of Life is a cellular automaton devised by mathematician John Conway. It consists of a grid of cells that evolve through a number of generations according to a set of rules.

**Made by Hyu**

## Game Rules

1. **Underpopulation**: A live cell with fewer than 2 live neighbors dies.
2. **Survival**: A live cell with 2 or 3 live neighbors survives.
3. **Overpopulation**: A live cell with more than 3 live neighbors dies.
4. **Reproduction**: A dead cell with exactly 3 live neighbors becomes alive.

## Features

- Toggle the state of individual cells by clicking on them.
- Start or pause the simulation with the Spacebar.
- Reset the grid with the 'R' key.
- Randomize the grid with the 'D' key.
- Adjust simulation speed with the Up and Down arrow keys.
- Save the current grid state with the 'S' key.
- Load a saved grid state with the 'L' key.
- Load predefined patterns like "glider" with the 'P' key.
- Resize the window to dynamically adjust the grid size.

## Controls

- **Mouse Click**: Toggle cell state (alive/dead).
- **Spacebar**: Start/Pause the simulation.
- **R key**: Reset the grid.
- **D key**: Randomize the grid.
- **Up Arrow**: Increase simulation speed.
- **Down Arrow**: Decrease simulation speed.
- **S key**: Save the grid state.
- **L key**: Load the grid state.
- **P key**: Load a "glider" pattern.

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install Pygame using pip:
   ```
   pip install pygame
   ```
3. Run the simulator:
   ```
   python game_of_life.py
   ```

## License

This project is licensed under the MIT License.
