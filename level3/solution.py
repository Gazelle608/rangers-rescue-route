"""
Level 3 (Bonus) — 100 nodes, 24 required stops, time + risk.

Strategy:
  1. Load graph from graph.json (or GRAPH constant).
  2. Precompute all-pairs shortest paths between
     {START, END} ∪ REQUIRED_STOPS using Dijkstra  (26 nodes → 26 Dijkstras).
  3. Solve the visiting order with:
       a. Nearest Neighbour greedy (fast initial tour)
       b. 2-opt local search       (swap two stops)
       c. Or-opt local search      (move a segment of 1-3 stops)
       d. Repeat until no improvement
  4. Expand the chosen order back into full node paths via the cached
     Dijkstra predecessors, concatenate, and write answer.json.

This is a heuristic — for 24 stops, exact Held-Karp is infeasible in Python.
Typical result: within 1-3% of optimal.
"""
import heapq
import itertools
import json
import os
import random
import time

# ---------------------------------------------------------------------------
# CONFIG — swap these when the real problem drops
# ---------------------------------------------------------------------------
START = "A"
END = "B"
REQUIRED_STOPS = [f"S{i}" for i in range(1, 25)]   # 24 stops

# If graph.json exists next to this file, load it. Otherwise use GRAPH below.
_here = os.path.dirname(os.path.abspath(__file__))
GRAPH_PATH = os.path.join(_here, "graph.json")


def load_graph():
    if os.path.exists(GRAPH_PATH):
        with open(GRAPH_PATH) as f:
            return json.load(f)
    raise FileNotFoundError(
        f"No graph.json found at {GRAPH_PATH}. "
        "Paste the adjacency list into graph.json."
    )


# ---------------------------------------------------------------------------
# Effective weight
# ---------------------------------------------------------------------------
def weight_fn(nb):
    """Effective edge weight = time + risk."""
    return nb.get("time", nb.get("weight", 0)) + nb.get("risk", 0)


# ---------------------------------------------------------------------------
# Dijkstra with predecessor tracking (for path reconstruction)
# ---------------------------------------------------------------------------
def dijkstra(graph, start, end, w_fn):
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
            v, w = nb["node"], w_fn(nb)
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if end not in dist:
        return None, float("inf"), prev
    path, cur = [], end
    while cur != start:
        path.append(cur)
        cur = prev[cur]
    path.append(start)
    path.reverse()
    return path, dist[end], prev


# ---------------------------------------------------------------------------
# Precompute distance matrix + path cache between key nodes
# ---------------------------------------------------------------------------
def build_distance_matrix(graph, key_nodes, w_fn):
    """
    Returns:
      D[i][j]  = shortest distance from key_nodes[i] to key_nodes[j]
      P[i][j]  = full node path (list) from key_nodes[i] to key_nodes[j]
    """
    n = len(key_nodes)
    D = [[float("inf")] * n for _ in range(n)]
    P = [[None] * n for _ in range(n)]
    for i, src in enumerate(key_nodes):
        D[i][i] = 0
        P[i][i] = [src]
        for j, dst in enumerate(key_nodes):
            if i == j:
                continue
            path, cost, _ = dijkstra(graph, src, dst, w_fn)
            if path is not None:
                D[i][j] = cost
                P[i][j] = path
    return D, P


# ---------------------------------------------------------------------------
# Tour cost helper (closed tour not required — A ... stops ... B)
# ---------------------------------------------------------------------------
def tour_cost(order, D, start_idx, end_idx):
    """order: list of stop indices (0..n_stops-1)."""
    if not order:
        return D[start_idx][end_idx]
    total = D[start_idx][order[0]]
    for a, b in zip(order, order[1:]):
        total += D[a][b]
    total += D[order[-1]][end_idx]
    return total


# ---------------------------------------------------------------------------
# Nearest Neighbour construction
# ---------------------------------------------------------------------------
def nearest_neighbour(D, start_idx, stop_indices, end_idx):
    unvisited = set(stop_indices)
    order = []
    cur = start_idx
    while unvisited:
        nxt = min(unvisited, key=lambda j: D[cur][j])
        order.append(nxt)
        unvisited.remove(nxt)
        cur = nxt
    return order


