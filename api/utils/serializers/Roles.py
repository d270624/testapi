from rest_framework import serializers


class RolesSerializer(serializers.Serializer):
    title = serializers.CharField()
    id = serializers.IntegerField()
