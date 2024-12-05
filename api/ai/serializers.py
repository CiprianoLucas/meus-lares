from rest_framework import serializers


class OpenaiChatSerializer(serializers.Serializer):
    message = serializers.CharField()
