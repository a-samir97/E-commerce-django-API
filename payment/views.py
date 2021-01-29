import uuid
import asyncio
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import status , permissions
from rest_framework.views import APIView
# from rest_framework import permissions, status
from utils import send_single_message
from . import secrets , shipping_secrets
from datetime import datetime
import hashlib, json, requests
import urllib.parse as urlparse
from cart.models import Cart
import random
import base64, os
from django.conf import settings


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
        try:
            get_cart = Cart.objects.get(id=request.data.get('id'))
        except:
            return Response(
                {'error': 'cart is not exists'},
                status=status.HTTP_404_NOT_FOUND
            )

        # get_cart.is_ordered = True
        # get_cart.save()
        
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
            'amount': price,
            'udf1' : "Product",
            'udf2':"http://581f6f004c50.ngrok.io/payment/payment_receipt/",
            "udf3" : request.user.id,
        }
        hashSequence = posted["trackid"]+"|"+posted["terminalId"]+"|"+posted["password"]+"|"+posted["secret"]+"|"+posted["amount"]+"|"+posted["currency"]
        hashVarsSeq=hashSequence.split('|')

        hash=hashlib.sha256(hashSequence.encode()).hexdigest()
        posted["requestHash"]=hash
        name=json.dumps(posted)
        apiURL = "https://payments-dev.urway-tech.com/URWAYPGService/transaction/jsonProcess/JSONrequest"
        response=requests.request("POST",apiURL,data=name)
        res = response.json()
        # print(res)
        pymentID = json.dumps(res["payid"])
        target_url = json.dumps(res["targetUrl"])
        redirectURL=(target_url+"?paymentid="+pymentID).replace('"','')
        if 'null' in redirectURL:
            return Response(
                {'error': 'there is something wrong, please try again'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # get_cart.is_ordered = True
        # get_cart.save()
        # cart_items = get_cart.products.all()
        # for item in cart_items:
        #     product = item.product
        #     product.sold_to = request.user
        #     product.save()

        return Response(
            {'payment_url': redirectURL},
            status=status.HTTP_200_OK
            )
    # def handle_payment_redirect(self,request,**kwargs):

class AddShippmentRequest(APIView):

    def post(self,request):

        if not request.data.get('cart_id'):
            return Response(
                {'error': 'please enter card id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            get_cart = Cart.objects.get(id=request.data.get('cart_id'))
        except:
            return Response(
                {'error': 'cart is not exists'},
                status=status.HTTP_404_NOT_FOUND
            )
        cart_id = request.data.get('cart_id')
        products = get_cart.products.all()
        weight = 0
        pcs = 0
        for prod in products:
            weight += prod.product.weight
            pcs += prod.quantity
        ref_number =  random.randint(0,9999)
        # products = request.user.products.all()
        # weight = 0
        # for product in products:
        #     weight += product.weight

        posted_data = {
                    "passkey": shipping_secrets.passkey,
                    "refno": cart_id + ref_number,
                    "sentDate": datetime,
                    "idNo":request.user.id,
                    "cName": request.data.get('customer_name'),
                    "cntry": shipping_secrets.cntry,
                    "cCity": request.data.get('city'),
                    "cZip" : request.data.get('zip'),
                    "cPOBox" : request.data.get('poBox'),
                    "cMobile":request.data.get('mobile'),
                    "cTel1" : request.data.get('tell1'),
                    "cTel2": request.data.get('tell2'),
                    "cAddr1" : request.data.get('address1'),
                    "cAddr2" : request.data.get('address2'),
                    "shipType": request.data.get('ship_type'),
                    "PCs" : pcs,
                    "cEmail": request.data.get('email'),
                    "carrValue":request.data.get('carr_value'),
                    "carrCurr": shipping_secrets.carrCurr,
                    "codAmt": request.data.get('code_amt'),
                    "weight": weight,
                    "itemDesc": request.data.get('item_desc'),
                    "custVal": request.data.get('custom_value'),
                    "custCurr": shipping_secrets.carrCurr,
                    "insrAmt": 0,
                    "insrCurr": shipping_secrets.carrCurr,
                    "sName": shipping_secrets.sName,
                    "sContact": shipping_secrets.sContact,
                    "sAddr1": shipping_secrets.sAddr1,
                    "sAddr2": shipping_secrets.sAddr2,
                    "sCity": shipping_secrets.sCity,
                    "sPhone": shipping_secrets.sPhone,
                    "sCntry": shipping_secrets.sCntry,
                    "prefDelvDate" : request.data.get('date'),
                    "gpsPoints" : shipping_secrets.gpsPoints
                    }
        api_url = 'https://track.smsaexpress.com/SecomRestWebApi/api/addship'
        response = requests.post(api_url,data=posted_data)
        if 'Message' and 'ExceptionMessage' in response.json():
            return Response(response.json())
        else:
            message = f'your Awb No For Tracking The Shippement is: {response.json()} Please Save it To Use For Getting Pdf file and Tracking your request.'
            asyncio.run(send_single_message(request.user, message))
            print(response.json())
            return Response({"awb":response.json()},status=status.HTTP_200_OK)

class GetTraking(APIView):

    def get(self,request,awbNo):
        passkey =shipping_secrets.passkey
        awbNo = awbNo
        response = requests.get('https://track.smsaexpress.com/SecomRestWebApi/api/getTracking',params={'awbNo' : awbNo,'passkey' : passkey})
        return Response(response.json())

class GetPdf(APIView):
    def get(self,request,awbNo):
        payload = {
            'passkey' : shipping_secrets.passkey,
            'awbno' : awbNo
        }
        response = requests.get('https://track.smsaexpress.com/SecomRestWebApi/api/getPDF',params=payload)
        pdf = response.json()
        news_path = os.path.join(os.path.join(settings.BASE_DIR, 'media'), 'pdf')
        print(news_path)
        file_name = str(uuid.uuid4())[:12]
        complete_file_name = "%s.pdf" % (file_name)
        pdf = base64.b64decode(pdf)
        try:
            with open(f'{news_path}/{complete_file_name}', 'wb') as fout:
                fout.write(pdf)
                return Response({"invoice":f'{news_path}/{complete_file_name}'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'{e}. Invalid pdf file data')
        # return Response(news_path)