from rest_framework.throttling import BaseThrottle, SimpleRateThrottle


class VisitThrottle(SimpleRateThrottle):
    """匿名用户"""
    scope = "keys"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class UserVisitThrottle(SimpleRateThrottle):
    """登录用户"""
    scope = "Userkeys"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
