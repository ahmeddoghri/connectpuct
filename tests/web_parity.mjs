// The browser agent must be the benchmarked agent. This replays random games
// through both engines and checks the JS search still beats the baselines.
//   node tests/web_parity.mjs    (needs `pip install -e .` for the Python side)
import { createRequire } from "module";
import { execFileSync } from "child_process";
const P = createRequire(import.meta.url)("../web/puct.js");

let seed = 7;
const rand = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;

const games = [];
for (let g = 0; g < 200; g++) {
  let b = P.emptyBoard();
  const moves = [];
  while (!P.winner(b)) {
    const legal = P.legalMoves(b);
    const m = legal[Math.floor(rand() * legal.length)];
    moves.push(m);
    b = P.play(b, m);
  }
  games.push({ moves, w: P.winner(b) });
}
const py = JSON.parse(execFileSync(process.env.PYTHON || "python", ["-c", `
import json, sys
from connectpuct.engine import empty_board
out = []
for g in json.load(sys.stdin):
    b = empty_board()
    for m in g["moves"]:
        b = b.play(m)
    out.append(b.winner())
print(json.dumps(out))`], { input: JSON.stringify(games) }).toString());
const mismatches = games.filter((g, i) => g.w !== py[i]).length;
if (mismatches) throw new Error(`engine disagrees with Python on ${mismatches} of 200 games`);

function match(opponent, n) {
  let wins = 0;
  for (let g = 0; g < n; g++) {
    let b = P.emptyBoard();
    const agent = g % 2 === 0 ? 1 : -1;
    while (!P.winner(b)) {
      const m = b.player === agent ? P.chooseMove(b, { simulations: 40, seed: g * 1000 + b.cells.filter(Boolean).length }).move : opponent(b);
      b = P.play(b, m);
    }
    if (P.winner(b) === agent) wins++;
  }
  return wins;
}
const randomOpp = (b) => { const l = P.legalMoves(b); return l[Math.floor(rand() * l.length)]; };
const centerOpp = (b) => P.legalMoves(b).sort((a, c) => Math.abs(3 - a) - Math.abs(3 - c))[0];
const vsRandom = match(randomOpp, 20);
const vsCenter = match(centerOpp, 20);
console.log(`engine parity: 0/200 mismatches; 40-sim JS agent: ${vsRandom}/20 vs random, ${vsCenter}/20 vs center`);
if (vsRandom < 18 || vsCenter < 17) throw new Error("browser agent is weaker than the benchmarked agent");
