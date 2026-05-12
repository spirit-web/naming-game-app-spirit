import streamlit as st
import time
import gc
import matplotlib.pyplot as plt

from naming_game import run_naming_game
from plots import (
    plot_top_symbol,
    plot_final_distribution,
    plot_agent_heatmap,
    plot_agent_population,
)

DEFAULTS = {
    "n_agents": 50,
    "n_symbols": 5,
    "rounds": 8000,
    "learning_rate": 0.12,
    "reward": 1.0,
    "penalty": 1.0,
    "seed": 7,
    "biased_fraction": 0.1,
    "bias_strength": 0.8,
}

st.set_page_config(
    page_title="Naming Game",
    layout="wide",
)



st.title("Naming Game – emergent kommunikation mellan agenter")

st.markdown(
    """
I denna app simulerar vi hur enkla agenter kan utveckla en gemensam symbol
genom upprepade interaktioner, belöning och straff.
"""
)

with st.expander("Vad visar denna app?"):
    st.markdown(
        """
        Denna app simulerar ett enkelt **Naming Game**.

        Agenter möts slumpmässigt två och två. Varje agent väljer en symbol.
        Om båda väljer samma symbol får de belöning. Om de väljer olika symboler
        justeras deras sannolikheter.

        Med tiden kan en gemensam symbol växa fram i populationen, trots att ingen
        agent har kontroll över hela systemet.

        Det viktiga att observera är:

        - hur snabbt systemet når en gemensam konvention
        - om en symbol blir dominant
        - hur learning rate påverkar stabilitet
        - hur initial bias hos vissa agenter kan påverka hela gruppen
        """
    )

# Init state
if "show_tasks" not in st.session_state:
    st.session_state.show_tasks = False

# Toggle knapp
if st.button("📘 Visa / Dölj övningar"):
    st.session_state.show_tasks = not st.session_state.show_tasks



if st.session_state.show_tasks:
    st.markdown("## 🧪 Övningar att testa i appen")

    st.markdown("""
### 1. 🔍 Få systemet att konvergera
- Sätt antal symboler till 3–4  
- Öka learning rate (t.ex. 0.2–0.3)  
- Öka antal rundor  

👉 Fråga: Hur snabbt når systemet en gemensam symbol?

---

### 2. ⚖️ Skapa ett system som INTE konvergerar
- Använd många symboler (8–10)  
- Sänk learning rate (t.ex. 0.05)  

👉 Fråga: Vad händer med kurvan? Varför stabiliseras den inte?

---

### 3. 🧠 Testa bias-agenter
- Sätt 10–20% bias-agenter  
- Välj symbol A  
- Kör simuleringen  

👉 Fråga: Vinner A alltid? Om inte – varför?

---

### 4. 🔥 Tipping point
- Öka andel bias-agenter till 30–50%  

👉 Fråga: När börjar bias påverka hela populationen?

---

### 5. ⚡ Reward vs penalty
- Testa hög reward / låg penalty  
- Testa låg reward / hög penalty  

👉 Fråga: Vilken effekt har det på lärandet?

---

### 6. 🎯 Samma seed vs olika seed
- Kör med samma seed flera gånger  
- Ändra seed  

👉 Fråga: Hur mycket påverkar slumpen resultatet?

---

### 7. 👀 Titta på populationen
- Studera färger och storlek på agenter  

👉 Fråga:
- Finns det grupper?
- Hur snabbt försvinner variation?

---

### 💡 Extra utmaning
Kan du hitta inställningar där:
- systemet ALDRIG konvergerar?
- en svag minoritet ändå vinner?

---
""")


if "initialized" not in st.session_state:
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    st.session_state.initialized = True


if st.sidebar.button("Återställ standardvärden"):
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    st.rerun()


st.sidebar.header("Simuleringsinställningar")

n_agents = st.sidebar.slider(
    "Antal agenter",
    10, 300,
    key="n_agents",
    help="Hur många agenter som deltar i spelet. Fler agenter gör populationen större och kan göra konvergens långsammare."
)

n_symbols = st.sidebar.slider(
    "Antal symboler",
    2, 10,
    key="n_symbols",
    help="Hur många möjliga symboler agenterna kan välja mellan. Fler symboler gör spelet svårare."
)

rounds = st.sidebar.slider(
    "Antal rundor",
    500, 50000,
    step=500,
    key="rounds",
    help="Hur många interaktioner som sker mellan agenterna."
)

learning_rate = st.sidebar.slider(
    "Learning rate",
    0.01, 0.5,
    step=0.01,
    key="learning_rate",
    help="Hur snabbt agenterna ändrar sina sannolikheter efter belöning eller straff."
)

