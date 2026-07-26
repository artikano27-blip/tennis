import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service import StartMatch
# Импортируем твои модели и функцию, которую будем тестировать
from src.models import Base, Player, Match
from src.service import AddPoints


@pytest.fixture
def temp_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Сначала сохраняем игроков, чтобы у них появились ID
    player1 = Player(name="Иван")
    player2 = Player(name="Петр")
    session.add_all([player1, player2])
    session.commit()

    # 2. Теперь создаем матч с готовыми ID
    match1 = StartMatch(session, player1.id, player2.id)

    yield session  # Отдаем сессию в тестовую функцию

    session.close()  # Завершаем работу сессии после теста

def test_win_game_at_40_0(temp_session):
    match = temp_session.query(Match).first()
    match.score = "40:0 0:0 0:0"
    temp_session.commit()

    AddPoints(temp_session, match.player1_id, match.uuid)
    temp_session.refresh(match)
    assert match.score == "0:0 1:0 0:0"

def test_pass_game_at_40_40(temp_session):
    match = temp_session.query(Match).first()
    match.score = "40:40 0:0 0:0"
    temp_session.commit()

    AddPoints(temp_session, match.player1_id, match.uuid)
    temp_session.refresh(match)
    assert match.score == "AD:40 0:0 0:0"

def test_win_game_on_tie_break(temp_session):
    match = temp_session.query(Match).first()
    match.score = "6:2 6:6 0:0"
    temp_session.commit()

    AddPoints(temp_session, match.player1_id, match.uuid)
    temp_session.refresh(match)
    assert match.score == "0:0 0:0 1:0"

def test_comeback_game_at_AD_40(temp_session):
    match = temp_session.query(Match).first()
    match.score = "AD:40 0:0 0:0"
    temp_session.commit()

    AddPoints(temp_session, match.player2_id, match.uuid)
    temp_session.refresh(match)
    assert match.score == "40:40 0:0 0:0"

def test_win_game_at_2_0(temp_session):
    match = temp_session.query(Match).first()
    match.score = "AD:40 5:0 1:0"
    temp_session.commit()

    AddPoints(temp_session, match.player1_id, match.uuid)
    temp_session.refresh(match)
    assert match.score == "0:0 0:0 2:0"
