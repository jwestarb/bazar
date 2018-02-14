from django.db.models import signals
from django.utils.functional import curry


class AuditMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated:
                user = request.user
            else:
                user = None

            mark_whodid = curry(self.mark_whodid, user)
            signals.pre_save.connect(mark_whodid, dispatch_uid=(self.__class__, request,), weak=False)

        response = self.get_response(request)
        response = self.process_response(request, response)
        return response

    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid=(self.__class__, request,))
        return response

    def mark_whodid(self, user, sender, instance, **kwargs):
        if not getattr(instance, 'criado_por_id', None):
            instance.criado_por = user
        if hasattr(instance, 'atualizado_por'):
            instance.atualizado_por = user
