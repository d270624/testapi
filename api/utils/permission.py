class SVIPPermission(object):
    message = '必须是SVIP才可能访问'

    def has_permission(self, request, view):
        # request.auth.user.user_type 获取用户权限
        if request.auth.user.user_type != 3:
            return False
        return True


class MyPermission1(object):
    message = '必须是SVIP才可能访问'

    def has_permission(self, request, view):
        # request.auth.user.user_type 获取用户权限
        if request.auth.user.user_type != 3:
            return False
        return True
