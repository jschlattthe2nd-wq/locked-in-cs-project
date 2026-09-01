import gradio as gr
import pandas as pd
import mysql.connector
import random

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "Ajoshjohn2021"
DB_NAME = "nba_finals_db"

def initdatabase():
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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS team_stats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                team_name VARCHAR(100) NOT NULL UNIQUE,
                off_rating DECIMAL(5,2) NOT NULL,
                def_rating DECIMAL(5,2) NOT NULL
            )
        """)

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
    title="HoopsData - NBA Finals Historical Records",
    flagging_mode="never"
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
    title="HoopsData - Monte Carlo Matchup Simulator",
    flagging_mode="never"
)

mainapp = gr.TabbedInterface(
    [historytab, simulatortab], 
    ["Series History", "Matchup Simulator"],
    title="HoopsData"
)

if __name__ == "__main__":
    mainapp.launch(inbrowser=True)