# **End-to-End Stock Data Handling and Prediction Project**

## **Overview**
This project presents a robust data pipeline for stock market analysis and predictions. Users can interact through a Streamlit interface to fetch, store, and analyze historical stock data while leveraging advanced machine learning and natural language processing for actionable insights. The system is fully containerized with Docker, ensuring seamless deployment and scalability.

Key highlights include:

1. Data Retrieval and Storage: Automatically fetches stock data from Yahoo Finance and stores it in a MySQL database for structured analysis.
2. Predictive Analytics: Employs XGBoost to forecast next-day stock prices based on historical trends.
3. Intelligent Recommendations: Utilizes a Large Language Model (LLM) to provide meaningful stock-related insights and recommendations.
4. Scalable Deployment: Dockerized architecture guarantees consistent performance across diverse environments

---

## **Features**
- **Streamlit Interface**: An intuitive UI for stock ticker input.
- **Automated Data Retrieval**: Fetches historical data using **yfinance**.
- **Database Integration**: Persists data securely in a **MySQL** database.
- **Machine Learning Predictions**: Leverages **XGBoost** for forecasting.
- **LLM-Powered Insights**: Provides actionable recommendations with **Ollama** and **Llama 3.2**.
- **Dockerized Environment**: Simplifies setup, sharing, and deployment.

---

## **Technologies Used**
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Data Retrieval**: [yfinance](https://pypi.org/project/yfinance/)
- **Database**: [MySQL](https://www.mysql.com/)
- **Machine Learning**: [XGBoost](https://xgboost.readthedocs.io/)
- **LLM**: [Ollama](https://ollama.com/) with [Llama 3.2 1B Model](https://ai.meta.com/blog/meta-llama-3-1/)
- **Containerization**: [Docker](https://www.docker.com/)

---

## **How It Works**
1. **User Input**:
   - Users enter a stock ticker symbol (e.g., AAPL, MSFT) via the Streamlit interface.

2. **Data Fetching**:
   - The application retrieves historical stock data from **Yahoo Finance**.

3. **Price Prediction**:
   - **XGBoost** processes the data to forecast the stock's next-day price.

4. **Recommendation Generation**:
   - The **LLM** generates textual insights or recommendations based on the stock data.

5. **Data Storage**:
   - Data is securely stored in a **MySQL database** for analysis and persistence.

6. **Containerization**:
   - The entire project is dockerized for consistency across different environments.

---

## **Setup Instructions**

### Prerequisites
- Ensure **Docker** and **Docker Compose** are installed on your system.

### Steps
- **First time setup**
(*Remember to do all the steps!*)

1. Clone the repo
```bash
git clone https://github.com/GovindTV/End-to-End-Data-Handling-Project.git
cd End-to-End-Data-Handling-Project
```

2. Build the container and start the server
```bash
docker-compose up --build -d
```

3. Download the required local LLM and exit from its interface
```bash
docker exec -it end-to-end-data-handling-project-ollama-1 ollama run llama3.2:1b
/bye
```

**Subsequent setup**
```bash
docker-compose up
```

**End session**
```bash
docker-compose down
```

---

## **Future Enhancements**
- ~~Secure database credentials using an .env file.~~
- ~~Containerization~~
- ~~Expand SQL query capabilities for advanced data analysis.~~
- Select SQL query from streamlit interface
- Introduce AI-powered data transformation and preprocessing layers.
- Deploy the application to cloud platforms (e.g., AWS, Azure, GCP).

---

## **Contact**
For feedback, questions, or collaboration opportunities, reach out:

[**LinkedIn**](https://linkedin.com/in/govindtv)  
[**GitHub**](https://github.com/GovindTV)

---

Does this meet your expectations? Let me know if you’d like any tweaks or have any opinions!