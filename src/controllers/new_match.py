from urllib import parse
from db_engine import SessionLocal
from service import AddPlayer,StartMatch

def HandleNewMatch(environ, start_response, env):
    method = environ.get("REQUEST_METHOD")

    # --- ОБРАБОТКА ФОРМЫ (POST) ---
    if method == "POST":
        content_length = int(environ.get("CONTENT_LENGTH", 0))
        body = environ["wsgi.input"].read(content_length).decode("utf-8")
        form_data = parse.parse_qs(body)

        player_one = form_data.get("player1", [""])[0]
        player_two = form_data.get("player2", [""])[0]

        with SessionLocal() as session:
            player1 = AddPlayer(session, player_one)
            player2 = AddPlayer(session, player_two)
            match_uuid = StartMatch(session, player1, player2)

        start_response('303 See Other', [('Location', f'/match-score?uuid={match_uuid}')])
        return [b""]

    # --- ОТРИСОВКА СТРАНИЦЫ (GET) ---
    else:
        start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])

        template = env.get_template("new-match.html")
        rendered_html = template.render(page_title="Tennis Scoreboard | New Match")

        return [rendered_html.encode("utf-8")]