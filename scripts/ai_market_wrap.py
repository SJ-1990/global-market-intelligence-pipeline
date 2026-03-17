import pandas as pd
import google.generativeai as genai
import psycopg2
import re
from datetime import date, datetime
import os

# =========================
# AI API
# =========================

API_KEY = os.getenv("AI_API_KEY")
genai.configure(api_key=API_KEY)

today = date.today()

# =========================
# POSTGRES CONNECTION
# =========================

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    database=os.getenv("DB_NAME", "market_intelligence"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD")
)
# =========================
# LOAD NEWS FROM DATABASE
# =========================

query = """
SELECT *
FROM te_news
ORDER BY scrape_time DESC
LIMIT 300
"""

data = pd.read_sql(query, conn)

print("total news:", len(data))

# =========================
# FILTER NEWS
# =========================

df_filtered = data[data["type"] != "Other"].copy()

print("filtered news:", len(df_filtered))

df_filtered["headline"] = df_filtered["headline"].fillna("")
df_filtered["news"] = df_filtered["news"].fillna("")

news_text = "\n\n".join(
    df_filtered["headline"] + " : " + df_filtered["news"]
)

# =========================
# PROMPT
# =========================

prompt = f"""
You are a global macro strategist at an investment bank preparing a weekly market wrap for investors.

Analyze the following macro, commodity, and equity market news and summarize the key developments over the past week.

Output format EXACTLY as follows:

Weekly Wrap ({today})

English Summary

Commodity

Energy
(summary)

Metals
(summary)

Agricultural
(summary)

Stock Market

US
(summary)

China
(summary)

Euro_Area
(summary)

Japan
(summary)

South_korea
(summary)

India
(summary)

All_Global_stock_and_commoddities
(summary)

Thai Summary

Commodity

Energy
(summary ภาษาไทย)

Metals
(summary ภาษาไทย)

Agricultural
(summary ภาษาไทย)

Stock Market

US
(summary ภาษาไทย)

China
(summary ภาษาไทย)

Euro_Area
(summary ภาษาไทย)

Japan
(summary ภาษาไทย)

South_korea
(summary ภาษาไทย)

India
(summary ภาษาไทย)

All_Global_stock_and_commoddities
(summary ภาษาไทย)

News:
{news_text}
"""

# =========================
# CALL AI_MODEL
# =========================

model = genai.GenerativeModel("AI_MODEL")

response = model.generate_content(prompt)

text = response.text

print(text)

# =========================
# SPLIT ENGLISH / THAI
# =========================

eng_block = re.search(r"English Summary(.*?)Thai Summary", text, re.S).group(1)
thai_block = re.search(r"Thai Summary(.*)", text, re.S).group(1)

# =========================
# CLEAN HEADER
# =========================

eng_block = re.sub(r"Commodity\s*", "", eng_block)
eng_block = re.sub(r"Stock Market\s*", "", eng_block)

thai_block = re.sub(r"Commodity\s*", "", thai_block)
thai_block = re.sub(r"Stock Market\s*", "", thai_block)

# =========================
# SECTIONS
# =========================

sections = [
    "Energy",
    "Metals",
    "Agricultural",
    "US",
    "China",
    "Euro_Area",
    "Japan",
    "South_korea",
    "India",
    "All_Global_stock_and_commoddities"
]

sections_pattern = "|".join(sections)

rows = []

for sec in sections:

    pattern_eng = rf"{sec}\s*\n(.*?)(?=\n(?:{sections_pattern})\s*\n|\Z)"
    match_eng = re.search(pattern_eng, eng_block, re.S)
    eng_text = match_eng.group(1).strip() if match_eng else ""

    pattern_th = rf"{sec}\s*\n(.*?)(?=\n(?:{sections_pattern})|\Z)"
    match_th = re.search(pattern_th, thai_block, re.S)
    thai_text = match_th.group(1).strip() if match_th else ""

    rows.append({
        "date": today,
        "section": sec,
        "english_summary": eng_text,
        "thai_summary": thai_text
    })

df_wrap = pd.DataFrame(rows)

print(df_wrap)

cursor = conn.cursor()

# =========================
# INSERT HISTORY TABLE
# =========================

sql_history = """
INSERT INTO weekly_market_wrap (date, section, english_summary, thai_summary)
VALUES (%s, %s, %s, %s)
ON CONFLICT (date, section) 
DO UPDATE SET 
english_summary = EXCLUDED.english_summary,
thai_summary = EXCLUDED.thai_summary;
"""

for _, row in df_wrap.iterrows():
    cursor.execute(sql_history, (
        row["date"],
        row["section"],
        row["english_summary"],
        row["thai_summary"]
    ))

print("History updated")

# =========================
# UPDATE LATEST TABLE
# =========================

cursor.execute("TRUNCATE TABLE weekly_market_latest RESTART IDENTITY")

sql_latest = """
INSERT INTO weekly_market_latest
(section, english_summary, thai_summary, updated_at)
VALUES (%s,%s,%s,%s)
"""

for _, row in df_wrap.iterrows():
    cursor.execute(sql_latest, (
        row["section"],
        row["english_summary"],
        row["thai_summary"],
        datetime.now()
    ))

print("Latest updated")

conn.commit()

cursor.close()
conn.close()

print("AI Market Wrap Completed")
