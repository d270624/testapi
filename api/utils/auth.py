from rest_framework import exceptions
from api import models


class Authtication(object):
    """用户认证类"""

    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户验证失败')
        return token, token_obj

    def authenticate_header(self, request):
        """认证失败浏览器返回的响应头"""
        return 'Basic realm="api"'
