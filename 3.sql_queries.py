from sqlalchemy import create_engine, text

user = "root"
password = "password"
host = "localhost"
database = "project_stocks_db"
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

query = text("""
             SELECT Date
            FROM (
                SELECT Date, `Adj Close`, 
                    LAG(`Adj Close`) OVER (ORDER BY Date) AS prev_adj_close
                FROM msft
            ) AS subquery
            WHERE (prev_adj_close - `Adj Close`) / `Adj Close` > 0.01;
             """)

with engine.connect() as connection:
    result = connection.execute(query)
    for row in result:
        print(row)