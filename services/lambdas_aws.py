from django.conf import settings
import requests
import os

def task_send_quotes_in_sms():
    token = __authenticate_as_admin()
    if not token:
        return

    notifications = __get_quote_prices_notifications(token)
    if not notifications:
        return
    
    for notification in notifications:
        __mock_send_sms(notification['phone'], notification['message'])


def __authenticate_as_admin():
    response = requests.post(f'{settings.APP_URL}/api-token-auth/', {
        "username": os.environ.get('ADMIN_EMAIL'),
        "password": os.environ.get('ADMIN_PASSWORD')
    })
    
    if response.status_code != 200:
        return None
    
    response = response.json()
    return response['token']


def __get_quote_prices_notifications(token):
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{settings.APP_URL}/get-share-prices/', headers=headers)
    if response.status_code != 200:
        return None
    return response['response']


def __mock_send_sms(phone, message):
    print(f'To: {phone}. message: {message}')
