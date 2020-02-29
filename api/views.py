from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from api import models
from api.utils.permission import MyPermission1
from api.utils.throttle import VisitThrottle
import time
import json

"""
认证 authentication_classes
权限 permission_classes
节流（访问频率） throttle_classes
"""


def md5(user):
    import hashlib
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    """登录类"""
    authentication_classes = []
    permission_classes = []
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = "用户名或密码错误"
            # 为登录用户创建token
            token = md5(user)
            # 存在就更新，不存在就创建
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)


ORDER_DICT = {
    'name': 'aa',
    'age': 18,
}


class OrderView(APIView):
    """只有SVIP可以访问"""

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None, 'data': None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)


class UserInfo(APIView):
    permission_classes = [MyPermission1, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None, 'data': None}
        return JsonResponse(ret)


class UsersView(APIView):

    def get(self, request, *args, **kwargs):
        """
        获取版本
        request.version
        反向获取url
        u1 = request.versioning_scheme.reverse(viewname="uuu", request=request)
        """
        return HttpResponse('用户列表')


class ParserView(APIView):
    # parser_classes = [JSONParser,FormParser,]
    """
    JSONParser:表示只能解析content-type:application/json头
    JSONParser:表示只能解析content-type:application/x-www-form-urlencoded头
    """

    def post(self, request, *args, **kwargs):
        """
        允许用户发送JSON格式数据
        a. content-type: application/json
        b. {'name':'alex',age:18}
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """
        1. 获取用户请求
        2. 获取用户请求体
        3. 根据用户请求头 和 parser_classes = [JSONParser,FormParser,] 中支持的请求头进行比较
        4. JSONParser对象去请求体
        5. request.data
        """
        print(type(request.data))
        return HttpResponse('ParserView')


from rest_framework import serializers

from api.utils.serializers.Roles import RolesSerializer


class RolesView(APIView):
    # 获取角色，采用get方法得到所有的
    def get(self, request, *args, **kwargs):
        # 方式一：
        # roles = models.Role.objects.all().values('id', 'title')
        # ret = json.dumps(list(roles), ensure_ascii=False)  # ensure_ascii=False 不改变中文编码
        # return HttpResponse(ret)

        # 方式二：
        roles = models.Role.objects.all()
        ser = RolesSerializer(instance=roles, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class MyField(serializers.CharField):
    """自定义CharField"""

    def to_representation(self, value):
        print(value)
        return "xxxxx"


# class UserInfoSerializer(serializers.ModelSerializer):
#     oooo = serializers.CharField(source="get_user_type_display")  # row.user_type
#     rls = serializers.SerializerMethodField()  # 自定义显示
#     x1 = MyField(source='username') # 使用自定义CharField
#
#     class Meta:
#         model = models.UserInfo
#         # fields = "__all__"
#         fields = ['id','username','password','oooo','rls','group','x1']
#
#     def get_rls(self, row):
#         role_obj_list = row.roles.all()
#
#         ret = []
#         for item in role_obj_list:
#             ret.append({'id':item.id,'title':item.title})
#         return ret

# class UserInfoSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#     xxx = serializers.CharField(source="user_type")  # source为指定具体哪个字段，xxx为指定显示名称，如果不加source就需要和数据库名字统一
#     ooo = serializers.CharField(source="get_user_type_display")  # choices
#     gp = serializers.CharField(source="group.title")  # ForeignKey
#     rls = serializers.SerializerMethodField()  # ManyToManyField 需使用自定义函数
#
#     def get_rls(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({'id': item.id, 'title': item.title})
#         return ret


from api.utils.serializers.userInfo import UserInfoSerializer


class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=users, many=True, context={'request': request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


###获取group###
from api.utils.serializers.group import GroupSerializer


class GroupView(APIView):
    # 获取组名信息等
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('xxx')
        obj = models.UserGroup.objects.filter(pk=pk).first()

        ser = GroupSerializer(instance=obj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


# #################### 验证 ############################
from api.utils.serializers.userGroup import UserGroupSerializer


class UserGroupView(APIView):

    def post(self, request, *args, **kwargs):

        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data['title'])
        else:
            print(ser.errors)

        return HttpResponse('提交数据')


# #################  分页 #################

from api.utils.serializers.pager import PagerSerialiser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class MyPageNumberPagination(PageNumberPagination):
    """PageNumberPagination 分页方法"""
    page_size = 2
    page_size_query_param = 'size'  # 指定页面大小
    max_page_size = 5
    page_query_param = 'page'  # 查询第几页的意思


class MyLimitOffsetPagination(LimitOffsetPagination):
    """LimitOffsetPagination分页方法"""
    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 5


class MyCursorPagination(CursorPagination):
    """使用加密分页，使用时必须要加get_paginated_response方法进行调用"""
    cursor_query_param = 'cursor'
    page_size = 2
    ordering = 'id'
    page_size_query_param = None
    max_page_size = None


class PageView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()

        # 创建分页对象
        # pg = PageNumberPagination()
        # pg = MyLimitOffsetPagination()
        pg = MyCursorPagination()

        # 在数据库中获取分页的数据
        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)

        # 对数据进行序列化
        ser = PagerSerialiser(instance=pager_roles, many=True)

        # return Response(ser.data)  # Response可以优化视图
        return pg.get_paginated_response(ser.data)  # 结果显示count，next，previous字段


from rest_framework.viewsets import ModelViewSet


class View1View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerialiser
    pagination_class = PageNumberPagination
