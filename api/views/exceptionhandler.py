from django.http import JsonResponse

def exceptionhandler(func):
    def Inner_Function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return JsonResponse({'status': 0, 'msg': str(e)})
    return Inner_Function