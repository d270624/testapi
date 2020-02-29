from rest_framework import serializers
from api import models


class UserInfoSerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedIdentityField(view_name='gp',
                                                 lookup_field='group_id', lookup_url_kwarg='xxx')

    class Meta:
        model = models.UserInfo
        fields = "__all__"
        # fields = ['id', 'username', 'password', 'group', 'roles']
        depth = 1  # 0 ~ 10
