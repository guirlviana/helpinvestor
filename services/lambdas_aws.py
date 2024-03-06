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

    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{settings.APP_URL}/get-share-prices/', headers=headers)
    notifications = response['response']
    if not notifications:
        return
    
    for notification in notifications:
        __mock_send_sms(notification['phone'], notification['message'])


def __mock_send_sms(phone, message):
    print(f'To: {phone}. message: {message}')
