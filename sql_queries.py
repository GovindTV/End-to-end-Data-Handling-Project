from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv()

user = os.getenv('MYSQL_USER', 'default_user')
password = os.getenv('MYSQL_PASSWORD', 'default_password')
host = os.getenv('MYSQL_HOST', 'localhost')
db_name = os.getenv('MYSQL_DATABASE', 'project_stocks_db')
ticker = "aapl"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")

ticker = ticker.strip().lower()
query = text(f"""
             SELECT Date
            FROM (
                SELECT Date, `Adj Close`, 
                    LAG(`Adj Close`) OVER (ORDER BY Date) AS prev_adj_close
                FROM `{ticker}`
            ) AS subquery
            WHERE (prev_adj_close - `Adj Close`) / `Adj Close` > 0.01;
             """)

# 1. Volatility Analysis Query
volatility_query = text(f"""
    SELECT 
        DATE_FORMAT(Date, '%Y-%m') as month,
        AVG((High - Low)/Low * 100) as avg_daily_volatility,
        MAX((High - Low)/Low * 100) as max_daily_volatility,
        MIN((High - Low)/Low * 100) as min_daily_volatility
    FROM `{ticker}`
    GROUP BY DATE_FORMAT(Date, '%Y-%m')
    ORDER BY month DESC
""")

# 2. Moving Average Crossover Detection
crossover_query = text(f"""
    WITH moving_avgs AS (
        SELECT 
            Date,
            Close,
            AVG(Close) OVER (ORDER BY Date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as MA10,
            AVG(Close) OVER (ORDER BY Date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as MA20
        FROM `{ticker}`
    )
    SELECT 
        Date,
        Close,
        MA10,
        MA20,
        CASE 
            WHEN MA10 > MA20 AND LAG(MA10) OVER (ORDER BY Date) <= LAG(MA20) OVER (ORDER BY Date) 
            THEN 'Golden Cross'
            WHEN MA10 < MA20 AND LAG(MA10) OVER (ORDER BY Date) >= LAG(MA20) OVER (ORDER BY Date) 
            THEN 'Death Cross'
            ELSE NULL
        END as crossover_signal
    FROM moving_avgs
    WHERE crossover_signal IS NOT NULL
""")

# 3. Gap Analysis with Volume Query
gap_analysis_query = text(f"""
    WITH daily_changes AS (
        SELECT 
            Date,
            Open,
            Close,
            Volume,
            LAG(Close) OVER (ORDER BY Date) as prev_close,
            AVG(Volume) OVER (ORDER BY Date ROWS BETWEEN 5 PRECEDING AND 1 PRECEDING) as avg_5day_volume
        FROM `{ticker}`
    )
    SELECT 
        Date,
        ROUND(((Open - prev_close) / prev_close * 100), 2) as gap_percentage,
        Volume,
        ROUND(((Volume - avg_5day_volume) / avg_5day_volume * 100), 2) as volume_change_percentage
    FROM daily_changes
    WHERE ABS((Open - prev_close) / prev_close * 100) > 1
        AND Volume > avg_5day_volume * 1.5
    ORDER BY ABS((Open - prev_close) / prev_close * 100) DESC
""")

# 4. Relative Strength Analysis
relative_strength_query = text(f"""
    WITH price_momentum AS (
        SELECT 
            Date,
            Close,
            LAG(Close, 5) OVER (ORDER BY Date) as price_5_days_ago,
            LAG(Close, 20) OVER (ORDER BY Date) as price_20_days_ago
        FROM `{ticker}`
    )
    SELECT 
        Date,
        Close,
        ROUND(((Close - price_5_days_ago) / price_5_days_ago * 100), 2) as momentum_5_day,
        ROUND(((Close - price_20_days_ago) / price_20_days_ago * 100), 2) as momentum_20_day
    FROM price_momentum
    WHERE price_5_days_ago IS NOT NULL 
        AND price_20_days_ago IS NOT NULL
    ORDER BY Date DESC
""")

# 5. Volume Profile Analysis
volume_profile_query = text(f"""
    SELECT 
        Date,
        Close,
        Volume,
        AVG(Volume) OVER (ORDER BY Date ROWS BETWEEN 20 PRECEDING AND CURRENT ROW) as avg_volume_20d,
        CASE 
            WHEN Volume > 2 * AVG(Volume) OVER (ORDER BY Date ROWS BETWEEN 20 PRECEDING AND CURRENT ROW)
            THEN 'High Volume Alert'
            ELSE 'Normal Volume'
        END as volume_signal
    FROM `{ticker}`
    WHERE Date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    ORDER BY Date DESC
""")

with engine.connect() as connection:
    result = connection.execute(query)
    for row in result:
        print(row)

