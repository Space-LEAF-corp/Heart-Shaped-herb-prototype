import math
import random

# ---- Parameters ----
ENV = {"thermal": 0.25, "mechanical": 0.25, "chemical": 0.25, "radiation": 0.25}
BASE_FAIL_EDGE = 0.003
BASE_FAIL_NODE = 0.0005
HUB_STRESS_REDUCTION = 0.35
EDGE_PASSIVATION_REDUCTION = 0.5
FLEXIUM_INITIAL = 0.6
FLEXIUM_DECAY = 0.004
RNA_REPAIR_PROB = 0.15
CASCADE_MULTIPLIER = 1.8

def classify_node(key: str) -> str:
    label = key.split("@")[0]
    if label in ("CTCF_TAG", "HISTONE_WRAP", "COHESIN_CLASP"):
        return "ANCHOR"
    if label in ("SMC_RING", "PHASE_HUB", "CHAPERONE"):
        return "HUB"
    if label in ("lncRNA_BRIDGE", "eRNA_NODE"):
        return "RNA"
    if label == "STICKY_NODE":
        return "STICKY"
    if label == "SSB_BOUNDARY":
        return "SSB"
    if label == "FLEXIUM_WRAP":
        return "FLEXIUM"
    return "OTHER"

def effective_env(t_year: int) -> float:
    raw = sum(ENV.values())
    shield = max(0.0, FLEXIUM_INITIAL - FLEXIUM_DECAY * t_year)
    return raw * (1.0 - shield)

def degree(graph, node):
    return len(graph.get(node, set()))

def neighbors(graph, node):
    return graph.get(node, set())

def is_edge_node(node):
    kind = classify_node(node)
    return kind in ("SSB", "STICKY")

def step_year(graph):
    to_remove_edges = []
    to_remove_nodes = set()
    deg = {n: degree(graph, n) for n in graph.keys()}
    env_load = effective_env(step_year.t)

    for n in list(graph.keys()):
        kind = classify_node(n)
        k_mult = 1.0
        if kind == "ANCHOR": k_mult *= 0.6
        if kind == "HUB":    k_mult *= (1.0 - HUB_STRESS_REDUCTION)
        if is_edge_node(n):  k_mult *= (1.0 - EDGE_PASSIVATION_REDUCTION)
        p_node = BASE_FAIL_NODE * env_load * k_mult
        if deg.get(n,0) < 2:
            p_node *= CASCADE_MULTIPLIER
        if random.random() < p_node and classify_node(n) != "FLEXIUM":
            to_remove_nodes.add(n)

    for u in list(graph.keys()):
        for v in list(graph[u]):
            if u > v:
                continue
            stress_mult = 1.0
            if classify_node(u) == "HUB" or classify_node(v) == "HUB":
                stress_mult *= (1.0 - HUB_STRESS_REDUCTION)
            if is_edge_node(u) or is_edge_node(v):
                stress_mult *= (1.0 - EDGE_PASSIVATION_REDUCTION)
            p_edge = BASE_FAIL_EDGE * env_load * stress_mult
            if deg.get(u,0) < 2 or deg.get(v,0) < 2:
                p_edge *= CASCADE_MULTIPLIER
            fail = random.random() < p_edge
            if fail:
                has_rna_neighbor = any(classify_node(x) == "RNA" for x in neighbors(graph, u) | neighbors(graph, v))
                if has_rna_neighbor and random.random() < RNA_REPAIR_PROB:
                    continue
                to_remove_edges.append((u, v))

    for (u, v) in to_remove_edges:
        graph[u].discard(v)
        graph[v].discard(u)
    for n in to_remove_nodes:
        for m in list(graph.get(n, set())):
            graph[m].discard(n)
        graph.pop(n, None)

    step_year.t += 1

step_year.t = 0

def simulate_100_years(graph, cohesion_fn, seed=7):
    random.seed(seed)
    history = []
    for _ in range(100):
        step_year(graph)
        score, stats = cohesion_fn(graph)
        stats["flexium_effectiveness"] = round(max(0.0, FLEXIUM_INITIAL - FLEXIUM_DECAY * step_year.t), 3)
        history.append((score, stats))
    return history
