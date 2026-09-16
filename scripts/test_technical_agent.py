from investment_agents.agents.technical import TechnicalAgent


agent = TechnicalAgent()

indicators = {
    "roc_5d": 2.3,
    "roc_10d": 4.1,
    "roc_20d": 6.8,
    "roc_1m": 7.2,
    "roc_3m": 12.5,
    "roc_6m": 18.4,
    "roc_12m": 25.7,

    "bollinger_z": 1.2,

    "rsi": 63.5,

    "macd": 0.021,
    "macd_signal": 0.017,
    "macd_hist": 0.004,

    "stochastic_k": 72.0,
    "stochastic_d": 68.0,
    "stochastic_j": 60.0,
}

result = agent.analyze(indicators)

print(result)
print("Score:", result.score)
print("Reason:", result.reason)