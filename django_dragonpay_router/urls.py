from django.conf.urls import url
from django_dragonpay_router import views

urlpatterns = [
    url(r'^dragonpay/7ea5b0130f888ac648effcb56799c643/payout/?$',
        views.DragonpayPayoutCallback.as_view(), name='dragonpay_callback_payout'),
    url(r'^dragonpay/7ea5b0130f888ac648effcb56799c643/?$',
        views.DragonpayCallback.as_view(), name='dragonpay_callback'),
]
