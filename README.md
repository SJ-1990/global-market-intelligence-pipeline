# 🌍 MarketAgent AI — Global Market Intelligence Pipeline


<img width="1429" height="788" alt="image" src="https://github.com/user-attachments/assets/ea8b0bb0-3933-4498-92f6-5ddbef1e3b76" />

## 📌 Project Overview

**MarketAgent AI** is an automated end-to-end data pipeline designed to combat **information overload in financial markets**.

The system transforms massive streams of unstructured news from TradingEconomics into **structured, high-level strategic insights**, enabling faster and more informed investment decisions with zero manual effort.


## 🔄 Core Data Flow

**Data Source → Processing → Storage → Visualization**

- **Data Source:** TradingEconomics (real-time news stream)  
- **Processing:** Python (Selenium) + Gemini AI (summarization)  
- **Orchestration:** Apache Airflow (automated scheduling)  
- **Storage:** PostgreSQL (relational database)  
- **Visualization:** Power BI (interactive dashboard)  


## ⚙️ Pipeline Architecture & Automation

This project follows a **modular ETL architecture** orchestrated by Apache Airflow:

- **Extraction**  
  Custom Python (Selenium) scraper for dynamic financial data  

- **AI Enrichment**  
  Gemini AI API for sentiment analysis and bilingual (EN/TH) summarization  

- **Orchestration**  
  Airflow DAGs manage scheduling, dependencies, and retry logic  

- **Storage**  
  PostgreSQL with **UPSERT (ON CONFLICT)** to prevent duplication  

- **Visualization**  
  Power BI dashboard for real-time monitoring and trend analysis  



## 🚀 Technical Highlights

- **Cost-Efficient AI Strategy**  
  Leveraged Gemini AI (Free Tier) for zero-cost, high-quality summarization  

- **Fully Automated Workflow**  
  End-to-end pipeline with Airflow scheduling (no manual intervention)  

- **Robust Web Scraping**  
  Headless Chrome + WebDriverWait for stable extraction from dynamic sites  

- **Strategic Intelligence Design**  
  Prompt engineering to extract key categories:  
  - Commodities (Energy, Metals)  
  - Global Equities (US, China, Europe, India)  


## 🧰 Tech Stack

- Python (pandas, selenium)  
- Apache Airflow  
- PostgreSQL  
- Power BI  
- Gemini API  

---

## 📊 Use Case: Market Intelligence Command Center

This pipeline transforms raw data into **actionable investment intelligence**:

### 1. Morning Market Briefing
**Problem:**  Manual news reading takes 1–2 hours daily  

**Solution:**  AI-generated summaries in under 5 minutes for immediate decision-making  


### 2. Cross-Asset Correlation
**Problem:**  Difficult to link macro events with multiple asset classes  

**Solution:**  Power BI enables visualization across:  Energy   Metals  Equities  


### 3. Institutional Knowledge Base
**Problem:**  Market context is lost over time  

**Solution:**  PostgreSQL stores historical insights for long-term analysis  


### 4. Localized Macro Strategy
**Problem:**  Language barriers limit accessibility  

**Solution:**  Dual-language (EN/TH) summaries for Thai investment teams  


## 💡 Key Strength

- End-to-end pipeline (data → AI → dashboard)  
- Combines financial analysis with data engineering  
- Real-world use case for investment workflow automation  


