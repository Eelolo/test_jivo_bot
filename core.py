@method_decorator(csrf_exempt, name='dispatch')
class FormResultBotView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):

        try:
            jivo_data, id, client_id, chat_id = process_callback(request)
        except:
            return JsonResponse(process_callback(request), status=500)

        utime = dateformat.format(timezone.now(), 'U')

        chat = Chat.objects.filter(chat_id=chat_id).first()
        if not chat:
            chat = Chat.objects.create(
                chat_id=chat_id,
                client_id=client_id,
            )

        text = ''
        if jivo_data.get('message', False):
            _msg = jivo_data.get('message', False)
            if _msg.get('text', False):
                text = _msg.get('text', False)
                chat_message = ChatMessage.objects.create(
                    chat=chat,
                    text=text,
                    step=chat.step
                )

        response = {}

        chat = process_step(id, client_id, chat_id, text, chat)
        not_understand_message(id, client_id, utime, chat)
        invite_step(id, client_id, chat_id, utime, chat)

        return JsonResponse(response, status=200)