import requests
from django.conf import settings


def make_request(path, access_token=None):
    url = '{}{}'.format(settings.API_SERVER_URL, path)
    if access_token is None:
        headers = {}
    else:
        headers = {
            'authorization': 'Bearer {}'.format(access_token)
        }

    r = requests.get(url, headers=headers)
    return r.json


class MessageService:

    def public_message(self):
        return make_request('/api/messages/public')

    def protected_message(self, access_token):
        return make_request('/api/messages/protected', access_token)

    def admin_message(self, access_token):
        return make_request('/api/messages/admin', access_token)
