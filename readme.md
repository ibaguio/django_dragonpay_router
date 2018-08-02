# Django DragonPay Router

A basic django application that routes dragonpay requests to internal applications depending on the prefix of the transction id (`txnid` or `merchanttxnid`). This app is useful to if you want to utilize a DragonPay subscription across multiple applications.

Please see [django_dragonpay](https://github.com/ibaguio/django_dragonpay) to utilize DragonPay as a payment channel for django projects.


### Installation and configuration

Deploy as a stand alone application using gunicorn.

Configure the routes by adding the environment variable `DRAGONPAY_ROUTE_ROUTEKEY` where `ROUTEKEY` is the string to be matched in `DRAGONPAY_TXNID_PREFIX` of the DragonPay request. See configuration of django_dragonpay to know more about transaction prefix

Consider two applications, `APP_A` and `APP_B`, running on the same machine with the following parameters:

| Field        | App_A        | App_B |
| :-------------|:-------------| :---- |
| App Name / identifier | myapp | otherapp |
| DRAGONPAY\_TXNID\_PREFIX | myapp | otherapp |
| Endpoint URL | http://localhost:8001/myapp/dp/ | http://localhost:8002/otherapp/dp/ |

The following env vars would be the proper configuration of `django_dragonpay_router`

| Environmental Variable | Value |
| :-------------|:-------------|
| DRAGONPAY\_ROUTE\_MYAPP | http://localhost:8001/myapp/dp/ 
| DRAGONPAY\_ROUTE\_OTHERAPP | http://localhost:8002/otherapp/dp/ |


### Sample DragonPay transaction request

### Notes
- Make sure that all apps has a configured `DRAGONPAY_TXNID_PREFIX`, by default there is no txnid prefix, so this must be explicitly set.
- Make sure that endpoint urls of applications are accessible from the `django_dragonpay_router` application.

