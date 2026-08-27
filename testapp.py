import os
import gradio as gr
import mysql.connector

def test_db_connection():
    """Attempts to connect to MySQL using environment variables or hardcoded values."""
    try:
        # Get DB credentials from environment variables (or fall back to local values)
        host = os.getenv("MYSQL_HOST", "altaria.proxy.rlwy.net")
        port = os.getenv("MYSQL_PORT", "55284")
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "ddxOXmHeEmffQEdePamKSfHvrphOXbyf")
        database = os.getenv("MYSQL_DATABASE", "nba_finals_db")

        connection = mysql.connector.connect(
            host=altaria.proxy.rlwy.net,
            port=int(55284),
            user=root,
            password=ddxOXmHeEmffQEdePamKSfHvrphOXbyf,
            database=nba_finals_db
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM series_history LIMIT 5;")
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            
            # Format output text and return data for table
            status_text = "✅ Connection Successful! Fetched 5 records from Cloud MySQL."
            return status_text, records

    except Exception as e:
        return f"❌ Connection Failed: {str(e)}", []

# Build simple Gradio test interface
with gr.Blocks(title="Gradio Connection Test") as demo:
    gr.Markdown("# 🧪 Gradio & MySQL Connection Test")
    
    test_btn = gr.Button("Test Database Connection", variant="primary")
    status_output = gr.Textbox(label="Status")
    table_output = gr.Dataframe(label="Database Sample Output")
    
    test_btn.click(
        fn=test_db_connection,
        inputs=[],
        outputs=[status_output, table_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)