# -*- coding: utf-8 -*-

from alipay import AliPay  # python-alipay-sdk
from django.conf import settings


def my_ali_pay(notify_url=None):
    """
    支付宝支付对象
    :param notify_url:
    支付成功支付宝服务器异步通知默认回调url，会向这个地址发送POST请求，接口实现校验是否支付已经完成，注意：此地址需要能在公网进行访问
    :return: 支付对象
    """
    ali_pay_obj = AliPay(
        appid=settings.ALI_PAY_APP_ID,
        app_notify_url=None,
        app_private_key_string=settings.ALIPAY_PRIVATE_KEY_STRING,
        alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,
        sign_type="RSA2",
    )

    return ali_pay_obj
