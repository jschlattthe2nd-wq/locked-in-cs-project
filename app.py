import gradio as gr
import pandas as pd
import mysql.connector
import random
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Database Connection Parameters
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "Ajoshjohn2021"
DB_NAME = "nba_finals_db"

def initdatabase():
    """Initializes the database, creates tables, and seeds default records."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
        conn.close()

        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # 1. Create team_stats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS team_stats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                team_name VARCHAR(100) NOT NULL UNIQUE,
                off_rating DECIMAL(5,2) NOT NULL,
                def_rating DECIMAL(5,2) NOT NULL
            )
        """)

        # 2. Create series_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS series_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                year INT NOT NULL UNIQUE,
                champion VARCHAR(100) NOT NULL,
                runner_up VARCHAR(100) NOT NULL,
                score VARCHAR(10) NOT NULL,
                finals_mvp VARCHAR(100) NOT NULL,
                total_games INT NOT NULL
            )
        """)

        # 3. Create simulation_logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS simulation_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                simulated_at DATETIME NOT NULL,
                team_a VARCHAR(100) NOT NULL,
                team_b VARCHAR(100) NOT NULL,
                iterations INT NOT NULL,
                team_a_win_pct DECIMAL(5,2) NOT NULL,
                team_b_win_pct DECIMAL(5,2) NOT NULL
            )
        """)

        # Seed team_stats if empty
        cursor.execute("SELECT COUNT(*) FROM team_stats")
        if cursor.fetchone()[0] == 0:
            team_data = [
                ('2001 Los Angeles Lakers', 108.4, 104.8), ('2001 Philadelphia 76ers', 101.8, 98.9),
                ('2002 Los Angeles Lakers', 109.4, 101.7), ('2002 New Jersey Nets', 101.1, 99.5),
                ('2003 San Antonio Spurs', 105.6, 99.7), ('2003 New Jersey Nets', 100.0, 96.0),
                ('2004 Detroit Pistons', 102.0, 95.4), ('2004 Los Angeles Lakers', 105.5, 103.2),
                ('2005 San Antonio Spurs', 107.5, 98.8), ('2005 Detroit Pistons', 103.9, 98.1),
                ('2006 Miami Heat', 108.7, 104.3), ('2006 Dallas Mavericks', 111.8, 105.0),
                ('2007 San Antonio Spurs', 109.2, 99.9), ('2007 Cleveland Cavaliers', 103.8, 101.3),
                ('2008 Boston Celtics', 110.2, 98.9), ('2008 Los Angeles Lakers', 113.0, 105.5),
                ('2009 Los Angeles Lakers', 112.8, 104.7), ('2009 Orlando Magic', 108.6, 101.9),
                ('2010 Los Angeles Lakers', 108.8, 103.7), ('2010 Boston Celtics', 107.7, 103.8),
                ('2011 Dallas Mavericks', 109.7, 105.0), ('2011 Miami Heat', 111.7, 103.5),
                ('2012 Miami Heat', 108.5, 100.2), ('2012 Oklahoma City Thunder', 109.8, 103.2),
                ('2013 Miami Heat', 112.3, 103.1), ('2013 San Antonio Spurs', 108.1, 101.6),
                ('2014 San Antonio Spurs', 110.5, 102.4), ('2014 Miami Heat', 109.0, 105.8),
                ('2015 Golden State Warriors', 111.6, 101.4), ('2015 Cleveland Cavaliers', 109.8, 106.3),
                ('2016 Cleveland Cavaliers', 110.9, 104.2), ('2016 Golden State Warriors', 114.5, 103.8),
                ('2017 Golden State Warriors', 115.6, 102.5), ('2017 Cleveland Cavaliers', 113.6, 108.0),
                ('2018 Golden State Warriors', 113.6, 107.7), ('2018 Cleveland Cavaliers', 111.1, 110.6),
                ('2019 Toronto Raptors', 113.1, 107.1), ('2019 Golden State Warriors', 115.9, 109.0),
                ('2020 Los Angeles Lakers', 112.0, 105.6), ('2020 Miami Heat', 112.5, 109.8),
                ('2021 Milwaukee Bucks', 117.2, 111.0), ('2021 Phoenix Suns', 117.2, 111.3),
                ('2022 Golden State Warriors', 112.5, 106.6), ('2022 Boston Celtics', 114.4, 106.9),
                ('2023 Denver Nuggets', 117.6, 113.5), ('2023 Miami Heat', 113.0, 112.8),
                ('2024 Boston Celtics', 122.2, 109.2), ('2024 Dallas Mavericks', 117.0, 114.9),
                ('2025 Oklahoma City Thunder', 118.5, 108.2), ('2025 Indiana Pacers', 119.8, 115.1),
                ('2026 Boston Celtics', 121.5, 110.1), ('2026 Oklahoma City Thunder', 119.2, 108.7)
            ]
            cursor.executemany("INSERT INTO team_stats (team_name, off_rating, def_rating) VALUES (%s, %s, %s)", team_data)

        # Seed series_history if empty
        cursor.execute("SELECT COUNT(*) FROM series_history")
        if cursor.fetchone()[0] == 0:
            history_data = [
                (2001, 'Los Angeles Lakers', 'Philadelphia 76ers', '4-1', "Shaquille O'Neal", 5),
                (2002, 'Los Angeles Lakers', 'New Jersey Nets', '4-0', "Shaquille O'Neal", 4),
                (2003, 'San Antonio Spurs', 'New Jersey Nets', '4-2', 'Tim Duncan', 6),
                (2004, 'Detroit Pistons', 'Los Angeles Lakers', '4-1', 'Chauncey Billups', 5),
                (2005, 'San Antonio Spurs', 'Detroit Pistons', '4-3', 'Tim Duncan', 7),
                (2006, 'Miami Heat', 'Dallas Mavericks', '4-2', 'Dwyane Wade', 6),
                (2007, 'San Antonio Spurs', 'Cleveland Cavaliers', '4-0', 'Tony Parker', 4),
                (2008, 'Boston Celtics', 'Los Angeles Lakers', '4-2', 'Paul Pierce', 6),
                (2009, 'Los Angeles Lakers', 'Orlando Magic', '4-1', 'Kobe Bryant', 5),
                (2010, 'Los Angeles Lakers', 'Boston Celtics', '4-3', 'Kobe Bryant', 7),
                (2011, 'Dallas Mavericks', 'Miami Heat', '4-2', 'Dirk Nowitzki', 6),
                (2012, 'Miami Heat', 'Oklahoma City Thunder', '4-1', 'LeBron James', 5),
                (2013, 'Miami Heat', 'San Antonio Spurs', '4-3', 'LeBron James', 7),
                (2014, 'San Antonio Spurs', 'Miami Heat', '4-1', 'Kawhi Leonard', 5),
                (2015, 'Golden State Warriors', 'Cleveland Cavaliers', '4-2', 'Andre Iguodala', 6),
                (2016, 'Cleveland Cavaliers', 'Golden State Warriors', '4-3', 'LeBron James', 7),
                (2017, 'Golden State Warriors', 'Cleveland Cavaliers', '4-1', 'Kevin Durant', 5),
                (2018, 'Golden State Warriors', 'Cleveland Cavaliers', '4-0', 'Kevin Durant', 4),
                (2019, 'Toronto Raptors', 'Golden State Warriors', '4-2', 'Kawhi Leonard', 6),
                (2020, 'Los Angeles Lakers', 'Miami Heat', '4-2', 'LeBron James', 6),
                (2021, 'Milwaukee Bucks', 'Phoenix Suns', '4-2', 'Giannis Antetokounmpo', 6),
                (2022, 'Golden State Warriors', 'Boston Celtics', '4-2', 'Stephen Curry', 6),
                (2023, 'Denver Nuggets', 'Miami Heat', '4-1', 'Nikola Jokic', 5),
                (2024, 'Boston Celtics', 'Dallas Mavericks', '4-1', 'Jaylen Brown', 5),
                (2025, 'Oklahoma City Thunder', 'Indiana Pacers', '4-3', 'Shai Gilgeous-Alexander', 7),
                (2026, 'Boston Celtics', 'Oklahoma City Thunder', '4-2', 'Jayson Tatum', 6)
            ]
            cursor.executemany("INSERT INTO series_history (year, champion, runner_up, score, finals_mvp, total_games) VALUES (%s, %s, %s, %s, %s, %s)", history_data)

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database Initialization Notice: {e}")

