# Naming Game – Streamlit App

This Streamlit app demonstrates a simple multi-agent Naming Game.

Agents interact pairwise and choose symbols. If two agents choose the same symbol,
that symbol is reinforced. If they choose different symbols, their probabilities are updated.

The app is designed for teaching concepts such as:

- multi-agent systems
- reinforcement learning
- emergent behavior
- convergence
- stochastic simulations
- social influence and bias

## Features

- Interactive parameter control
- Animated convergence curve
- Final symbol distribution
- Agent probability heatmap
- Agent population visualization
- Initial bias agents
- Student exercises

## Project structure

```text
app.py              # Streamlit interface
naming_game.py      # Simulation logic
plots.py            # Plotting functions
requirements.txt    # Python dependencies
Procfile            # Heroku startup command
README.md           # Project documentation