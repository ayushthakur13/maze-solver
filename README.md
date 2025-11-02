# 🧠 AI-Based Maze Solver using BFS and A* Algorithm

An intelligent maze-solving application that demonstrates how classical AI search algorithms, such as Breadth-First Search (BFS) and A*, efficiently discover the optimal path between two points in a dynamically generated maze.

---

## 🚀 Overview

This project demonstrates how **state-space search** and **heuristic reasoning** can be applied to solve navigation problems.  
It includes both a **Tkinter GUI** and a **Flask web interface** for real-time visualization of the pathfinding process.

---

## 🧩 Features

- 🌀 **Random Maze Generation**  
- 🔍 **Pathfinding using BFS and A\***  
- 💡 **Heuristic (Manhattan Distance)** for A\*  
- 🎨 **Real-time Visualization** of search and solution  
- 🌐 **Dual Interface:** Tkinter GUI + Flask Web App  
- 📊 **Performance Comparison** between BFS and A\*

---

## 🧠 Algorithms Used

| Algorithm | Type | Description |
|------------|------|-------------|
| **BFS** | Uninformed Search | Explores level by level; guarantees shortest path |
| **A\*** | Informed Search | Uses heuristic to reach goal faster and efficiently |

**Heuristic Used:** Manhattan Distance → `|x1 - x2| + |y1 - y2|`

---

## ⚙️ Tech Stack

- **Language:** Python  
- **Libraries:** `Tkinter`, `Flask`, `NumPy`  
- **Tools:** VS Code / PyCharm  
- **Version:** Python 3.10+

---

## 🧰 Installation & Usage

```bash
# Clone the repository
git clone https://github.com/ayushthakur13/maze-solver.git
cd maze-solver

# Install dependencies
pip install flask numpy

# Run Flask web app
python app.py

# OR run Tkinter GUI
python maze_gui.py

```

Open your browser at http://localhost:5000 to see the solver in action.
