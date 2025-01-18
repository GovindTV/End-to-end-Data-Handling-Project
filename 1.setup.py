from sqlalchemy import create_engine, text
from setup.config import user,password,host,DB_NAME

DB_URL = "mysql+pymysql://{user}:{password}@{host}"

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