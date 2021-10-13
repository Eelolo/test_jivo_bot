from django.http import HttpResponse
from django.views.generic.base import View
from rest_framework.views import APIView
from django.shortcuts import render


class IndexPageView(View):
    def get(self, request):
        return render(request, "index.html")


class DataFromJivoView(APIView):
    def post(self, request):
        print(request)
