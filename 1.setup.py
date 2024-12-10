from sqlalchemy import create_engine, text

DB_URL = "mysql+pymysql://root:password@localhost"
DB_NAME = "project_stocks_db"

engine = create_engine(DB_URL, echo=True)

with engine.connect() as conn:
    result = conn.execute(text(f"SHOW DATABASES LIKE '{DB_NAME}';")).fetchone()
    if result:
        print(f"Database '{DB_NAME}' exists. Dropping it...")
        conn.execute(text(f"DROP DATABASE `{DB_NAME}`;"))
    else:
        print(f"Database '{DB_NAME}' does not exist.")

    print(f"Creating database '{DB_NAME}'...")
    conn.execute(text(f"CREATE DATABASE `{DB_NAME}`;"))
    print(f"Database '{DB_NAME}' created successfully!")