# ---------------------------------------------------------------------------
# 2-opt: reverse a segment of the stop order
# ---------------------------------------------------------------------------
def two_opt(order, D, start_idx, end_idx):
    improved = True
    best = order[:]
    best_cost = tour_cost(best, D, start_idx, end_idx)
    n = len(best)
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 1, n):
                cand = best[:i] + best[i:j + 1][::-1] + best[j + 1:]
                c = tour_cost(cand, D, start_idx, end_idx)
                if c + 1e-9 < best_cost:
                    best, best_cost = cand, c
                    improved = True
        # loop again
    return best, best_cost


# ---------------------------------------------------------------------------
# Or-opt: move a segment of length L (1..3) to another position
# ---------------------------------------------------------------------------
def or_opt(order, D, start_idx, end_idx):
    improved = True
    best = order[:]
    best_cost = tour_cost(best, D, start_idx, end_idx)
    n = len(best)
    while improved:
        improved = False
        for L in (1, 2, 3):
            for i in range(0, n - L + 1):
                seg = best[i:i + L]
                rest = best[:i] + best[i + L:]
                for k in range(len(rest) + 1):
                    if k == i:
                        continue
                    cand = rest[:k] + seg + rest[k:]
                    c = tour_cost(cand, D, start_idx, end_idx)
                    if c + 1e-9 < best_cost:
                        best, best_cost = cand, c
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
    return best, best_cost


# ---------------------------------------------------------------------------
# Main solve
# ---------------------------------------------------------------------------
def solve():
    t0 = time.time()
    graph = load_graph()

    # Key nodes: START, END, then all required stops
    key_nodes = [START, END] + REQUIRED_STOPS
    start_idx = 0
    end_idx = 1
    stop_indices = list(range(2, 2 + len(REQUIRED_STOPS)))

    print(f"Building distance matrix over {len(key_nodes)} key nodes...")
    D, P = build_distance_matrix(graph, key_nodes, weight_fn)
    print(f"  done in {time.time() - t0:.1f}s")

    # Quick feasibility check
    unreachable = [
        key_nodes[i] for i in stop_indices
        if D[start_idx][i] == float("inf") or D[i][end_idx] == float("inf")
    ]
    if unreachable:
        print(f"⚠ Unreachable stops: {unreachable}")

    # 1. Nearest Neighbour
    order = nearest_neighbour(D, start_idx, stop_indices, end_idx)
    cost = tour_cost(order, D, start_idx, end_idx)
    print(f"NN initial cost: {cost:.2f}")

    # 2. 2-opt
    order, cost = two_opt(order, D, start_idx, end_idx)
    print(f"After 2-opt:     {cost:.2f}")

    # 3. Or-opt
    order, cost = or_opt(order, D, start_idx, end_idx)
    print(f"After Or-opt:    {cost:.2f}")

    # 4. Try a few random restarts (bounded by time)
    best_order, best_cost = order[:], cost
    deadline = t0 + 300  # 5 min budget
    restarts = 0
    while time.time() < deadline and restarts < 20:
        restarts += 1
        random.shuffle(order)
        order, cost = two_opt(order, D, start_idx, end_idx)
        order, cost = or_opt(order, D, start_idx, end_idx)
        if cost < best_cost:
            best_order, best_cost = order[:], cost
            print(f"Restart {restarts}: improved to {best_cost:.2f}")

    print(f"Best cost: {best_cost:.2f}  (after {restarts} restarts)")

    # Reconstruct full node path
    seq_idx = [start_idx] + best_order + [end_idx]
    full = []
    for a, b in zip(seq_idx, seq_idx[1:]):
        leg = P[a][b]
        if not leg:
            raise RuntimeError(f"No path from {key_nodes[a]} to {key_nodes[b]}")
        full.extend(leg if not full else leg[1:])

    # Save
    out = os.path.join(_here, "answer.json")
    with open(out, "w") as f:
        json.dump({"route": full}, f, indent=2)
    print(f"Wrote {out}  ({len(full)} nodes)")
    print(f"Stop order: {[key_nodes[i] for i in best_order]}")
    return full, best_cost


if __name__ == "__main__":
    solve()