
from urllib import parse
from db_engine import SessionLocal
from service import GetMatch

def HandleMatchInfo(environ, start_response, env):
    method = environ.get("REQUEST_METHOD")

    # --- ОБРАБОТКА ФОРМЫ (POST) ---
    if method == "GET":
        query_string = environ.get("QUERY_STRING", "")
        params = parse.parse_qs(query_string)
        match_uuid = params.get("uuid", [None])[0]

        with SessionLocal() as session:
            finished_match = GetMatch(session, match_uuid)
            player1_set, player2_set = finished_match.score.split(" ")[2].split(":")
            if finished_match:
                start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
                template = env.get_template("match-info.html")
                rendered_html = template.render(page_title="Tennis Scoreboard | Finished Match",
                                                match_info=finished_match,
                                                player1_sets=player1_set,
                                                player2_sets=player2_set,
                                                )
        return [rendered_html.encode("utf-8")]
