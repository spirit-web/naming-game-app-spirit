import streamlit as st

from naming_game import run_naming_game
from plots import (
    plot_top_symbol,
    plot_final_distribution,
    plot_agent_heatmap,
    plot_agent_population,
)


def run_scenario(config: dict):
    st.set_page_config(page_title=config["title"], layout="wide")

    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] label {
            font-size: 1.10rem !important;
            font-weight: 650 !important;
        }

        section[data-testid="stSidebar"] p {
            font-size: 1rem !important;
        }

        section[data-testid="stSidebar"] .stMarkdown {
            font-size: 1rem !important;
        }

        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            font-size: 1.30rem !important;
            font-weight: 800 !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] {
            font-size: 1rem !important;
        }

        section[data-testid="stSidebar"] input {
            font-size: 1rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title(config["title"])
    st.write(config["subtitle"])

    if config.get("disclaimer"):
        st.warning(config["disclaimer"])

    labels = config["labels"]
    help_text = config["help"]
    defaults = config["defaults"]
    symbols = config["symbols"]

    st.sidebar.header("Simuleringsinställningar")

    num_agents = st.sidebar.slider(
        labels["num_agents"],
        min_value=10,
        max_value=500,
        value=defaults["num_agents"],
        step=10,
        help=help_text["num_agents"],
    )

    num_symbols = st.sidebar.slider(
        labels["num_symbols"],
        min_value=2,
        max_value=len(symbols),
        value=defaults["num_symbols"],
        step=1,
        help=help_text["num_symbols"],
    )

    active_symbols = symbols[:num_symbols]

    num_rounds = st.sidebar.slider(
        labels["num_rounds"],
        min_value=500,
        max_value=50000,
        value=defaults["num_rounds"],
        step=500,
        help=help_text["num_rounds"],
    )

    learning_rate = st.sidebar.slider(
        labels["learning_rate"],
        min_value=0.01,
        max_value=0.50,
        value=defaults["learning_rate"],
        step=0.01,
        help=help_text["learning_rate"],
    )

    reward = st.sidebar.slider(
        labels["reward"],
        min_value=0.00,
        max_value=3.00,
        value=defaults["reward"],
        step=0.10,
        help=help_text["reward"],
    )

    penalty = st.sidebar.slider(
        labels["penalty"],
        min_value=0.00,
        max_value=3.00,
        value=defaults["penalty"],
        step=0.10,
        help=help_text["penalty"],
    )

    seed = st.sidebar.slider(
        labels["seed"],
        min_value=1,
        max_value=10,
        value=defaults["seed"],
        step=1,
        help=help_text["seed"],
    )

    st.sidebar.header("Startbias / initial preferens")

    bias_fraction = st.sidebar.slider(
        labels["bias_fraction"],
        min_value=0.00,
        max_value=0.80,
        value=defaults["bias_fraction"],
        step=0.05,
        help=help_text["bias_fraction"],
    )

    bias_strength = st.sidebar.slider(
        labels["bias_strength"],
        min_value=0.50,
        max_value=0.99,
        value=defaults["bias_strength"],
        step=0.01,
        help=help_text["bias_strength"],
    )

    default_preferred_symbol = defaults["preferred_symbol"]

    preferred_symbol = st.sidebar.selectbox(
        labels["preferred_symbol"],
        options=active_symbols,
        index=active_symbols.index(default_preferred_symbol)
        if default_preferred_symbol in active_symbols
        else 0,
        help=help_text["preferred_symbol"],
    )

    animation_speed = st.sidebar.slider(
        labels["animation_speed"],
        min_value=0.05,
        max_value=0.50,
        value=defaults["animation_speed"],
        step=0.05,
        help=help_text["animation_speed"],
    )

    st.subheader("Valda alternativ i denna simulering")
    st.write(", ".join(active_symbols))

    with st.expander("Hur ska scenariot tolkas?"):
        st.markdown(config["interpretation"])

    if st.button("Kör simulering"):
        history_df, agents_df, final_distribution, biased_agents = run_naming_game(
            n_agents=num_agents,
            symbols=active_symbols,
            rounds=num_rounds,
            reward=reward,
            penalty=penalty,
            learning_rate=learning_rate,
            seed=seed,
            biased_fraction=bias_fraction,
            biased_symbol=preferred_symbol,
            bias_strength=bias_strength,
        )

        st.success("Simuleringen är klar.")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Ledande alternativ över tid")
            fig1 = plot_top_symbol(history_df)
            st.pyplot(fig1)

        with col2:
            st.subheader("Slutlig genomsnittlig preferens")
            fig2 = plot_final_distribution(final_distribution)
            st.pyplot(fig2)

        st.subheader("Agenternas slutliga sannolikheter")
        fig3 = plot_agent_heatmap(agents_df)
        st.pyplot(fig3)

        st.subheader("Agentpopulation")
        fig4 = plot_agent_population(agents_df, biased_agents)
        st.pyplot(fig4)

        st.caption(
            f"Animationshastighet är satt till {animation_speed}, men i denna första scenario-mall "
            "påverkar den bara hur vi tänker kring visualisering, inte själva simuleringen."
        )