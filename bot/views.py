from django.views.generic.base import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import client_chat_logging, deserialize_data
from .logic import Bot


class IndexPageView(View):
    def get(self, request):
        return render(request, "index.html")


@method_decorator((csrf_exempt, client_chat_logging), name='dispatch')
class DataFromJivoView(View):
    http_method_names = ['post']

    def get(self, request):
        return JsonResponse({'message': 'Bot sends POST requests here'})

    def post(self, request):
        data = deserialize_data(request.body)

        # try:
        Bot(data)
        # except:
        #     return JsonResponse({'message': 'Internal server error'}, status=500)

        return JsonResponse({'message': 'ok'}, status=200)
