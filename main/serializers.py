from . import models
from rest_framework import serializers


class ParseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ParseModel
        fields = ['title', 'url']


class HtmlPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HtmlPage
        fields = ['text']
