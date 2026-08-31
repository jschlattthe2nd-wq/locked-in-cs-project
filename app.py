import gradio as gr
import pandas as pd
import mysql.connector
import random

def getdbconnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ddxOXmHeEmffQEdePamKSfHvrphOXbyf",
        database="nba_finals_db"
    )

def fetchserieshistory(startyear, endyear):
    conn = getdbconnection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT year AS Year, champion AS Champion, runner_up AS Runner_Up, 
               score AS Score, finals_mvp AS Finals_MVP, total_games AS Total_Games
        FROM series_history 
        WHERE year BETWEEN %s AND %s 
        ORDER BY year DESC
    """
    cursor.execute(query, (int(startyear), int(endyear)))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows)

def fetchallteams():
    conn = getdbconnection()
    cursor = conn.cursor()
    cursor.execute("SELECT team_name FROM team_stats ORDER BY team_name ASC")
    teams = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return teams if teams else ["2017 Golden State Warriors", "2013 Miami Heat"]

def fetchteamratings(teamname):
    conn = getdbconnection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT off_rating, def_rating FROM team_stats WHERE team_name = %s"
    cursor.execute(query, (teamname,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return float(row["off_rating"]), float(row["def_rating"])
    return 110.0, 110.0

def runmontecarlosimulation(teama, teamb, simulations):
    offa, defa = fetchteamratings(teama)
    offb, defb = fetchteamratings(teamb)
    
    neta = offa - defb
    netb = offb - defa
    proba = 1 / (1 + 10 ** ((netb - neta) / 400))
    
    winsa = 0
    winsb = 0
    sims = int(simulations)
    
    for _ in range(sims):
        seriesa = 0
        seriesb = 0
        while seriesa < 4 and seriesb < 4:
            if random.random() < proba:
                seriesa += 1
            else:
                seriesb += 1
        if seriesa == 4:
            winsa += 1
        else:
            winsb += 1
            
    pcta = (winsa / sims) * 100
    pctb = (winsb / sims) * 100
    
    summary = f"{teama} (Off: {offa}, Def: {defa}) vs {teamb} (Off: {offb}, Def: {defb})"
    return summary, f"{pcta:.2f}%", f"{pctb:.2f}%"

teamoptions = fetchallteams()

historytab = gr.Interface(
    fn=fetchserieshistory,
    inputs=[
        gr.Number(label="Start Year", value=2001),
        gr.Number(label="End Year", value=2026)
    ],
    outputs=gr.Dataframe(label="Finals Records"),
    title="NBA Finals Historical Records"
)

simulatortab = gr.Interface(
    fn=runmontecarlosimulation,
    inputs=[
        gr.Dropdown(choices=teamoptions, label="Select Team A", value=teamoptions[0]),
        gr.Dropdown(choices=teamoptions, label="Select Team B", value=teamoptions[1] if len(teamoptions) > 1 else teamoptions[0]),
        gr.Slider(minimum=1000, maximum=50000, step=1000, value=10000, label="Simulation Iterations")
    ],
    outputs=[
        gr.Textbox(label="Ratings Breakdown"),
        gr.Textbox(label="Team A Win Chance"),
        gr.Textbox(label="Team B Win Chance")
    ],
    title="Monte Carlo Matchup Simulator"
)

mainapp = gr.TabbedInterface(
    [historytab, simulatortab], 
    ["Series History", "Matchup Simulator"]
)

if __name__ == "__main__":
    mainapp.launch(inbrowser=True)