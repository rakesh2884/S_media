from s_media_app.models import User
from rest_framework.response import Response
from functools import wraps
from rest_framework import status

def is_user(f):
    @wraps(f)
    def decorator(self,request,*args, **kwargs):
        user=request.user
        if user.role=="1":
            return f(self,request,*args, **kwargs)
        else:
            return Response({'message':'no acess'},status=status.HTTP_401_UNAUTHORIZED)
    return decorator

def is_admin(f):
    @wraps(f)
    def decorator(self,request,*args, **kwargs):
        user=request.user
        if user.role=="2":
            return f(self,request,*args, **kwargs)
        else:
            return Response({'message':'no access'},status=status.HTTP_401_UNAUTHORIZED)
    return decorator

def is_moderator(f):
    @wraps(f)
    def decorator(self,request,*args, **kwargs):
        user=request.user
        if user.role=="3":
            return f(self,request,*args, **kwargs)
        else:
            return Response({'message':'no access'},status=status.HTTP_401_UNAUTHORIZED)
    return decorator