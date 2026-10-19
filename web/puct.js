(function (root) {
// A line-for-line port of connectpuct/engine.py and connectpuct/mcts.py, so the
// agent you play in the browser is the agent the benchmark measures.
// Board: cells[r * 7 + c], row 0 at the top; 1 and -1 are the players.

const ROWS = 6;
const COLS = 7;

const WIN_LINES = [];
for (let r = 0; r < ROWS; r++) {
  for (let c = 0; c < COLS; c++) {
    if (c <= COLS - 4) WIN_LINES.push([0, 1, 2, 3].map((i) => r * COLS + c + i));
    if (r <= ROWS - 4) WIN_LINES.push([0, 1, 2, 3].map((i) => (r + i) * COLS + c));
    if (r <= ROWS - 4 && c <= COLS - 4) WIN_LINES.push([0, 1, 2, 3].map((i) => (r + i) * COLS + c + i));
    if (r >= 3 && c <= COLS - 4) WIN_LINES.push([0, 1, 2, 3].map((i) => (r - i) * COLS + c + i));
  }
}

function emptyBoard() {
  return { cells: new Array(ROWS * COLS).fill(0), player: 1 };
}

function legalMoves(b) {
  const out = [];
  for (let c = 0; c < COLS; c++) if (b.cells[c] === 0) out.push(c);
  return out;
}

function play(b, col) {
  const cells = b.cells.slice();
  for (let row = ROWS - 1; row >= 0; row--) {
    const idx = row * COLS + col;
    if (cells[idx] === 0) {
      cells[idx] = b.player;
      return { cells, player: -b.player };
    }
  }
  throw new Error(`illegal move: ${col}`);
}

// 1 or -1 for a win, 2 for a draw, 0 while the game is still going.
function winner(b) {
  for (const line of WIN_LINES) {
    const v = b.cells[line[0]];
    if (v !== 0 && b.cells[line[1]] === v && b.cells[line[2]] === v && b.cells[line[3]] === v) return v;
  }
  return legalMoves(b).length ? 0 : 2;
}

function winningLine(b) {
  for (const line of WIN_LINES) {
    const v = b.cells[line[0]];
    if (v !== 0 && line.every((i) => b.cells[i] === v)) return line;
  }
  return null;
}

// Python's random.Random is not reproducible in JS; mulberry32 keeps the
// search deterministic per seed, which is what matters for debugging.
function rng32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function winningMove(b, player) {
  for (const move of legalMoves(b)) {
    if (winner(play(b, move)) === player) return move;
  }
  return null;
}

function priors(b) {
  const weights = new Map();
  let total = 0;
  for (const move of legalMoves(b)) {
    let w = 1.0 + (3 - Math.abs(3 - move)) * 0.45;
    const nxt = play(b, move);
    if (winner(nxt) === b.player) w += 8.0;
    if (winningMove(nxt, nxt.player) !== null) w -= 0.6;
    w = Math.max(0.05, w);
    weights.set(move, w);
    total += w;
  }
  for (const [m, w] of weights) weights.set(m, w / total);
  return weights;
}

function rollout(b, rand) {
  const rootPlayer = b.player;
  let state = b;
  for (let i = 0; i < 42; i++) {
    const win = winner(state);
    if (win === rootPlayer) return 1.0;
    if (win === -rootPlayer) return -1.0;
    if (win === 2) return 0.0;
    let move = winningMove(state, state.player);
    if (move === null) {
      const block = winningMove({ cells: state.cells, player: -state.player }, -state.player);
      const legal = legalMoves(state);
      move = block !== null && legal.includes(block) ? block : legal[Math.floor(rand() * legal.length)];
    }
    state = play(state, move);
  }
  return 0.0;
}

function node(board, prior) {
  return { board, prior, visits: 0, valueSum: 0, children: null };
}

const value = (n) => (n.visits === 0 ? 0 : n.valueSum / n.visits);

function simulate(n, rand, cPuct) {
  const win = winner(n.board);
  if (win) {
    const v = win === 2 ? 0 : win === n.board.player ? 1 : -1;
    n.visits += 1;
    n.valueSum += v;
    return v;
  }
  if (!n.children) {
    n.children = new Map();
    for (const [move, prior] of priors(n.board)) n.children.set(move, node(play(n.board, move), prior));
    const v = rollout(n.board, rand);
    n.visits += 1;
    n.valueSum += v;
    return v;
  }
  let best = null;
  let bestScore = -Infinity;
  const parentSqrt = Math.sqrt(Math.max(1, n.visits));
  for (const [move, child] of n.children) {
    const score = -value(child) + (cPuct * child.prior * parentSqrt) / (1 + child.visits);
    if (score > bestScore) {
      best = move;
      bestScore = score;
    }
  }
  const v = -simulate(n.children.get(best), rand, cPuct);
  n.visits += 1;
  n.valueSum += v;
  return v;
}

// Returns the move plus what the search saw, so the page can show its work.
function chooseMove(b, { simulations = 80, seed = 0, cPuct = 1.4 } = {}) {
  const immediate = winningMove(b, b.player);
  if (immediate !== null) return { move: immediate, reason: "win", visits: null, value: 1 };
  const block = winningMove({ cells: b.cells, player: -b.player }, -b.player);
  if (block !== null && legalMoves(b).includes(block)) return { move: block, reason: "block", visits: null, value: null };
  const rand = rng32(seed);
  const root = node(b, 1.0);
  for (let i = 0; i < simulations; i++) simulate(root, rand, cPuct);
  if (!root.children) return { move: legalMoves(b)[0], reason: "only", visits: null, value: null };
  let move = null;
  let most = -1;
  const visits = new Array(COLS).fill(0);
  for (const [m, child] of root.children) {
    visits[m] = child.visits;
    if (child.visits > most) {
      most = child.visits;
      move = m;
    }
  }
  // The chosen child's value is from the opponent's side, so flip it.
  return { move, reason: "search", visits, value: -value(root.children.get(move)) };
}

const api = { ROWS, COLS, emptyBoard, legalMoves, play, winner, winningLine, chooseMove };
if (typeof module !== "undefined" && module.exports) module.exports = api;
else root.PUCT = api;
})(this);
