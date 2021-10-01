import requests

from app import config


def send_mail(
        to, subject=None, content=None, template=None, template_args=None
):
    if template:
        with open(f'./templates/{template}') as f:
            content = f.read()
        content.replace(**template_args)
    return requests.post(
        config.SENDGRID_API_URL,
        headers={'Authorization': f'Bearer {config.SENDGRID_API_KEY}'},
        json={
            'personalizations': [{'to': [{'email': to}]}],
            'from': {'email': config.SENDGRID_SENDER_EMAIL},
            'subject': f'[ORGANIA] {subject or "Message"}',
            'content': [{'type': 'text/plain', 'value': content}],
        },
    )


def test():
    result = send_mail(
        to='damien.savatier@epitech.eu',
        subject='testitesto',
        content='This is some quality content',
    )
    print(result)
    print(result.content)
