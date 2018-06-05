from django.utils.deprecation import MiddlewareMixin
from django.http.response import JsonResponse
from django.shortcuts import render


class ParamException(Exception):

    def __init__(self, code=0, message='系统异常，请联系管理员！'):
        self.code = code
        self.message = message

    @staticmethod
    def create_error(message):
        p = ParamException(message=message)
        return p


class CrmMiddleware(MiddlewareMixin):

    # 处理异常机制
    def process_exception(self, request, exception):

        if isinstance(exception, ParamException):
            result = {'code': exception.code, 'message': exception.message}
        else:
            result = {'code': 0, 'message': '系统异常，请联系管理员'}

        # 校验是否是ajax请求
        if request.is_ajax():
            return JsonResponse(result)
        else:
            return render(request, "error.html", result)


# 如果为空报异常
def is_empty(value, code=0, message='系统异常，请联系管理员'):
   if value is None:
       raise ParamException(code, message)