from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from . import secrets

import hashlib, json, requests

TERMINAL_ID = secrets.TERMINAL_ID
PASSWORD = secrets.PASSWORD
MERCHANT_SECRET_KEY= secrets.MERCHANT_SECRET_KEY
ACTION = secrets.ACTION
CURRENCY = secrets.CURRENCY
COUNTRY = secrets.COUNTRY

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class PaymentRequest(APIView):

    def post(self, request):
        
        if not request.data.get('price') and not request.data.get('id'):
            return Response(
                {'error': 'please enter price and card id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        price = str(request.data['price'])
        card_id = str(request.data['id'])
        ip_address = get_client_ip(request)

        posted={
            'terminalId': TERMINAL_ID,
            'password': PASSWORD,
            'secret': MERCHANT_SECRET_KEY,
            'currency': CURRENCY,
            'country': COUNTRY,
            'action': ACTION,
            'trackid': card_id,
            'customerEmail': request.user.email,
            'merchantIp': ip_address,
            'amount': price
        }
        hashSequence = posted["trackid"]+"|"+posted["terminalId"]+"|"+posted["password"]+"|"+posted["secret"]+"|"+posted["amount"]+"|"+posted["currency"]
        hashVarsSeq=hashSequence.split('|')

        hash=hashlib.sha256(hashSequence.encode()).hexdigest()
        posted["requestHash"]=hash
        name=json.dumps(posted)
        apiURL = 'https://payments.urway-tech.com/URWAYPGService/transaction/jsonProcess/JSONrequest'
        response=requests.request("POST",apiURL,data=name)
        res=json.loads(response.text)
        
        targetURL=json.dumps(res["targetUrl"]).replace('test-vegaah.concertosoft.com','10.10.10.101')+"?paymentid="
        pymentID=json.dumps(res["payid"])
        redirectURL=(targetURL+pymentID).replace('"','')
        
        if 'null' in redirectURL:
            return Response(
                {'error': 'there is something wrong, please try again'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'payment_url': redirectURL},
            status=status.HTTP_200_OK
            )
