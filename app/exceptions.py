from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # 在此处补充自定义的异常处理
    error_msg = exc.args[0]
    if response is not None:
        response.data['error'] = error_msg
    return response
