import gradio as gr
from database import fetch_dataframe
from simulation import run_monte_carlo

def get_history(start_yr, end_yr):
    query = "SELECT year, champion, runner_up, score, finals_mvp, total_games FROM series_history WHERE year BETWEEN %s AND %s ORDER BY year DESC"
    return fetch_dataframe(query, (int(start_yr), int(end_yr)))

def predict(t_a, off_a, def_a, t_b, off_b, def_b, sims):
    p_a, p_b = run_monte_carlo(float(off_a), float(def_a), float(off_b), float(def_b), int(sims))
    return f"{t_a}: {p_a:.2f}%", f"{t_b}: {p_b:.2f}%"

demo = gr.Interface(
    fn=get_history,
    inputs=["number", "number"],
    outputs="dataframe",
    title="Series History"
)

sim_demo = gr.Interface(
    fn=predict,
    inputs=["text", "number", "number", "text", "number", "number", "number"],
    outputs=["text", "text"],
    title="Monte Carlo Simulator"
)

app = gr.TabbedInterface([demo, sim_demo], ["History", "Simulator"])

if __name__ == "__main__":
    app.launch(inbrowser=True)