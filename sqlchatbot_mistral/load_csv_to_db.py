import sqlite3
import pandas as pd

# CSV 파일 경로와 DB 파일 경로 설정
csv_file_path = '국민건강보험공단_건강검진정보_2023.CSV'
db_file_path = 'sample.db'

# SQLite DB에 연결 (파일이 없으면 새로 생성)
conn = sqlite3.connect(db_file_path)

# Pandas를 사용하여 CSV 파일을 읽고 DB에 저장
try:
    df = pd.read_csv(csv_file_path, encoding='cp949')
    df.to_sql('건강검진정보', conn, if_exists='replace', index=False)
    print(f"'{csv_file_path}' 파일이 '{db_file_path}'의 '건강검진정보' 테이블로 성공적으로 저장되었습니다.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
finally:
    conn.close()