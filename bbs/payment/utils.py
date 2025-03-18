# -*- coding: utf-8 -*-
import os

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
        appid=settings.ALIPAY_APPID,
        app_notify_url=notify_url,  # 支付成功支付宝服务器异步通知默认回调url, 即会向这个地址发送POST请求
        app_private_key_path=settings.ALIPAY_PRIVATE_KEY_STRING,
        # 支付宝的公钥，验证支付宝回传消息使用
        alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_STRING,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 是否是沙箱环境, 默认False
    )

    return ali_pay_obj

def redKey(key):
    """
    加密密钥
    :param key:
    :return:
    """
    alipay_client_config = None
    with open(key) as f:
        alipay_client_config.app_private_key = f.read()

    return alipay_client_config