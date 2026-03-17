import pandas as pd
import psycopg2
from psycopg2 import extras
import os

# =========================
# CSV PATH 
# =========================

file_path = "data/market_price.csv"

# =========================
# READ CSV
# =========================

df = pd.read_csv(file_path)


df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# clean column name
df.columns = [
    c.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
    for c in df.columns
]

print("rows:", len(df))

# =========================
# CONNECT POSTGRES
# =========================

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    database=os.getenv("DB_NAME", "market_intelligence"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

# =========================
# CLEAR TABLE
# =========================

cur.execute("TRUNCATE TABLE market_price RESTART IDENTITY")

print("old data cleared")

# =========================
# INSERT DATA
# =========================

columns = ",".join([f'"{c}"' for c in df.columns])

values = [tuple(x) for x in df.values]

insert_query = f"""
INSERT INTO market_price ({columns})
VALUES %s
"""

extras.execute_values(cur, insert_query, values)

conn.commit()

print("market price updated:", len(df))

cur.close()
conn.close()