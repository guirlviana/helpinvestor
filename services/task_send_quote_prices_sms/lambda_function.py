from django.conf import settings
import requests
import os

def lambda_handler(event, context):
    sns = boto3.client('sns', region_name='us-east-1')
    token = __authenticate_as_admin()
    if not token:
        return {
            'statusCode': 422,
            'body': 'Authentication failed'
        }
    
    notifications = __get_quote_prices_notifications(token)
    if not notifications:
        return {
            'statusCode': 422,
            'body': 'No target quote prices found'
        }
    
    for notification in notifications:
        __send_sms(sns, notification['phone'], notification['message'])


def __send_sms(sns, phone_number, message):
    try:
        response = sns.publish(
            PhoneNumber=phone_number,
            Message=message
        )
        
        return {
            'statusCode': 200,
            'body': 'SMS sent successfully!',
            'messageId': response['MessageId']
        }
    except Exception as e:
        print("Error sending SMS:", str(e))
        return {
            'statusCode': 500,
            'body': 'Error sending SMS'
        }


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
