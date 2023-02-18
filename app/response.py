from rest_framework.response import Response


class SuccessResponse(Response):
    def __init__(self, *args, **kwargs):
        super(SuccessResponse, self).__init__(*args, **kwargs)
        self.data = {
            'code': 0,
            'message': 'success',
            'data': self.data
        }

    @staticmethod
    def wrap_response(response: Response):
        response.data = {
            'code': 0,
            'message': 'success',
            'data': response.data
        }
        return response


class ErrorResponse(Response):
    def __init__(self, message, *args, **kwargs):
        super(ErrorResponse, self).__init__(*args, **kwargs)
        self.data = {
            'code': 1,
            'message': message,
            'data': self.data
        }

    @staticmethod
    def wrap_response(response: Response, msg: str):
        response.data = {
            'code': 1,
            'message': msg,
            'data': response.data
        }
        return response
