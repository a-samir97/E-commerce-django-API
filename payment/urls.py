from django.urls import path
from . import views
from .payment_response import Payment_Receipt
urlpatterns =[
    # path('payment_rsponse/',views.PaymentResponse.as_view()),
    path('add_shipping/',views.AddShippmentRequest.as_view()),
    path('get_traking/<int:awbNo>/',views.GetTraking.as_view()),
    path('get_pdf/<int:awbNo>/',views.GetPdf.as_view()),
    path('payment_receipt/',Payment_Receipt)
]