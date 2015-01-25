import sys
from exceptions import APIException


py_version = sys.version_info.major

if py_version >= 3:
    from urllib.request import urlopen
    from urllib.error import HTTPError
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib import urlencode


def satoshi_to_btc(value):
    return float(value) / 10**8


def btc_to_satoshi(value):
    return value * 10**8


def compat_response(response):
    '''In python 3, it will return a byte object
    not return a string. so here, we handle for it
    '''
    if isinstance(response, str):
        return response
    else:
        return response.decode('utf-8')


def call_api(base_url, resource, data=None):
    '''an simple encapsulation for request a rest api
    '''
    try:
        payload = urlencode(data) if data else None

        if py_version >= 3 and payload is not None:
            payload = payload.encode('utf-8')

        response = urlopen(base_url+resource, payload, timeout=10).read()

        return compat_response(response)

    except HTTPError as e:
        raise APIException(compat_response(e.read()), e.code)
