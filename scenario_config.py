SCENARIOS = {
    "religion_prison": {
        "title": "Religionsanpassning i fängelse",
        "subtitle": "En förenklad simulering av hur trosidentitet kan förstärkas eller förändras genom sociala möten i en sluten miljö.",
        "disclaimer": (
            "OBS: Detta är inte en verklig modell för religiös tro eller konvertering. "
            "Här används religion som en förenklad symbol för social identitet, tillhörighet och gruppåverkan."
        ),
        "labels": {
            "num_agents": "Antal fångar",
            "num_symbols": "Antal trosinriktningar",
            "num_rounds": "Antal sociala möten",
            "learning_rate": "Påverkansbarhet / konverteringsbenägenhet",
            "reward": "Social belöning för delad tro",
            "penalty": "Social kostnad vid olik tro",
            "seed": "Startscenario",
            "bias_fraction": "Andel med stark starttro",
            "bias_strength": "Grad av övertygelse från start",
            "preferred_symbol": "Trosinriktning med startfördel",
            "animation_speed": "Animationshastighet",
        },
        "help": {
            "num_agents": "Hur många personer som ingår i miljön. Fler personer gör samordning långsammare.",
            "num_symbols": "Hur många trosinriktningar som kan bli socialt dominerande i modellen.",
            "num_rounds": "Hur många möten som sker mellan två slumpmässigt valda personer.",
            "learning_rate": "Hur snabbt en person ändrar sina sannolikheter efter social respons.",
            "reward": "Hur mycket delad trosinriktning förstärks när två personer matchar.",
            "penalty": "Hur starkt ett möte med olik trosinriktning påverkar individens framtida val.",
            "seed": "Vilket slumpmässigt startscenario som används. Samma startscenario ger samma simulering igen.",
            "bias_fraction": "Hur stor andel som redan från början har en tydligare trosinriktning.",
            "bias_strength": "Hur stark den initiala övertygelsen är hos de personer som börjar med starttro.",
            "preferred_symbol": "Vilken trosinriktning som vissa personer börjar med starkare preferens för.",
            "animation_speed": "Endast hur snabbt visualiseringen spelas upp. Detta påverkar inte själva sociala processen.",
        },
        "symbols": [
            "Kristendom",
            "Islam",
            "Buddhism",
            "Judendom",
            "Taoism",
        ],
        "defaults": {
            "num_agents": 80,
            "num_symbols": 5,
            "num_rounds": 8000,
            "learning_rate": 0.08,
            "reward": 1.0,
            "penalty": 0.8,
            "seed": 1,
            "bias_fraction": 0.25,
            "bias_strength": 0.80,
            "preferred_symbol": "Islam",
            "animation_speed": 0.10,
        },
        "interpretation": """
### Hur du kan tolka simuleringen

- Hög **social belöning för delad tro** gör att en gemensam trosidentitet snabbare kan förstärkas.
- Hög **social kostnad vid olik tro** gör att avvikelse blir dyrare och att konvergens kan gå snabbare.
- Hög **andel med stark starttro** ger en trosinriktning historisk startfördel.
- Hög **grad av övertygelse från start** gör att den initiala preferensen blir svårare att rubba.
- Hög **påverkansbarhet** gör att individer ändrar sig snabbare efter möten.

Viktig begränsning: verklig religiös identitet formas också av biografi, trauma, teologi, relationer, etnicitet, makt, skyddsbehov, institutionella regler och personlig övertygelse. Den här modellen visar bara en förenklad social förstärkningsprocess.
"""
    }
}