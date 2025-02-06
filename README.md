## A* Pathfinding Algorithm Visualization 🗺️

This Python program visualizes the A* pathfinding algorithm using Pygame. It includes different visualizations such as a grid with random obstacles, hexagonal grids, and a snake game pathfinding.

### Requirements

* Python 3.x
* Pygame

### How to Run

1. Make sure you have Pygame installed (`pip install pygame`).
2. Save the code as a Python file (e.g., `a_star.py`, `hexagons.py`, or `snake_astar.py`).
3. Run the desired file from your terminal:
    * For grid visualization: `python a_star.py`
    * For hexagonal grid visualization: `python hexagons.py`
    * For snake game pathfinding: `python snake_astar.py`

### How it Works

* **Grid:** The program creates a grid of squares. ⬜
* **Hexagonal Grid:** The program creates a grid of hexagons for pathfinding.
* **Snake Game:** The program uses A* to find the path for a snake in a grid.
* **Obstacles:** Random cells are blocked to represent obstacles. 🧱
* **A\* Algorithm:** The A* search algorithm is used to find the shortest path from the start to the end point.
    * **Heuristic:** Manhattan distance is used as the heuristic function to estimate the distance to the end.
    * **Priority Queue:** A priority queue (`heapq`) is used to store and retrieve the next cell to explore based on its f-score (cost + heuristic).
* **Visualization:** Pygame is used to visualize the grid, obstacles, visited cells, and the final path. 

### Features

* **Random Obstacles:** The number of obstacles is randomly generated within a defined range.
* **Visualization:** The algorithm's progress is visualized in real-time, showing visited cells and the current path.
* **Start and End Points:** The start and end points are fixed at the top-left and bottom-right corners of the grid.

### Customization

* **Grid Size:** You can adjust the `ROWS`, `COLS`, and `SQUARE_SIZE` constants to change the grid dimensions.
* **Obstacle Density:** Modify `MIN_BLOCKS` and `MAX_BLOCKS` to control the number of obstacles.
* **Colors:** Change the color constants to customize the appearance.
* **Sleep Time:** Adjust `SLEEP_TIME` to control the speed of the visualization.

### Potential Improvements

* **Interactive Obstacles:** Allow the user to place obstacles manually. ✏️
* **Different Heuristics:** Implement other heuristic functions (e.g., Euclidean distance).
* **Diagonal Movement:** Allow diagonal movement in the pathfinding. ↗️
* **Maze Generation:** Integrate maze generation algorithms to create more complex environments. 🌀
* **GUI:** Add a graphical user interface for controlling parameters and starting the algorithm. 🖱️
