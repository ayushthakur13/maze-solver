
const canvas = document.getElementById("mazeCanvas");
const ctx = canvas.getContext("2d");
const generateBtn = document.getElementById("generateBtn");
const solveBtn = document.getElementById("solveBtn");
const algoSelect = document.getElementById("algoSelect");
const speedRange = document.getElementById("speedRange");

let maze = [];
let cellSize = 20; // adjusted to fit; will be recalculated for large screens
let explored = [];
let path = [];

async function generateMaze() {
  const res = await fetch("/generate");
  maze = await res.json();
  adjustCellSizeAndCanvas();
  drawMaze();
}

function adjustCellSizeAndCanvas() {
  // make cellSize such that maze fits in viewport width comfortably
  const maxWidth = Math.min(window.innerWidth - 40, 1000);
  const cols = maze[0].length;
  const rows = maze.length;
  cellSize = Math.floor(maxWidth / cols);
  if (cellSize < 6) cellSize = 6;
  canvas.width = cols * cellSize;
  canvas.height = rows * cellSize;
}

function drawMaze() {
  for (let r = 0; r < maze.length; r++) {
    for (let c = 0; c < maze[0].length; c++) {
      ctx.fillStyle = maze[r][c] === 1 ? "#0b0b0b" : "#ffffff";
      ctx.fillRect(c * cellSize, r * cellSize, cellSize, cellSize);
    }
  }
  // start and end markers
  ctx.fillStyle = "green";
  ctx.fillRect(0, 0, cellSize, cellSize);
  ctx.fillStyle = "red";
  ctx.fillRect((maze[0].length - 1) * cellSize, (maze.length - 1) * cellSize, cellSize, cellSize);
}

async function solveMaze() {
  if (!maze || maze.length === 0) return;
  const start = [0, 0];
  const end = [maze.length - 1, maze[0].length - 1];
  const algo = algoSelect.value;

  // send to backend
  const res = await fetch("/solve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ maze, start, end, algo })
  });
  const data = await res.json();
  explored = data.explored || [];
  path = data.path || [];

  if ((!path || path.length === 0) && (!explored || explored.length === 0)) {
    alert("No path found and no exploration returned.");
    return;
  }

  await animateExplorationThenPath();
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function animateExplorationThenPath() {
  drawMaze();
  const delay = parseInt(speedRange.value); // ms
  // draw exploration (lighter color)
  for (let i = 0; i < explored.length; i++) {
    const [r, c] = explored[i];
    // skip start & end
    if ((r === 0 && c === 0) || (r === maze.length-1 && c === maze[0].length-1)) continue;
    ctx.fillStyle = "#a0d2ff"; // exploration color
    ctx.fillRect(c * cellSize, r * cellSize, cellSize, cellSize);
    if (i % 5 === 0) await sleep(delay); // batch small groups to speed up large mazes
  }

  // short pause before drawing final path
  await sleep(Math.max(60, delay));

  // draw final path (highlight)
  for (let i = 0; i < path.length; i++) {
    const [r, c] = path[i];
    if ((r === 0 && c === 0) || (r === maze.length-1 && c === maze[0].length-1)) continue;
    ctx.fillStyle = "#ffd166"; // final path color
    ctx.fillRect(c * cellSize, r * cellSize, cellSize, cellSize);
    await sleep(Math.max(10, Math.floor(delay/2)));
  }

  // re-draw start/end to ensure visible
  ctx.fillStyle = "green";
  ctx.fillRect(0, 0, cellSize, cellSize);
  ctx.fillStyle = "red";
  ctx.fillRect((maze[0].length - 1) * cellSize, (maze.length - 1) * cellSize, cellSize, cellSize);
}

generateBtn.onclick = generateMaze;
solveBtn.onclick = solveMaze;
window.addEventListener('resize', () => {
  if (maze && maze.length) {
    adjustCellSizeAndCanvas();
    drawMaze();
  }
});

// initial generate
generateMaze();
