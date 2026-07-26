import math
from urllib import parse
from db_engine import SessionLocal
from service import GetPageMatches, CountAllMatches


def HandleMatches(environ, start_response, env):
    method = environ.get("REQUEST_METHOD")

    if method == "GET":
        start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])

        query_string = environ.get("QUERY_STRING", "")
        params = parse.parse_qs(query_string)

        current_page = int(params.get("page", ["1"])[0])
        filter_by_name = params.get("filter_by_player_name", [""])[0]

        with SessionLocal() as session:
            page_matches = GetPageMatches(session, current_page, filter_by_name)
            count_matches = CountAllMatches(session, filter_by_name)
            total_pages = math.ceil(count_matches / 5)

            template = env.get_template("matches.html")
            rendered_html = template.render(
                page_title="Tennis Scoreboard | Finished Matches",
                page_matches=page_matches,
                total_pages=total_pages,
                current_page=current_page,
                count_matches=count_matches,
                filter_by_name=filter_by_name
            )

        return [rendered_html.encode("utf-8")]