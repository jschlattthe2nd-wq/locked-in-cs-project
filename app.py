import gradio as gr
import pandas as pd
from database import fetch_dataframe
from simulation import run_monte_carlo

def get_historical_data(start_yr, end_yr):
    query = """
        SELECT year, champion, runner_up, score, finals_mvp, total_games 
        FROM series_history 
        WHERE year BETWEEN %s AND %s 
        ORDER BY year DESC
    """
    return fetch_dataframe(query, (int(start_yr), int(end_yr)))

def predict_matchup(name_a, off_a, def_a, name_b, off_b, def_b, sims):
    p_a, p_b = run_monte_carlo(float(off_a), float(def_a), float(off_b), float(def_b), int(sims))
    return f"{name_a} Win Probability: {p_a:.2f}%", f"{name_b} Win Probability: {p_b:.2f}%"

with gr.Blocks(title="NBA Finals Analytics System") as demo:
    gr.Markdown("# 🏀 NBA Finals Analytics & Statistics System")
    
    with gr.Tabs():
        with gr.Tab("🏆 Series History"):
            with gr.Row():
                start_slider = gr.Slider(2000, 2026, value=2010, step=1, label="Start Year")
                end_slider = gr.Slider(2000, 2026, value=2026, step=1, label="End Year")
            fetch_btn = gr.Button("Fetch Records", variant="primary")
            history_table = gr.Dataframe(label="Finals History Output")
            fetch_btn.click(get_historical_data, inputs=[start_slider, end_slider], outputs=history_table)
            
        with gr.Tab("🎲 Monte Carlo Simulator"):
            with gr.Row():
                with gr.Column():
                    t_a = gr.Textbox(value="2017 Warriors", label="Team A Name")
                    off_a = gr.Number(value=115.6, label="Offensive Rating A")
                    def_a = gr.Number(value=102.5, label="Defensive Rating A")
                with gr.Column():
                    t_b = gr.Textbox(value="2013 Heat", label="Team B Name")
                    off_b = gr.Number(value=112.3, label="Offensive Rating B")
                    def_b = gr.Number(value=103.1, label="Defensive Rating B")
            sims_input = gr.Slider(1000, 50000, value=10000, step=1000, label="Simulation Count")
            sim_btn = gr.Button("Run Simulation", variant="primary")
            with gr.Row():
                res_a = gr.Textbox(label="Result A")
                res_b = gr.Textbox(label="Result B")
            sim_btn.click(predict_matchup, inputs=[t_a, off_a, def_a, t_b, off_b, def_b, sims_input], outputs=[res_a, res_b])

if _name_ == "_main_":
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)