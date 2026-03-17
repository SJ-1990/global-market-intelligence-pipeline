from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="global_market_intelligence_pipeline",
    start_date=datetime(2024,1,1),
    schedule="0 16 * * *",
    catchup=False
) as dag:

    scrape_news = BashOperator(
        task_id="scrape_news",
        bash_command="python scripts/scrape_te_news.py"
    )

    ai_summary = BashOperator(
        task_id="ai_market_wrap",
        bash_command="python scripts/ai_market_wrap.py"
    )

    market_price = BashOperator(
        task_id="import_market_price",
        bash_command="python scripts/import_market_price.py"
    )

    metrics = BashOperator(
        task_id="market_metrics",
        bash_command="python scripts/market_metrics.py"
    )

    scrape_news >> ai_summary >> market_price >> metrics
