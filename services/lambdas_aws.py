from django.conf import settings
import requests
import os

def task_send_quotes_in_sms():
    response = requests.post(f'{settings.APP_URL}/api-token-auth/', {
        "username": os.environ.get('ADMIN_EMAIL'),
        "password": os.environ.get('ADMIN_PASSWORD')
    })

    if response.status_code != 200:
        return response
    
    response = response.json()
    token = response['token']
