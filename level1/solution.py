"""
Level 1 — The Small Reserve
Shortest path from A to B using Dijkstra's algorithm.
Effective weight = travel time only.
"""
import heapq
import json
import os

GRAPH = {
    "A": [{"node": "C", "weight": 4}, {"node": "D", "weight": 2}],
    "B": [{"node": "E", "weight": 4}, {"node": "F", "weight": 7}],
    "C": [{"node": "A", "weight": 4}, {"node": "D", "weight": 1}, {"node": "E", "weight": 5}],
    "D": [{"node": "A", "weight": 2}, {"node": "C", "weight": 1}, {"node": "E", "weight": 3}, {"node": "F", "weight": 6}],
    "E": [{"node": "C", "weight": 5}, {"node": "D", "weight": 3}, {"node": "F", "weight": 2}, {"node": "B", "weight": 4}],
    "F": [{"node": "D", "weight": 6}, {"node": "E", "weight": 2}, {"node": "B", "weight": 7}],
}
START, END = "A", "B"


def dijkstra(graph, start, end, weight_fn=lambda nb: nb["weight"]):
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


if __name__ == "__main__":
    route, cost = dijkstra(GRAPH, START, END)
    print(f"Level 1 route: {route}")
    print(f"Level 1 cost : {cost}")
    out = os.path.join(os.path.dirname(__file__), "answer.json")
    with open(out, "w") as f:
        json.dump({"route": route}, f, indent=2)
    print(f"Wrote {out}")