import random
from collections import Counter
import pandas as pd


def initialize_agents(
    n_agents,
    symbols,
    biased_fraction=0.0,
    biased_symbol=None,
    bias_strength=0.8,
    seed=7,
):
    rng = random.Random(seed)
    symbols = list(symbols)

    n_biased = int(n_agents * biased_fraction)
    biased_agents = set(rng.sample(range(n_agents), n_biased))

    agents = []

    for i in range(n_agents):
        if i in biased_agents and biased_symbol is not None:
            remaining_prob = (1.0 - bias_strength) / (len(symbols) - 1)

            probs = {
                s: bias_strength if s == biased_symbol else remaining_prob
                for s in symbols
            }
        else:
            probs = {s: 1.0 / len(symbols) for s in symbols}

        agents.append(probs)

    return agents, biased_agents


def sample_symbol(probabilities, rng):
    r = rng.random()
    acc = 0.0

    for symbol, prob in probabilities.items():
        acc += prob
        if r <= acc:
            return symbol

    return list(probabilities.keys())[-1]


def normalize(probabilities):
    total = sum(max(v, 1e-12) for v in probabilities.values())

    for key in probabilities:
        probabilities[key] = max(probabilities[key], 1e-12) / total


def run_naming_game(
    n_agents=50,
    symbols=("A", "B", "C", "D", "E"),
    rounds=8000,
    reward=1.0,
    penalty=1.0,
    learning_rate=0.12,
    seed=7,
    log_points=200,
    biased_fraction=0.0,
    biased_symbol=None,
    bias_strength=0.8,
):
    rng = random.Random(seed)
    symbols = list(symbols)

    agents, biased_agents = initialize_agents(
        n_agents=n_agents,
        symbols=symbols,
        biased_fraction=biased_fraction,
        biased_symbol=biased_symbol,
        bias_strength=bias_strength,
        seed=seed,
    )

    log_every = max(1, rounds // log_points)
    window = []

    history = []

    for t in range(1, rounds + 1):
        i, j = rng.sample(range(n_agents), 2)

        si = sample_symbol(agents[i], rng)
        sj = sample_symbol(agents[j], rng)

        window.extend([si, sj])

        if si == sj:
            agents[i][si] += learning_rate * reward
            agents[j][sj] += learning_rate * reward
        else:
            agents[i][si] -= learning_rate * penalty
            agents[j][sj] -= learning_rate * penalty

            agents[i][sj] += learning_rate * reward
            agents[j][si] += learning_rate * reward

        normalize(agents[i])
        normalize(agents[j])

        if t % log_every == 0 or t == 1:
            counts = Counter(window)
            top_symbol, top_count = counts.most_common(1)[0]
            top_share = top_count / len(window)

            row = {
                "round": t,
                "top_symbol": top_symbol,
                "top_share": top_share,
            }

            for symbol in symbols:
                row[f"share_{symbol}"] = counts[symbol] / len(window)

            history.append(row)
            window = []

    history_df = pd.DataFrame(history)
    agents_df = pd.DataFrame(agents)

    final_distribution = agents_df.mean().reset_index()
    final_distribution.columns = ["symbol", "mean_probability"]

    return history_df, agents_df, final_distribution, biased_agents