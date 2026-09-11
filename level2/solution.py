"""
Level 2 — The Great Savannah
Start: A | End: B | 18 nodes | Visit S1, S2, S3, S4 (any order)
Effective edge weight = time + risk
Brute-force all 4! = 24 orderings, Dijkstra for each leg.
"""
import heapq
import itertools
import json
import os

GRAPH = {
    "A":  [{"node": "P1",  "time": 4, "risk": 0}, {"node": "P6",  "time": 5, "risk": 2}],
    "B":  [{"node": "P5",  "time": 4, "risk": 0}, {"node": "P12", "time": 4, "risk": 0}],
    "S1": [{"node": "P3",  "time": 4, "risk": 0}, {"node": "P4",  "time": 4, "risk": 1}, {"node": "P9",  "time": 5, "risk": 1}],
    "S2": [{"node": "P7",  "time": 4, "risk": 0}, {"node": "P8",  "time": 5, "risk": 1}, {"node": "P10", "time": 5, "risk": 2}],
    "S3": [{"node": "P1",  "time": 4, "risk": 0}, {"node": "P2",  "time": 4, "risk": 1}],
    "S4": [{"node": "P4",  "time": 5, "risk": 0}, {"node": "P5",  "time": 4, "risk": 0}, {"node": "P10", "time": 7, "risk": 0}],
    "P1": [{"node": "A",   "time": 4, "risk": 0}, {"node": "S3",  "time": 4, "risk": 0}],
    "P2": [{"node": "S3",  "time": 4, "risk": 1}, {"node": "P3",  "time": 3, "risk": 0}],
    "P3": [{"node": "P2",  "time": 3, "risk": 0}, {"node": "S1",  "time": 4, "risk": 0}],
    "P4": [{"node": "S1",  "time": 4, "risk": 1}, {"node": "S4",  "time": 5, "risk": 0}],
    "P5": [{"node": "S4",  "time": 4, "risk": 0}, {"node": "B",   "time": 4, "risk": 0}],
    "P6": [{"node": "A",   "time": 5, "risk": 2}, {"node": "P7",  "time": 4, "risk": 0}],
    "P7": [{"node": "P6",  "time": 4, "risk": 0}, {"node": "S2",  "time": 4, "risk": 0}, {"node": "P11", "time": 4, "risk": 2}],
    "P8": [{"node": "S2",  "time": 5, "risk": 1}, {"node": "P9",  "time": 4, "risk": 2}],
    "P9": [{"node": "P8",  "time": 4, "risk": 2}, {"node": "S1",  "time": 5, "risk": 1}],
    "P10":[{"node": "S2",  "time": 5, "risk": 2}, {"node": "S4",  "time": 7, "risk": 0}],
    "P11":[{"node": "P7",  "time": 4, "risk": 2}, {"node": "P12", "time": 5, "risk": 1}],
    "P12":[{"node": "P11", "time": 5, "risk": 1}, {"node": "B",   "time": 4, "risk": 0}],
}
START, END = "A", "B"
STOPS = ["S1", "S2", "S3", "S4"]


def dijkstra(graph, start, end, weight_fn):
    """Standard Dijkstra. Returns (path, cost)."""
    dist = {start: 0}
    prev = {}
    pq = [(0, start)]
    visited = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == end:
            break
        for nb in graph.get(u, []):
            v, w = nb["node"], weight_fn(nb)
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    path, cur = [], end
    while cur != start:
        path.append(cur)
        cur = prev[cur]
    path.append(start)
    path.reverse()
    return path, dist[end]


def effective(nb):
    """Effective edge weight = time + risk."""
    return nb["time"] + nb["risk"]


def solve():
    """Try all 4! = 24 station orderings, keep the cheapest."""
    best_cost, best_legs, best_order = float("inf"), None, None
    for perm in itertools.permutations(STOPS):
        seq = [START, *perm, END]
        total, legs, ok = 0, [], True
        for i in range(len(seq) - 1):
            path, cost = dijkstra(GRAPH, seq[i], seq[i + 1], effective)
            if cost == float("inf"):
                ok = False
                break
            total += cost
            legs.append(path)
        if ok and total < best_cost:
            best_cost, best_legs, best_order = total, legs, seq
    # Concatenate legs (drop duplicated joint nodes)
    full = []
    for leg in best_legs:
        full.extend(leg if not full else leg[1:])
    return full, best_cost, best_order


if __name__ == "__main__":
    route, cost, order = solve()
    print(f"Level 2 order: {order}")
    print(f"Level 2 route: {route}")
    print(f"Level 2 cost : {cost}")
    out = os.path.join(os.path.dirname(__file__), "answer.json")
    with open(out, "w") as f:
        json.dump({"route": route}, f, indent=2)
    print(f"Wrote {out}")