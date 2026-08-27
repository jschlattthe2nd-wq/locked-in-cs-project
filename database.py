import mysql.connector
import pandas as pd

def fetch_dataframe(query, params=None):
    """Connects to MySQL, executes a query, and returns a Pandas DataFrame."""
    try:
        connection = mysql.connector.connect(
            host="altaria.proxy.rlwy.net",       # Or your cloud host (e.g., Railway/Aiven)
            port=55284,              # Default MySQL port (or your custom 5-digit port)
            user="root",            # Your MySQL username
            password="ddxOXmHeEmffQEdePamKSfHvrphOXbyf", # Your MySQL password
            database="nba_finals_db"  # Your database name
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return pd.DataFrame(result) if result else pd.DataFrame()
    except Exception as e:
        print(f"Database Error: {e}")
        return pd.DataFrame()