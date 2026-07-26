from urllib import parse
from db_engine import SessionLocal
from service import GetMatch,AddPoints

def HandleMatchScore(environ, start_response, env):
    method = environ.get("REQUEST_METHOD")

    # --- ОБРАБОТКА ФОРМЫ (POST) ---
    if method == "POST":
        content_length = int(environ.get("CONTENT_LENGTH", 0))
        body = environ["wsgi.input"].read(content_length).decode("utf-8")
        form_data = parse.parse_qs(body)

        point_winner = form_data.get("point_winner", [""])[0]
        match_uuid = form_data.get("match_uuid", [""])[0]

        with SessionLocal() as session:
            finished_match_id = AddPoints(session, point_winner, match_uuid)

        if finished_match_id:
            redirect = f'/match-info?uuid={match_uuid}'
        else:
            redirect = f'/match-score?uuid={match_uuid}'

        start_response('303 See Other', [('Location', f'{redirect}')])
        return [b""]

    # --- ОТРИСОВКА СТРАНИЦЫ (GET) ---
    else:
        query_string = environ.get("QUERY_STRING", "")
        params = parse.parse_qs(query_string)

        match_uuid = params.get("uuid", [None])[0]

        with SessionLocal() as session:
            current_match = GetMatch(session, match_uuid)
            player1_score, player2_score, player1_game, player2_game, player1_set, player2_set = current_match.score.replace(
                " ", ":").split(":")

            template = env.get_template("match-score.html")
            rendered_html = template.render(
                page_title="Tennis Scoreboard | Match Score",
                current_match=current_match,
                player1_score=player1_score,
                player2_score=player2_score,
                player1_sets=player1_set,
                player2_sets=player2_set,
                player1_games=player1_game,
                player2_games=player2_game,
            )

        start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])

        return [rendered_html.encode("utf-8")]