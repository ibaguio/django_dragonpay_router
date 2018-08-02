import logging
import requests

from django.views import generic
from django.conf import settings
from django.http.response import HttpResponse

logger = logging.getLogger('django_dragonpay_router')


class BaseCallbackHandler(generic.View):
    URL_POSTFIX = ''

    def dispatch(self, request, *args, **kwargs):
        payload = getattr(request, request.method)
        txnid = payload.get(self.TXNID_PARAM)

        def _fail_transaction(msg):
            # log invalid transaction
            logger.debug(
                '[%s]. %s Transaction payload: %s',
                msg, request.method, payload)

            return HttpResponse('Invalid request ' + msg, status=400)

        def _forward_request(dst, request):
            logger.debug(
                'Forwarding %s request to [%s] %s. payload: %s',
                request.method, appname, dst, payload.dict())

            if request.method == 'GET':
                requests.get(dst, param=payload.dict())

            elif request.method == 'POST':
                requests.post(dst, data=payload.dict())

        # code validations
        if not txnid:
            return _fail_transaction('missing %s' % self.TXNID_PARAM)

        try:
            # get the appname from the txnid
            appname, _txnid = txnid.split('_')
        except:
            return _fail_transaction('%s has no prefix' % self.TXNID_PARAM)

        # check if appname is in our routes
        if appname in settings.DRAGONPAY_ROUTES:
            _forward_request(
                settings.DRAGONPAY_ROUTES[appname] + self.URL_POSTFIX, request)

            return HttpResponse(
                'Request forwarded to %s' % settings.DRAGONPAY_ROUTES[appname])
        else:
            logger.error('%s is not a registered route.', appname)

            return _fail_transaction('%s is not a registered application' % appname)


class DragonpayCallback(BaseCallbackHandler):
    TXNID_PARAM = 'txnid'

    def get(self, request):
        pass

    def post(self, request):
        pass


class DragonpayPayoutCallback(BaseCallbackHandler):
    URL_POSTFIX = 'payout/'
    TXNID_PARAM = 'merchanttxnid'

    def get(self, request):
        pass
