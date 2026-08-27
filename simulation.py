import random

def run_monte_carlo(off_a, def_a, off_b, def_b, simulations=10000):
    """Simulates a 7-game series between two teams using offensive and defensive ratings."""
    wins_a = 0
    wins_b = 0
    
    # Simple net rating or efficiency-based simulation logic
    net_a = off_a - def_b
    net_b = off_b - def_a
    prob_a = 1 / (1 + 10 ** ((net_b - net_a) / 400)) # Elo-style or rating probability
    
    for _ in range(simulations):
        series_wins_a = 0
        series_wins_b = 0
        while series_wins_a < 4 and series_wins_b < 4:
            if random.random() < prob_a:
                series_wins_a += 1
            else:
                series_wins_b += 1
        if series_wins_a == 4:
            wins_a += 1
        else:
            wins_b += 1
            
    pct_a = (wins_a / simulations) * 100
    pct_b = (wins_b / simulations) * 100
    return pct_a, pct_b