reward = st.sidebar.slider(
    "Reward",
    0.0, 3.0,
    step=0.1,
    key="reward",
    help=(
        "Hur mycket en agent förstärker sannolikheten att välja en symbol "
        "som fungerade (båda valde samma symbol). "
        "Detta ökar chansen att agenten väljer samma symbol i framtiden."
    )
)

penalty = st.sidebar.slider(
    "Penalty",
    0.0, 3.0,
    step=0.1,
    key="penalty",
    help=(
        "Hur mycket en agent minskar sannolikheten att välja en symbol "
        "som inte fungerade (agenter valde olika symboler). "
        "Samtidigt ökar sannolikheten för den andra agentens symbol."
    )
)    

seed = st.sidebar.number_input(
    "Seed",
    step=1,
    key="seed",
    help="Startvärde för slumpgeneratorn. Samma seed ger samma simulering."
)
st.sidebar.header("Bias / fixerad preferens")

symbols = tuple(chr(65 + i) for i in range(n_symbols))

biased_fraction = st.sidebar.slider(
    "Andel agenter med initial preferens",
    0.0, 0.8,
    step=0.05,
    key="biased_fraction",
    help="Andel agenter som börjar med starkare preferens för en viss symbol."
)

bias_strength = st.sidebar.slider(
    "Styrka på initial preferens",
    0.5, 0.99,
    step=0.01,
    key="bias_strength",
    help="Hur stark den initiala preferensen är. 0.8 betyder att agenten börjar med 80 % sannolikhet för vald symbol."
)

biased_symbol = st.sidebar.selectbox(
    "Symbol som vissa agenter föredrar",
    symbols,
)


run_button = st.button("Kör simulering")


st.sidebar.header("Visualisering")

animate_plot = st.sidebar.checkbox(
    "Animera kurvan",
    value=False,
    help="Visar hur den ledande symbolen växer fram steg för steg."
)

animation_speed = st.sidebar.slider(
    "Animationshastighet",
    0.01,
    0.30,
    0.12,
    step=0.01,
    help="Paus i sekunder mellan varje steg. Lägre värde ger snabbare animation."
)  

if run_button:
    history_df, agents_df, final_distribution, biased_agents = run_naming_game(
        n_agents=n_agents,
        symbols=symbols,
        rounds=rounds,
        reward=reward,
        penalty=penalty,
        learning_rate=learning_rate,
        seed=seed,
        biased_fraction=biased_fraction,
        biased_symbol=biased_symbol,
        bias_strength=bias_strength,
        log_points=60,
    )

    

    final_winner = final_distribution.sort_values(
        "mean_probability",
        ascending=False,
    ).iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Vinnande symbol", final_winner["symbol"])
    col2.metric("Vinnarens medelsannolikhet", f"{final_winner['mean_probability']:.2f}")
    col3.metric("Bias-agenter", len(biased_agents))

    st.subheader("Ledande symbol under simuleringen")

    if animate_plot:
        plot_placeholder = st.empty()

        for i in range(2, len(history_df) + 1):
            partial_history = history_df.iloc[:i]
            fig = plot_top_symbol(partial_history)

            plot_placeholder.pyplot(fig)
            plt.close(fig)

            gc.collect()
            time.sleep(animation_speed)
    else:
        fig = plot_top_symbol(history_df)
        st.pyplot(fig)
        plt.close(fig)
        gc.collect()


    st.info(
    "Visar hur stor andel av agenterna som använde den mest populära symbolen över tid. "
    "Om kurvan går mot 1 → systemet konvergerar."
    )    

    st.subheader("Slutlig symbolfördelning")

    fig = plot_final_distribution(final_distribution)
    st.pyplot(fig)
    plt.close(fig)
    gc.collect()

    st.info(
    "Visar den genomsnittliga sannolikheten för varje symbol i populationen. "
    "En tydlig topp betyder att en symbol dominerar."
    )

    st.subheader("Agenternas slutliga preferenser")

    fig = plot_agent_heatmap(agents_df)
    st.pyplot(fig)
    plt.close(fig)
    gc.collect()

    st.info(
    "Varje rad är en agent och varje kolumn en symbol. "
    "Ljusa färger betyder hög sannolikhet. "
    "En tydlig kolumn visar global konvergens."
    )

    st.subheader("Agentpopulation")

    fig = plot_agent_population(agents_df, biased_agents)
    st.pyplot(fig)
    plt.close(fig)
    gc.collect()

    st.info(
    "Varje punkt är en agent. "
    "Färg = vilken symbol agenten föredrar. "
    "Storlek = hur säker agenten är. "
    "Svart ring = agent med initial bias."
    )

    with st.expander("Visa rådata"):
        st.write("Historik")
        st.dataframe(history_df)

        st.write("Slutliga agentpreferenser")
        st.dataframe(agents_df)

      

else:
    st.info("Välj parametrar i sidopanelen och klicka på 'Kör simulering'.")