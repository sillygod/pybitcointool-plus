from api_manager import *
import logging


class APIFactory(object):

    """an api class factory. According to identifier
    you give, you will get different class.
    """

    _class_dict = {}

    def __new__(cls, name, base, attrs):
        c = type(name, base, attrs)

        if attrs.get('identifier', None):
            APIFactory._class_dict[attrs['identifier']] = c

        return c

    @staticmethod
    def get_class(id):
        return APIFactory._class_dict[id]

    @staticmethod
    def get_all_class():
        return APIFactory._class_dict
