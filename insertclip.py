import psycopg2
from datetime import date

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="clips_db",        # Database name
    user="clips_user",        # Database user
    password="yourpassword",  # Database password
    host="localhost"          # Host (localhost if running locally)
)

# Create a cursor object to interact with the database
cur = conn.cursor()

# Define clip data
file_path = "clip2.mp4"
week_start = date(2025, 4, 14)   # Adjust this as needed
player_names = ["Caleb Williams"]
length_seconds = 15
highlight_meter = 9.3

# Insert clip into the database
cur.execute("""
    INSERT INTO clips (file_path, week_start, player_names, length_seconds, highlight_meter)
    VALUES (%s, %s, %s, %s, %s)
""", (file_path, week_start, player_names, length_seconds, highlight_meter))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Clip added successfully!")
