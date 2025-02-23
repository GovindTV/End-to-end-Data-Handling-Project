import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import streamlit as st
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data.columns = stock_data.columns.get_level_values(0)
    stock_data.reset_index(inplace=True)
    return stock_data

def prepare_data(data):
    from ta import add_all_ta_features

    
    data = add_all_ta_features(
        data, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True
    )

    data['Target'] = data['Close'].shift(-1)
    data = data.iloc[:-1] # Removes latest entry as we do not know its target (i.e., today's price)
    return data

def load_df_to_mysql(ticker, data):
    user = os.getenv('MYSQL_USER', 'default_user')
    password = os.getenv('MYSQL_PASSWORD', 'default_password')
    host = os.getenv('MYSQL_HOST', 'localhost')
    db_name = os.getenv('MYSQL_DATABASE', 'project_stocks_db')
    
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")
    
    data.to_sql(
        name=ticker.lower(), 
        con=engine, 
        if_exists='replace',
        index=True 
    )
    
    print(f"SQL Load done for {ticker}")

def train_model(features, target):    
    import xgboost as xgb
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    accuracy = r2 * 100
    
    return model, mse, accuracy

def get_stock_recommendation(ticker, data):
    import httpx
    import ollama

    os.environ["OLLAMA_HOST"] = "http://ollama:11434"
    
    # The Llama model used does not have the ability to access the required below data to fulfill the below requests. It is purely hallucinating.
    prompt = f"""
        Given the stock ticker {ticker} and its historical data with all technical indicators {data}, please provide a recommendation to buy or sell, based on the following factors:
        1. Current stock price and performance trends.
        2. Recent news or events impacting the company.
        3. Financial health (e.g., earnings reports, revenue, debt levels).
        4. Market sentiment and sector performance.
        5. Technical analysis indicators (e.g., moving averages, RSI).
        6. General market conditions (bullish or bearish trend).
          
        Consider both short-term and long-term factors in your recommendation.
        """

    try:
        client = ollama.Client()
        response = client.generate(
            model="deepseek-r1:1.5b",
            prompt=prompt
        )
        return response['response']
    except httpx.ConnectError as e:
        print(f"Connection failed: {e}")
        return "Connection error. Please ensure the server is running."

load_dotenv()
st.title("Stock Price Prediction App")

st.sidebar.header("Input Parameters")
ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=datetime.now() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", value=datetime.now())

## Future update : SQL query selection option
# option = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone"),
#     index=None,
#     placeholder="Select contact method...",
# )

if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        stock_data = get_stock_data(ticker, start_date, end_date)
        
        if stock_data.empty:
            st.error("No data found. Please check the ticker and date range.")
        else:
            st.success(f"Data fetched for {ticker}!")
            st.write("Stock Data Preview:")
            st.dataframe(stock_data)

            processed_data = prepare_data(stock_data)
            st.write("Processed Data Preview:")
            st.dataframe(processed_data)

            features = processed_data[processed_data.columns[1:-1]]
            target = processed_data['Target']

            with st.spinner("Training model..."):
                model, mse, accuracy = train_model(features, target)
                st.success("Model trained successfully!")
                st.write(f"Model Mean Squared Error: {mse:.2f} & Accuracy: {accuracy:.2f}")

            next_day_features = features.iloc[-1:].values  # Use last row for prediction
            next_day_prediction = model.predict(next_day_features)[0]
            st.write(f"Predicted Price for Next Trading Day: {next_day_prediction:.2f}")

            st.write("Historical Closing Prices")
            plt.figure(figsize=(10, 5))
            plt.plot(stock_data['Close'], label="Closing Price")
            plt.axhline(y=next_day_prediction, color='r', linestyle='--', label="Predicted Price")
            plt.title(f"{ticker} Closing Prices")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.legend()
            st.pyplot(plt)
                    
            with st.spinner("Getting recommendation from Deepseek R1..."):
                recommendation = get_stock_recommendation(ticker, processed_data)
                st.write(f"AI stock recommendation: {recommendation}")

            with st.spinner("Loading data to MySQL db"):
                load_df_to_mysql(ticker,stock_data)