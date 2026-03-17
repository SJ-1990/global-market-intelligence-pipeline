import pandas as pd
import psycopg2
from psycopg2 import extras
import os

# =========================
# CSV PATH 
# =========================

file_path = "data/market_price.csv"
# =========================
# LOAD CSV
# =========================

df = pd.read_csv(file_path)

df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

df = df.sort_values("Date").reset_index(drop=True)

# =========================
# CONNECT DATABASE
# =========================

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    database=os.getenv("DB_NAME", "market_intelligence"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD")
)


cur = conn.cursor()

# =================================================
# 1️⃣ MARKET SUMMARY
# =================================================

summary_list = []

for col in df.columns[1:]:

    try:

        latest_price = df[col].iloc[-1]

        price_1d_ago = df[col].iloc[-2]

        price_1w_ago = df[col].iloc[-6]

        price_1m_ago = df[col].iloc[-21]

        pct_1d = ((latest_price - price_1d_ago) / price_1d_ago) * 100
        pct_1w = ((latest_price - price_1w_ago) / price_1w_ago) * 100
        pct_1m = ((latest_price - price_1m_ago) / price_1m_ago) * 100

        summary_list.append({
            "asset": col,
            "latest_price": latest_price,
            "pct_1d": round(pct_1d,2),
            "pct_1w": round(pct_1w,2),
            "pct_1m": round(pct_1m,2)
        })

    except:
        pass

df_summary = pd.DataFrame(summary_list)

cur.execute("DROP TABLE IF EXISTS market_summary")

cur.execute("""
CREATE TABLE market_summary(
asset TEXT,
latest_price NUMERIC,
pct_1d NUMERIC,
pct_1w NUMERIC,
pct_1m NUMERIC
)
""")

columns = ",".join(df_summary.columns)

values = [tuple(x) for x in df_summary.values]

insert_query = f"INSERT INTO market_summary ({columns}) VALUES %s"

extras.execute_values(cur, insert_query, values)

print("market_summary updated")

# =================================================
# 2️⃣ MARKET REBASE
# =================================================

df_rebase = pd.DataFrame()

df_rebase["date"] = df["Date"].dt.strftime("%Y-%m-%d")

for col in df.columns[1:]:

    first_price = df[col].iloc[0]

    clean_col = col.lower().replace(" ","_").replace("(","").replace(")","")

    if first_price != 0 and pd.notnull(first_price):

        df_rebase[clean_col] = (df[col] / first_price) * 100

    else:

        df_rebase[clean_col] = 100.0

cur.execute("DROP TABLE IF EXISTS market_rebase")

cols_sql = [f'"{df_rebase.columns[0]}" DATE']

for c in df_rebase.columns[1:]:

    cols_sql.append(f'"{c}" NUMERIC')

create_query = f"CREATE TABLE market_rebase ({', '.join(cols_sql)})"

cur.execute(create_query)

columns = ",".join([f'"{c}"' for c in df_rebase.columns])

values = [tuple(x) for x in df_rebase.values]

insert_query = f"INSERT INTO market_rebase ({columns}) VALUES %s"

extras.execute_values(cur, insert_query, values)

print("market_rebase updated")

# =========================
# COMMIT
# =========================

conn.commit()

cur.close()

conn.close()

print("market metrics pipeline completed")