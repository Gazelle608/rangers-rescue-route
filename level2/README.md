# Level 2 — Great Savannah

## Problem
- Start: A, End: B
- Graph: 18 nodes
- Must visit: S1, S2, S3, S4 (any order)
- Effective edge weight = time + risk

## Run
```bash
python3 solution.py
Expected Output
text
Level 2 order: ['A', 'S3', 'S1', 'S2', 'S4', 'B']
Level 2 route: ['A', 'P1', 'S3', 'P2', 'P3', 'S1', 'P9', 'P8', 'S2', 'P10', 'S4', 'P5', 'B']
Level 2 cost : 60
Optimal
Cost = 60. Optimal stop order: S3 → S1 → S2 → S4 (NOT alphabetical).

Approach
Effective weight = time + risk.

Brute-force all 4! = 24 permutations of stops.

Dijkstra for each leg.

Keep the cheapest concatenated route.

Leg Breakdown
Leg	Path	Cost
A → S3	A → P1 → S3	8
S3 → S1	S3 → P2 → P3 → S1	12
S1 → S2	S1 → P9 → P8 → S2	18
S2 → S4	S2 → P10 → S4	14
S4 → B	S4 → P5 → B	8
Total		60
text

---

## 🧪 Run It in Codespaces

```bash
cd level2
python3 solution.py
cat answer.json
Expected output:

text
Level 2 order: ['A', 'S3', 'S1', 'S2', 'S4', 'B']
Level 2 route: ['A', 'P1', 'S3', 'P2', 'P3', 'S1', 'P9', 'P8', 'S2', 'P10', 'S4', 'P5', 'B']
Level 2 cost : 60
Wrote /workspaces/.../level2/answer.json