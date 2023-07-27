from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin





class ProcessRequestMiddleware(MiddlewareMixin):    
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        user = request.user
        
        
        if  not user.is_authenticated:
            if  request.resolver_match.url_name in ["tag_api","tag_read"]:
                pass
            else:
                if  not request.resolver_match.url_name=="login"  :
                    return redirect("login")