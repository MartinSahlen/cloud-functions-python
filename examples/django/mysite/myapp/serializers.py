from rest_framework import serializers


class DataSerializer(serializers.Serializer):
    objectId = serializers.CharField()
    email = serializers.EmailField()
