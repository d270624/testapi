from rest_framework import serializers


class XXValidator(object):
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            message = '标题必须以 %s 为开头。' % self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # 执行验证之前调用,serializer_fields是当前字段对象
        pass


class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required': '标题不能为空'}, validators=[XXValidator('老男人'), ])

    def validate_title(self, value):
        from rest_framework import exceptions
        raise exceptions.ValidationError('看你不爽')
        # 设置报错或自定义返回值
        return value
