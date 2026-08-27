import streamlit as st
import mysql.connector

st.title("🧪 Streamlit & MySQL Connection Test")

# 1. Test basic Streamlit rendering
st.write("If you can see this, Streamlit is running correctly!")

# 2. Test MySQL database connection
try:
    connection = mysql.connector.connect(
        host=st.secrets["mysql"]["altaria.proxy.rlwy.net"],
        port=st.secrets["mysql"]["55284"],
        user=st.secrets["mysql"]["root"],
        password=st.secrets["mysql"]["ddxOXmHeEmffQEdePamKSfHvrphOXbyf"],
        database=st.secrets["mysql"]["series_history"]
    )
    
    if connection.is_connected():
        st.success("✅ Successfully connected to the Cloud MySQL Database!")
        
        # Query your test table
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM series_history LIMIT 5;")
        records = cursor.fetchall()
        
        st.subheader("Database Sample Output (First 5 Rows):")
        st.dataframe(records)
        
        cursor.close()
        connection.close()

except Exception as e:
    st.error(f"❌ Connection failed: {e}")