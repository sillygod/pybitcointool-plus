class APIException(Exception):

    def __init__(self, message, code):
        super(APIException, self).__init__(self, message)
        self.code = code
