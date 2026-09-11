# Level 1 — The Small Reserve

## Problem
- **Start node:** A
- **End node:** B
- **Graph size:** 6 nodes (A, B, C, D, E, F)
- **Visit stops:** 0 (direct shortest path)
- **Time weighting:** Yes
- **Risk weighting:** No
- Effective edge weight = travel time only

## Run
```bash
python3 solution.py
Expected Output
text
Level 1 route: ['A', 'D', 'E', 'B']
Level 1 cost : 9
Wrote .../level1/answer.json
Optimal
Cost = 9 (matches the stated optimal).

Approach
Build the adjacency list (undirected, travel-time weights only).

Run Dijkstra's algorithm from A to B using a min-heap.

Reconstruct the path by backtracking prev pointers from B to A.

Write the route to answer.json.

Route Breakdown
Leg	Cost
A → D	2
D → E	3
E → B	4
Total	9
Why Not Other Paths?
Route	Cost
A → D → E → B	9 ✅
A → C → D → E → B	12
A → C → E → B	13
A → D → F → E → B	14
A → D → F → B	15
Answer
json
{ "route": ["A", "D", "E", "B"] }