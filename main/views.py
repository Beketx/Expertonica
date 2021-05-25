from rest_framework.response import Response
from rest_framework.views import APIView

from utils.divan import Client
from . import models
from . import serializers

parser = Client()


class MainPageView(APIView):

    def get(self, request):
        parser.run()
        queryset = models.HtmlPage.objects.all()
        serializer = serializers.HtmlPageSerializer(queryset,
                                                    many=True)
        return Response(serializer.data)


class ObjectsView(APIView):

    def get(self, request):
        parser.run()
        queryset = models.ParseModel.objects.all()
        serializer = serializers.ParseSerializer(queryset,
                                                 many=True)
        return Response(serializer.data)
