from faker import Faker
import psycopg2
import random

fake = Faker()
num_rows = 10000  # ← 필요 시 더 늘려도 OK

conn = psycopg2.connect(
    dbname="dummydb",
    user="postgres",         
    password="5117", 
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 테이블 생성
cur.execute("DROP TABLE IF EXISTS employees")
cur.execute("""
    CREATE TABLE employees (
        id SERIAL PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary INTEGER,
        hire_date DATE
    )
""")

departments = ['Engineering', 'Marketing', 'HR', 'Sales', 'Product']

for _ in range(num_rows):
    name = fake.name()
    dept = random.choice(departments)
    salary = random.randint(40000, 120000)
    hire_date = fake.date_between(start_date='-10y', end_date='today')
    cur.execute(
        "INSERT INTO employees (name, department, salary, hire_date) VALUES (%s, %s, %s, %s)",
        (name, dept, salary, hire_date)
    )

conn.commit()
conn.close()
print(f"✅ {num_rows} rows inserted into 'employees' table in dummydb.")
