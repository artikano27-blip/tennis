import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()
db_password = os.getenv("DB_PASSWORD")
DATABASE_URL = f"mysql+pymysql://tennis_user:secure_password@localhost/tennis_db"

# Создаем движок (подключение) ОДИН раз
engine = create_engine(url = DATABASE_URL
                       )

# Создаем фабрику сессий (SessionLocal) ОДИН раз
# Называем с припиской Local, чтобы подчеркнуть, что это локальная сессия для запроса
SessionLocal = sessionmaker(bind=engine)