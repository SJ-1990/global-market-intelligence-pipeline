from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from datetime import datetime
import psycopg2
import os


# =========================
# 1. CHROME OPTIONS (WSL)
# =========================

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

chrome_options.add_argument(
"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
)


# =========================
# 2. DATABASE CONNECTION
# =========================

try:

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "market_intelligence"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )

    cursor = conn.cursor()

    print("Connected to PostgreSQL")

except Exception as e:

    print("Database connection error:", e)
    exit()


# =========================
# 3. SELENIUM SCRAPING
# =========================

driver = webdriver.Chrome(options=chrome_options)

try:

    print("Opening News stream...")

    driver.get("SOURCE_URL")

    time.sleep(10)


    # ---------------------
    # SCROLL LOAD NEWS
    # ---------------------

    news_target = 100

    last_count = 0
    stuck_count = 0

    print("Start scrolling for news...")

    while True:

        items = driver.find_elements(By.CSS_SELECTOR, "li.te-stream-item")

        current_count = len(items)

        print("news loaded:", current_count)

        if current_count >= news_target:
            print("Reached target news")
            break

        if current_count == last_count:

            stuck_count += 1

            if stuck_count >= 3:
                print("Page stopped loading more items")
                break

        else:
            stuck_count = 0

        last_count = current_count

        driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(4)


    # ---------------------
    # PARSE NEWS
    # ---------------------

    data = []

    items = driver.find_elements(By.CSS_SELECTOR,"li.te-stream-item")[:current_count]


    for item in items:

        def get_text(selector):

            try:
                return item.find_element(By.CSS_SELECTOR,selector).text
            except:
                return ""

        data.append({

            "date": get_text(".te-stream-date"),
            "country": get_text(".te-stream-country"),
            "type": get_text(".te-stream-category"),
            "headline": get_text("b"),
            "news": get_text(".te-stream-item-description"),
            "source": ("NEWS"),
            "scrape_time": datetime.now()

        })


finally:

    driver.quit()


# ======================
# DATA QUALITY CHECK
# ======================

print("news collected:", len(data))

if len(data) < 20:
    raise Exception("Scrape error: news too low - website structure may have changed")


# =========================
# 4. INSERT DATA TO SQL
# =========================

df = pd.DataFrame(data)

print("Total news:", len(df))


cursor.execute(
"TRUNCATE TABLE public.te_news RESTART IDENTITY"
)


sql = """

INSERT INTO public.te_news
(date, country, type, headline, news, source, scrape_time)
VALUES (%s,%s,%s,%s,%s,%s,%s)

"""


for _, row in df.iterrows():

    cursor.execute(

        sql,

        (

            row["date"],
            row["country"],
            row["type"],
            row["headline"],
            row["news"],
            row["source"],
            row["scrape_time"]

        )

    )


conn.commit()

print("Inserted news rows:", len(df))


# =========================
# 5. CLOSE CONNECTION
# =========================

cursor.close()
conn.close()

print("Pipeline finished")