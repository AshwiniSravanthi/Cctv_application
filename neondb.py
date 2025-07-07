import psycopg2
import uuid
from datetime import datetime
import os

DATABASE_URL = "postgresql://neondb_owner:npg_uXQr3V7pbLOx@ep-shy-king-a82p1v83-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"

# ✅ Establish connection using DATABASE_URL
conn = psycopg2.connect(DATABASE_URL)

# ✅ Create enquiries table
def create_enquiry_table():
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone_number TEXT,
            message TEXT,
            submitted_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    conn.commit()
    cursor.close()
    print("✅ enquiries table created.")

# ✅ Insert new enquiry
def insert_enquiry(name: str, email: str, phone: str, message: str):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO enquiries (name, email, phone_number, message)
        VALUES (%s, %s, %s, %s);
    """, (name, email, phone, message))
    conn.commit()
    cursor.close()