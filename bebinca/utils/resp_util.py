class BaseResponse:

    def __init__(self):
        self.status = True
        self.error_code = None
        self.message = None
        self.data = None
