import flask
import requests
from multiprocessing import Process

from app import config, app


def post(*args, url=None):
    msg = ' '.join(str(x) for x in args)
    url = url or config.DISCORD_LOGS
    if not url:
        return
    def f():
        requests.post(url, data={'content': msg})
    Process(target=f, daemon=True).start()


@app.before_request
def log_request():
    msg = (
        f'{flask.request.method} {flask.request.full_path}'
        f'\n```json\n{flask.request.data.decode() or "(empty body)"}\n```'
    )
    post(msg)
