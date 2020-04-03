from functools import wraps
from django.core.exceptions import PermissionDenied

def ajax_login_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        raise PermissionDenied ## or 401 == not authenticated
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
