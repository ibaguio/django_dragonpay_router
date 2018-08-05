from django.conf.urls import url
from django.conf import settings
from django_dragonpay_router import views

urlpatterns = [
    url(r'^' + settings.DRAGONPAY_CALLBACK_PAYOUT_URL + '?$',
        views.DragonpayPayoutCallback.as_view(), name='dragonpay_callback_payout'),
    url(r'^' + settings.DRAGONPAY_CALLBACK_URL + '?$',
        views.DragonpayCallback.as_view(), name='dragonpay_callback'),
]
