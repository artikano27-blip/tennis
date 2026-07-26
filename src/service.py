from uuid import uuid4

from models import Player, Match
from sqlalchemy.exc import IntegrityError


def AddPlayer(session, player_name):
    new_player = Player(name=player_name)

    try:
        session.add(new_player)
        session.commit()

        return new_player.id

    except IntegrityError:
        session.rollback()
        exist_player = session.query(Player).filter(Player.name == player_name).first()

        return exist_player.id

def GetPlayer(session, player_id):
    player = session.query(Player).filter_by(id=player_id).first()
    return player


def StartMatch(session,player1_id, player2_id):
    match_uuid = str(uuid4())

    new_match = Match(uuid=match_uuid,
                      player1_id=player1_id,
                      player2_id=player2_id,
                      winner_id=None,
                      score="0:0 0:0 0:0"
                      )
    session.add(new_match)
    session.commit()
    return new_match.uuid

def GetMatch(session,match_uuid):
    match = session.query(Match).filter_by(uuid=match_uuid).first()
    return match

def AddPoints(session, player_id, match_uuid):
    match = GetMatch(session, match_uuid)

    player1_score, player2_score, player1_game_str, player2_game_str, player1_set_str, player2_set_str = match.score.replace(" ", ":").split(":")
    player1_game = int(player1_game_str)
    player2_game = int(player2_game_str)
    player1_set = int(player1_set_str)
    player2_set = int(player2_set_str)
    score_winner_id = int(player_id)
    is_tie_break = (player1_game == 6 and player2_game == 6)
    tennis_points = ["0", "15", "30", "40" ]


    if match.winner_id is None:
        if is_tie_break:
            player1_score = int(player1_score)
            player2_score = int(player2_score)

            if score_winner_id == match.player1_id:
                player1_score+=1

                if player1_score >=7 and player1_score - player2_score>=2:
                    player1_score = 0
                    player2_score = 0
                    player1_game = 0
                    player2_game = 0
                    player1_set +=1
                    if player1_set == 2:
                        match.winner_id = match.player1_id

            elif score_winner_id == match.player2_id:
                player2_score += 1

                if player2_score >= 7 and player2_score - player1_score >= 2:
                    player1_score = 0
                    player2_score = 0
                    player1_game = 0
                    player2_game = 0
                    player2_set += 1
                    if player2_set == 2:
                        match.winner_id = match.player2_id

        else:
            if score_winner_id == match.player1_id:

                if player1_score == "AD" or (player1_score == "40" and player2_score in ["0", "15", "30"]):
                    player1_score = "0"
                    player2_score = "0"
                    player1_game +=1
                    if player1_game >= 6 and player1_game - player2_game >= 2:
                        player1_game = 0
                        player2_game = 0
                        player1_set +=1
                        if player1_set == 2:
                            match.winner_id = match.player1_id
                elif player1_score == "40" and player2_score == "40":
                    player1_score = "AD"
                elif player2_score == "AD":
                    player2_score = "40"
                else:
                    player1_points = tennis_points.index(player1_score)
                    p1_next_index = player1_points + 1
                    player1_score = tennis_points[p1_next_index]

            elif score_winner_id == match.player2_id:

                if player2_score == "AD" or (player2_score == "40" and player1_score in ["0", "15", "30"]):
                    player1_score = "0"
                    player2_score = "0"
                    player2_game +=1
                    if player2_game >= 6 and player2_game - player1_game >= 2:
                        player1_game = 0
                        player2_game = 0
                        player2_set +=1
                        if player2_set == 2:
                            match.winner_id = match.player2_id

                elif player1_score == "40" and player2_score == "40":
                    player2_score = "AD"
                elif player1_score == "AD":
                    player1_score = "40"
                else:
                    player2_points = tennis_points.index(player2_score)
                    p2_next_index = player2_points + 1
                    player2_score = tennis_points[p2_next_index]

        result_score = f"{player1_score}:{player2_score} {player1_game}:{player2_game} {player1_set}:{player2_set}"
        match.score = result_score
        session.add(match)
        session.commit()

        if match.winner_id is not None:
            return match_uuid

def GetPageMatches(session,current_page,filter):
    query = session.query(Match).filter(Match.winner_id.isnot(None))

    if filter:
        query = query.filter(Match.winner.has(name=filter))

    return query.order_by(Match.id.desc()).limit(5).offset((current_page-1) * 5)

def CountAllMatches(session,filter):
    query = session.query(Match).filter(Match.winner_id.isnot(None))

    if filter:
        query = query.filter(Match.winner.has(name=filter))

    return query.count()


