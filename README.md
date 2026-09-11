# The Ranger's Rescue — Entelect Hack<IT> Practice Solution

Dijkstra + waypoint-ordering solver for the practice hackathon.

## Folder Layout

- `level1/` — Small reserve: shortest path A → B (travel time only)
- `level2/` — Great Savannah: A → {S1,S2,S3,S4 in any order} → B (time + risk)
- `level3/` — Generic template for the real hackathon bonus level

## How to Run

```bash
cd level1 && python3 solution.py
cd ../level2 && python3 solution.py
cd ../level3 && python3 solution.py
```

Each `solution.py` prints the route and cost, and writes `answer.json`
next to itself.

## Upload Checklist

- Level 1: upload `level1/answer.json` + a zip of `level1/`
- Level 2: upload `level2/answer.json` + a zip of `level2/`
- Level 3: upload `level3/answer.json` + a zip of `level3/`