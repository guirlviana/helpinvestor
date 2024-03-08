import boto3
import requests

ADMIN_EMAIL='pitoco@gmail.com'
ADMIN_PASSWORD='123456'
URL="http://127.0.0.1:8000"

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
    
    return {
        'statusCode': 200,
        'body': 'Everything done!' 
    }


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
    response = requests.post(f'{URL}/api-token-auth/', {
        "username": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })
    
    if response.status_code != 200:
        return None
    
    response = response.json()
    return response['token']


def __get_quote_prices_notifications(token):
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{URL}/get-share-prices/', headers=headers)
    if response.status_code != 200:
        return None
    
    response = response.json()
    return response['response']
