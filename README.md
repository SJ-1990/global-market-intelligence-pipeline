🌍 MarketAgent AI: Global Intelligence Pipeline
Automated Macro-Economic Monitoring & AI-Driven Insights (EN/TH)

<img width="1425" height="785" alt="image" src="https://github.com/user-attachments/assets/ac9f9f34-2796-4fc7-9a23-5ad4a89ea9f2" />

📌 Project Overview
MarketAgent AI is an automated end-to-end data pipeline designed to combat Information Overload in the financial landscape. The system transforms massive streams of unstructured news from TradingEconomics into structured, high-level strategic summaries, enabling users to stay ahead of global macro shifts with zero manual effort.

Core Data Flow:
Data Source → Processing → Storage → Visualization

Data Source: TradingEconomics (Real-time news stream)

Processing: Python (Selenium) + Gemini AI (Summarization)

Orchestration: Apache Airflow (Automated Scheduling)

Storage: PostgreSQL (Relational Database)

Visualization: Power BI (Interactive Dashboard)

⚙️ Pipeline Architecture & Automation
The project follows a modular ETL approach managed by Apache Airflow:

Extraction: Custom Python (Selenium) scraper to ingest dynamic web content from TradingEconomics.

AI Enrichment: Utilizing the Gemini AI API (Free Tier) to perform automated sentiment analysis and thematic summarization in both English and Thai.

Orchestration: Airflow DAGs manage the automated scheduling, task dependencies, and retry logic to ensure daily data consistency.

Storage: Processed insights are stored in PostgreSQL using Upsert (ON CONFLICT) logic to prevent duplication and maintain historical records.

Visualization: A Power BI Dashboard connected to PostgreSQL for real-time monitoring and historical trend analysis.

🚀 Technical Highlights
Cost-Efficient AI Strategy: Strategically implemented Gemini AI (Free Tier) to provide institutional-grade summarization with zero API overhead.

Automated Workflow: Fully hands-off execution via Airflow, moving from manual scripts to a managed, monitored pipeline.

Robust Scraping: Configured Headless Chrome and WebDriverWait for stable data extraction from dynamic financial platforms.

Strategic Intelligence: Engineered prompts to extract specific categories such as Commodities (Energy, Metals) and Global Stock Markets (US, China, Europe, India, etc.).
---

## 🧰 Tech Stack

- **Python** (pandas, selenium)  
- **Airflow** (pipeline orchestration)  
- **PostgreSQL** (data storage)  
- **Power BI** (data visualization)  
- **Gemini API** (AI analysis)

---
📊 Use Case: Market Intelligence Command Center
This pipeline transforms raw data into a strategic asset for financial professionals:

1. Morning Market Briefing
The Problem: Spending 1-2 hours manually reading global news before the market opens.

The Solution: MarketAgent AI delivers a structured summary of global events in under 5 minutes, allowing for immediate strategic action.

2. Cross-Asset Correlation
The Problem: Difficulty tracking how macro events (e.g., Fed policy) impact different assets simultaneously.

The Solution: Integrated Power BI visualization helps analysts correlate AI-processed news themes with price movements across Energy, Metals, and Equities.

3. Institutional Knowledge Base
The Problem: Historical market context is often lost as news cycles move forward.

The Solution: Permanent storage in PostgreSQL creates a searchable database of past macro events and market reactions for long-term trend analysis.

4. Localized Macro Strategy
The Problem: High-quality macro analysis is often trapped behind language barriers.

The Solution: Automated Dual-Language (EN/TH) summaries enable instant communication of global shifts to local Thai stakeholders or investment committees.
