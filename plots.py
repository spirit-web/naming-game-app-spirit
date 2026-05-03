import matplotlib.pyplot as plt
import numpy as np

SYMBOL_COLORS = {
    "A": "tab:blue",
    "B": "tab:orange",
    "C": "tab:green",
    "D": "tab:red",
    "E": "tab:purple",
    "F": "tab:brown",
    "G": "tab:pink",
    "H": "tab:gray",
    "I": "tab:olive",
    "J": "tab:cyan",
}


def plot_top_symbol(history_df):
    fig, ax = plt.subplots(figsize=(8, 4))

    colors = [
        SYMBOL_COLORS.get(symbol, "black")
        for symbol in history_df["top_symbol"]
    ]

    ax.scatter(
        history_df["round"],
        history_df["top_share"],
        c=colors,
        alpha=0.8,
    )

    ax.plot(
        history_df["round"],
        history_df["top_share"],
        alpha=0.3,
    )

    ax.set_title("Ledande symbol över tid")
    ax.set_xlabel("Runda")
    ax.set_ylabel("Andel av senaste val")
    ax.set_ylim(0, 1.05)

    return fig


def plot_final_distribution(final_distribution):
    fig, ax = plt.subplots(figsize=(7, 4))

    colors = [
        SYMBOL_COLORS.get(symbol, "gray")
        for symbol in final_distribution["symbol"]
    ]

    ax.bar(
        final_distribution["symbol"],
        final_distribution["mean_probability"],
        color=colors,
    )

    ax.set_title("Slutlig genomsnittlig symbolpreferens")
    ax.set_xlabel("Symbol")
    ax.set_ylabel("Genomsnittlig sannolikhet")
    ax.set_ylim(0, 1.05)

    return fig


def plot_agent_heatmap(agents_df):
    fig, ax = plt.subplots(figsize=(8, 5))

    im = ax.imshow(agents_df.values, aspect="auto")

    ax.set_title("Agenternas slutliga sannolikheter")
    ax.set_xlabel("Symbol")
    ax.set_ylabel("Agent")

    ax.set_xticks(range(len(agents_df.columns)))
    ax.set_xticklabels(agents_df.columns)

    fig.colorbar(im, ax=ax, label="Sannolikhet")

    return fig




def plot_agent_population(agents_df, biased_agents=None):
    import numpy as np

    fig, ax = plt.subplots(figsize=(7, 6))

    dominant_symbols = agents_df.idxmax(axis=1)
    dominant_probs = agents_df.max(axis=1)

    colors = [
        SYMBOL_COLORS.get(symbol, "black")
        for symbol in dominant_symbols
    ]

    n_agents = len(agents_df)
    grid_size = int(np.ceil(np.sqrt(n_agents)))

    x = [i % grid_size for i in range(n_agents)]
    y = [i // grid_size for i in range(n_agents)]

    sizes = 80 + dominant_probs * 220

    ax.scatter(x, y, c=colors, s=sizes, alpha=0.8)

    for i, symbol in enumerate(dominant_symbols):
        ax.text(
            x[i],
            y[i],
            symbol,
            ha="center",
            va="center",
            fontsize=9,
            color="white",
            weight="bold",
        )

    if biased_agents:
        bx = [x[i] for i in biased_agents]
        by = [y[i] for i in biased_agents]

        ax.scatter(
            bx,
            by,
            facecolors="none",
            edgecolors="black",
            s=[sizes[i] + 80 for i in biased_agents],
            linewidths=1.8,
        )

    ax.set_title("Agentpopulation: färg = symbol, storlek = säkerhet")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()

    return fig