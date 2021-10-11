import logging
import requests


class WebhookHandler(logging.Handler):
    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url

    def emit(self, record):
        if not self.url:
            return
        if 'urllib' in record.name or 'request' in record.name:
            return
        if record.levelname == 'DEBUG':
            return
        message = record.getMessage()
        if message is None:
            return
        message = f'[{record.levelname}] {message}'
        requests.post(self.url, data={'content': message})
