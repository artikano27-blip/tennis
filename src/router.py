import mimetypes
from jinja2 import Environment, FileSystemLoader

from controllers.new_match import HandleNewMatch
from controllers.matches import HandleMatches
from controllers.match_info import HandleMatchInfo
from controllers.match_score import HandleMatchScore

env = Environment(loader=FileSystemLoader("templates"))

def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ.get('PATH_INFO', '')

    # Проверяем, начинается ли путь с /static/
    if method == "GET" and path.startswith(("/static/", "/js/", "/images/", "/favicon.ico")):
        import os
        file_path = os.path.join(path.lstrip("/"))

        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Угадываем тип файла по его пути/расширению
            guessed_type, _ = mimetypes.guess_type(file_path)

            # Если Питон вдруг не узнал файл, отдаем базовый бинарный тип
            mime_type = guessed_type or 'application/octet-stream'

            with open(file_path, "rb") as f:
                file_content = f.read()

            # ВАЖНО: говорим браузеру, что это именно CSS код, а не просто текст
            start_response('200 OK', [('Content-type', f'{mime_type}; charset=utf-8')])
            return [file_content]
        else:
            start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
            return [b"Static File Not Found"]


    elif method == "GET" and path == "/":
        start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])

        template = env.get_template("index.html")
        rendered_html = template.render(page_title="Tennis Scoreboard | Home")
        return [rendered_html.encode("utf-8")]


    elif path == "/new-match":
        return HandleNewMatch(environ, start_response, env)

    elif path == "/match-score":
        return HandleMatchScore(environ, start_response, env)

    elif path == "/match-info":
        return HandleMatchInfo(environ, start_response, env)

    elif path == "/matches":
        return HandleMatches(environ,start_response,env)
