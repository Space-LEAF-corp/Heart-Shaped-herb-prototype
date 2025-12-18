from src.simulation import simulate_100_years

def cohesion_fn(graph):
    score = len(graph)
    stats = {"nodes_remaining": score}
    return score, stats

if __name__ == "__main__":
    graph = {
        "CTCF_TAG@1": {"SMC_RING@2", "lncRNA_BRIDGE@3"},
        "SMC_RING@2": {"CTCF_TAG@1", "lncRNA_BRIDGE@3"},
        "lncRNA_BRIDGE@3": {"CTCF_TAG@1", "SMC_RING@2"},
    }

    history = simulate_100_years(graph, cohesion_fn)
    for year, (score, stats) in enumerate(history, 1):
        print(f"Year {year}: score={score}, stats={stats}")
