from functools import wraps

from utils.error_handler import error_response
from s_media import settings


def is_user(f):
    @wraps(f)
    def decorator(self, request, *args, **kwargs):
        user = request.user
        if user:
            if user.role == settings.USER_ROLE:
                return f(self, request, *args, **kwargs)
            else:
                return error_response('no acess', 401)
        else:
            return error_response('User not exist', 400)
    return decorator


def is_admin(f):
    @wraps(f)
    def decorator(self, request, *args, **kwargs):
        user = request.user
        if user:
            if user.role == settings.ADMIN_ROLE:
                return f(self, request, *args, **kwargs)
            else:
                return error_response('no acess', 401)
        else:
            return error_response('User not exist', 400)
    return decorator


def is_moderator(f):
    @wraps(f)
    def decorator(self, request, *args, **kwargs):
        user = request.user
        if user:
            if user.role == settings.MODERATOR_ROLE:
                return f(self, request, *args, **kwargs)
            else:
                return error_response('no acess', 401)
        else:
            return error_response('User not exist', 400)
    return decorator
