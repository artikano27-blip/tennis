# Импортируй свои настройки базы и модель (названия могут немного отличаться в твоем проекте)
from db_engine import SessionLocal
from models import Match,Player


def clean_database():
    with SessionLocal() as session:
        # Находим все записи в таблице Match и удаляем их из сессии
        session.query(Player).delete()

        session.commit()

        print("Все старые матчи успешно удалены из базы!")


if __name__ == "__main__":
    clean_database()