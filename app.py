from flask import Flask, render_template, jsonify, request
import random
from collections import deque
import heapq

app = Flask(__name__)

# Default maze size (adjustable later)
ROWS, COLS = 25, 35
WALL, PATH = 1, 0

def generate_maze():
    maze = [[WALL for _ in range(COLS)] for _ in range(ROWS)]

    def carve_from(r, c):
        maze[r][c] = PATH
        directions = [(0,2),(0,-2),(2,0),(-2,0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == WALL:
                maze[r + dr//2][c + dc//2] = PATH
                carve_from(nr, nc)

    carve_from(0, 0)
    maze[0][0] = PATH
    maze[ROWS-1][COLS-1] = PATH
    return maze

# BFS that returns exploration order + final path
def bfs_with_exploration(maze, start, end):
    ROWS, COLS = len(maze), len(maze[0])
    q = deque([start])
    parent = {start: None}
    explored = []
    found = False

    while q:
        node = q.popleft()
        explored.append(node)
        if node == end:
            found = True
            break
        r, c = node
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            n = (nr, nc)
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == PATH and n not in parent:
                parent[n] = node
                q.append(n)

    # reconstruct path
    path = []
    if found:
        cur = end
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
    return explored, path

# A* that returns exploration order + final path
def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar_with_exploration(maze, start, end):
    ROWS, COLS = len(maze), len(maze[0])
    gscore = {start: 0}
    fscore = {start: manhattan(start, end)}
    parent = {}
    open_heap = []
    heapq.heappush(open_heap, (fscore[start], start))
    open_set = {start}
    closed = set()
    explored = []

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        open_set.discard(current)
        closed.add(current)
        explored.append(current)

        if current == end:
            break

        r, c = current
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            neighbor = (nr, nc)
            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue
            if maze[nr][nc] == WALL:
                continue
            tentative_g = gscore[current] + 1
            if tentative_g < gscore.get(neighbor, float('inf')):
                parent[neighbor] = current
                gscore[neighbor] = tentative_g
                fscore[neighbor] = tentative_g + manhattan(neighbor, end)
                if neighbor not in open_set and neighbor not in closed:
                    heapq.heappush(open_heap, (fscore[neighbor], neighbor))
                    open_set.add(neighbor)

    # reconstruct path
    path = []
    if end in parent or start == end:
        cur = end
        # include end even if it's start
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur, None)
            if cur == start and start not in path:
                path.append(start)
                break
        path.reverse()
        # ensure start included if missing
        if path and path[0] != start:
            path.insert(0, start)
    return explored, path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate")
def generate():
    maze = generate_maze()
    return jsonify(maze)

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    maze = data.get("maze")
    start = tuple(data.get("start", (0,0)))
    end = tuple(data.get("end", (len(maze)-1, len(maze[0])-1)))
    algo = data.get("algo", "astar")
    if algo == "bfs":
        explored, path = bfs_with_exploration(maze, start, end)
    else:
        explored, path = astar_with_exploration(maze, start, end)
    # Convert tuples to lists for JSON
    explored_list = [[r,c] for (r,c) in explored]
    path_list = [[r,c] for (r,c) in path]
    return jsonify({"explored": explored_list, "path": path_list})

if __name__ == "__main__":
    app.run(debug=True)


