from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import client_chat_logging, deserialize_data
from .logic import Bot


class IndexPageView(View):
    def get(self, request):
        return render(request, "index.html")


def process_callback(request):
    import json

    _body = request.body.decode("utf-8")
    jivo_data = json.loads(_body)

    id = jivo_data.get('id', False)
    client_id = jivo_data.get('client_id', False)
    chat_id = jivo_data.get('chat_id', False)

    response = {}
    if not id:
        response['error'] = {'code': 1, 'message': 'No id'}
    elif not client_id:
        response['error'] = {'code': 2, 'message': 'No client id'}
    elif not chat_id:
        response['error'] = {'code': 3, 'message': 'No chat_id'}

    if not response:
        return jivo_data, id, client_id, chat_id

    return response


@method_decorator((csrf_exempt, client_chat_logging), name='dispatch')
class DataFromJivoView(View):
    http_method_names = ['post']

    def get(self, request):
        return HttpResponse('Bot sends POST requests here')

    def post(self, request):
        # data = deserialize_data(request.body)
        # Bot(data)
        #
        # return HttpResponse({'result': 'ok'}, status=200)

        from django.http import JsonResponse
        try:
            jivo_data, id, client_id, chat_id = process_callback(request)
        except:
            return JsonResponse(process_callback(request), status=500)

        print(jivo_data, id, client_id, chat_id)