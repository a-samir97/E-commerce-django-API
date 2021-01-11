from rest_framework.views import exception_handler
import requests

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        customized_response = {}
        customized_response['error'] = []

        for key, value in response.data.items():
            error = {key: value}
            customized_response['error'].append(error)

        response.data = customized_response

    return response

USERNAME = 'msawmhttp'
PASSWORD = 'phqls6421PHQ'

async def send_single_message(user, text):
    BASE_URL = 'https://meapi.myvaluefirst.com/smpp/sendsms?username=%s&password=%s&to=%s&from=MSAWM&coding=3&text=%s' % (
        USERNAME, PASSWORD, user.phone_number, text
    )
    response = requests.get(BASE_URL)

async def send_sms_messages(following_users):


    # get phone_number 
    phone_numbers = []

    for user in following_users:
        phone_numbers.append(user.phone_number)
    
    PHONES = ','.join(phone_numbers)

    TEXT = 'ساوم معنا عن طريق التطبيق الخاص بنا'

    BASE_URL = 'https://meapi.myvaluefirst.com/smpp/sendsms?username=%s&password=%s&to=%s&from=MSAWM&category=bulk&coding=3&text=%s' % (
        USERNAME, PASSWORD, PHONES, TEXT
    )
    response = requests.get(BASE_URL)