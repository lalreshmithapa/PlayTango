# 🌗 Tango Puzzle Game

Welcome to the **Tango Puzzle Game** — a visual, interactive, and intelligent puzzle solver developed in Python using Pygame. This project features:

- 🧠 **Manual Mode** – play the puzzle yourself!
- ⭐ **A\*** – solve the puzzle with the A\* search algorithm.
- 🔁 **AC-3 + Backtracking** – solve using constraint propagation and backtracking with visual arc consistency.
- 🤖 **Q-Learning Agent** – solve the puzzle using reinforcement learning with visual feedback and self-improvement.

---

## 📂 Project Structure

```
tango_project/
├── tango.py                  # Main entry point with CLI
├── manual/
│   └── play.py               # Manual (human play) mode
├── solvers/
│   ├── astar.py # A* search solver
│   ├── ac3.py # AC-3 with backtracking solver
│   └── qlearning.py # Q-learning visual solver (self-learning agent)
├── game/
│   ├── grid_setup.py         # Initializes grid and locked cells
│   ├── constraints.py        # Game rules and constraint checking logic
├── assets/
│   └── images/               # sun.png, moon.png
```

---

## ▶️ How to Run

Make sure you have **Python ≥ 3.8** and **Pygame** installed:

```bash
pip install pygame
```

### 💡 Run the Game:

```bash
# Play manually (human player)
python tango.py -m manual

# Solve with A* search algorithm
python tango.py -m astar

# Solve with AC-3 + backtracking
python tango.py -m ac3

# Solve with Q-learning agent
python tango.py -m qlearn

```

---

## 🎮 Game Rules

- The board is a 6x6 grid.
- Cells can contain either a 🌞 **sun**, 🌚 **moon**, or be **empty**.
- Some cells are locked with predefined values.
- **Constraints include**:
  - No more than 3 suns or moons in any row or column.
  - No three identical symbols consecutively in any row or column.
  - Special directional constraints (e.g., adjacent cells must or must not match values).

---

## 🧠 Features

| Mode     | Description                                                                                                                           |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `manual` | Play the game manually using mouse clicks (left-click to place, cycle, or clear cells). Undo and Clear options included.              |
| `astar`  | Automatically solves the puzzle using A\* with a visual step-by-step update.                                                          |
| `ac3`    | Uses Arc Consistency (AC-3) followed by Backtracking to solve the puzzle visually. Highlights inconsistent arcs during solving.       |
| `qlearn` | Uses a Q-learning agent with top-left-to-bottom-right serial assignment, backtracking on invalid moves, and visual learning feedback. |

---

## 🖼️ Assets

Place the following image assets inside `assets/images/`:

- `sun.png`
- `moon.png`

> 📝 Make sure images are scaled appropriately or use Pygame's `transform.scale()` in code.

---

## 🧩 Credits & Acknowledgements

Developed by **Suraj Thapa**, **Sadiksha Chitrakar**, and **Lal Bahadur Reshmi Thapa** as part of University of New Haven’s [Intro to AI Project](https://catalog.newhaven.edu/preview_program.php?catoid=31&poid=8818&returnto=2075).

---

## 📜 License

This project is open-source and intended for educational and personal use. Contributions and forks are welcome!