initdatabase()

def getdbconnection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# --- Simulation Logging Functions ---

def log_simulation(team_a, team_b, iterations, pct_a, pct_b):
    """Inserts a record of a completed simulation into simulation_logs."""
    try:
        conn = getdbconnection()
        cursor = conn.cursor()
        query = """
            INSERT INTO simulation_logs 
            (simulated_at, team_a, team_b, iterations, team_a_win_pct, team_b_win_pct)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(query, (now, team_a, team_b, int(iterations), float(pct_a), float(pct_b)))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to log simulation to database: {e}")

def fetch_simulation_logs():
    """Retrieves the last 50 simulation logs."""
    try:
        conn = getdbconnection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                simulated_at AS `Timestamp`,
                team_a AS `Team A`,
                team_b AS `Team B`,
                iterations AS `Iterations`,
                CONCAT(team_a_win_pct, '%') AS `Team A Win %`,
                CONCAT(team_b_win_pct, '%') AS `Team B Win %`
            FROM simulation_logs
            ORDER BY id DESC
            LIMIT 50
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(rows)
    except Exception:
        return pd.DataFrame()

def clear_simulation_logs():
    """Truncates the simulation_logs table."""
    try:
        conn = getdbconnection()
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE simulation_logs")
        conn.commit()
        cursor.close()
        conn.close()
        return fetch_simulation_logs(), "Simulation logs cleared successfully."
    except Exception as e:
        return fetch_simulation_logs(), f"Error clearing logs: {e}"

# --- Series History & Team Stats Queries ---

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
    try:
        conn = getdbconnection()
        cursor = conn.cursor()
        cursor.execute("SELECT team_name FROM team_stats ORDER BY team_name ASC")
        teams = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return teams if teams else ["2017 Golden State Warriors", "2013 Miami Heat"]
    except Exception:
        return ["2017 Golden State Warriors", "2013 Miami Heat"]

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
    
    # Log simulation result to database
    log_simulation(teama, teamb, sims, round(pcta, 2), round(pctb, 2))
    
    summary = f"{teama} (Off: {offa}, Def: {defa}) vs {teamb} (Off: {offb}, Def: {defb})"
    return summary, f"{pcta:.2f}%", f"{pctb:.2f}%"

# --- Plotly Visualizations ---

def generate_ratings_scatter():
    """Generates an interactive scatter plot comparing Offensive vs Defensive Ratings."""
    try:
        conn = getdbconnection()
        query = """
            SELECT 
                t.team_name, 
                t.off_rating, 
                t.def_rating, 
                ROUND(t.off_rating - t.def_rating, 2) AS net_rating,
                CASE 
                    WHEN s.champion IS NOT NULL THEN 'Champion'
                    ELSE 'Runner-Up'
                END AS status
            FROM team_stats t
            LEFT JOIN series_history s 
                ON t.team_name = CONCAT(s.year, ' ', s.champion)
        """
        df = pd.read_sql(query, conn)
        conn.close()

        fig = px.scatter(
            df,
            x="def_rating",
            y="off_rating",
            color="status",
            hover_name="team_name",
            hover_data={"net_rating": True, "off_rating": True, "def_rating": True, "status": False},
            title="Offensive Rating vs. Defensive Rating (2001–2026)",
            labels={
                "def_rating": "Defensive Rating (Lower is Better)",
                "off_rating": "Offensive Rating (Higher is Better)",
                "status": "Finals Outcome"
            },
            color_discrete_map={"Champion": "#FFD700", "Runner-Up": "#94A3B8"}
        )
        fig.update_xaxes(autorange="reversed")
        fig.update_layout(
            template="plotly_dark",
            height=500,
            font=dict(family="Arial, sans-serif", size=12)
        )
        return fig
    except Exception as e:
        print(f"Error building scatter chart: {e}")
        return go.Figure()

def generate_era_trend():
    """Generates an interactive trend line showing rating evolution across years."""
    try:
        conn = getdbconnection()
        query = """
            SELECT 
                CAST(LEFT(team_name, 4) AS UNSIGNED) AS year,
                ROUND(AVG(off_rating), 2) AS avg_off_rating,
                ROUND(AVG(def_rating), 2) AS avg_def_rating
            FROM team_stats
            GROUP BY year
            ORDER BY year ASC
        """
        df = pd.read_sql(query, conn)
        conn.close()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["year"], y=df["avg_off_rating"],
            mode="lines+markers", name="Avg Offensive Rating",
            line=dict(color="#10B981", width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df["year"], y=df["avg_def_rating"],
            mode="lines+markers", name="Avg Defensive Rating",
            line=dict(color="#EF4444", width=3)
        ))

        fig.update_layout(
            title="NBA Finals Efficiency Rating Trends Across Eras (2001–2026)",
            xaxis_title="Year",
            yaxis_title="Rating Value",
            template="plotly_dark",
            height=500,
            hovermode="x unified"
        )
        return fig
    except Exception as e:
        print(f"Error building trend chart: {e}")
        return go.Figure()

# --- Gradio UI Layout ---

teamoptions = fetchallteams()

with gr.Blocks(title="HoopsData - NBA Analytics Platform") as mainapp:
    gr.Markdown("# 🏀 HoopsData - NBA Finals Analytics & Simulation Engine")

    with gr.Tabs():
        
        # TAB 1: Series History
        with gr.TabItem("Series History"):
            gr.Markdown("### Historical NBA Finals Records (2001–2026)")
            with gr.Row():
                start_input = gr.Number(label="Start Year", value=2001, precision=0)
                end_input = gr.Number(label="End Year", value=2026, precision=0)
            fetch_btn = gr.Button("Query History", variant="primary")
            history_df = gr.Dataframe(value=fetchserieshistory(2001, 2026), label="Finals Records")
            fetch_btn.click(fn=fetchserieshistory, inputs=[start_input, end_input], outputs=history_df)

        # TAB 2: Matchup Simulator
        with gr.TabItem("Matchup Simulator"):
            gr.Markdown("### Monte Carlo Series Simulation Engine")
            with gr.Row():
                team_a_dropdown = gr.Dropdown(choices=teamoptions, label="Select Team A", value=teamoptions[0])
                team_b_dropdown = gr.Dropdown(choices=teamoptions, label="Select Team B", value=teamoptions[1] if len(teamoptions) > 1 else teamoptions[0])
            
            sim_slider = gr.Slider(minimum=1000, maximum=50000, step=1000, value=10000, label="Simulation Iterations")
            sim_btn = gr.Button("Run Simulation", variant="primary")

            with gr.Row():
                rating_breakdown = gr.Textbox(label="Ratings Breakdown")
                team_a_win_out = gr.Textbox(label="Team A Win Chance")
                team_b_win_out = gr.Textbox(label="Team B Win Chance")

            sim_btn.click(
                fn=runmontecarlosimulation,
                inputs=[team_a_dropdown, team_b_dropdown, sim_slider],
                outputs=[rating_breakdown, team_a_win_out, team_b_win_out]
            )

        # TAB 3: Visual Analytics
        with gr.TabItem("Visual Analytics"):
            gr.Markdown("### Interactive Efficiency Data Visualizations")
            refresh_charts_btn = gr.Button("Refresh Charts")
            
            with gr.Row():
                scatter_plot = gr.Plot(value=generate_ratings_scatter(), label="Offensive vs Defensive Efficiency")
            with gr.Row():
                trend_plot = gr.Plot(value=generate_era_trend(), label="Era Efficiency Trends")

            refresh_charts_btn.click(
                fn=lambda: (generate_ratings_scatter(), generate_era_trend()),
                outputs=[scatter_plot, trend_plot]
            )

        # TAB 4: Simulation Logs
        with gr.TabItem("Simulation History Logs"):
            gr.Markdown("### Database Simulation Run Logs")
            with gr.Row():
                refresh_logs_btn = gr.Button("Refresh Logs", variant="primary")
                clear_logs_btn = gr.Button("Clear All Logs", variant="stop")
            
            status_box = gr.Textbox(label="System Status", value="Ready")
            logs_df = gr.Dataframe(value=fetch_simulation_logs(), label="Recent Simulations (Stored in MySQL)")

            refresh_logs_btn.click(fn=fetch_simulation_logs, outputs=logs_df)
            clear_logs_btn.click(fn=clear_simulation_logs, outputs=[logs_df, status_box])

if __name__ == "__main__":
    mainapp.launch(inbrowser=True)