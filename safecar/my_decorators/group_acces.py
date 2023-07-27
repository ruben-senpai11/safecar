from functools import wraps

from safecar.models import UserGroup
from django.http import Http404

def group_required(groups=[]):    
    def decorator(func):
        def inner_decorator(request,*args, **kwargs):
            for group in groups:
                try:
                    if UserGroup.objects.get(sys_name=group) == request.user.user_group:
                        return func(request, *args, **kwargs)
                except:
                    pass

            raise Http404()

        return wraps(func)(inner_decorator)

    return decorator