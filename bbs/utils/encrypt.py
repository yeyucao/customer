import hashlib

from django.conf import settings


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))

    return obj.hexdigest()


if __name__ == '__main__':
    print(md5('123456'))