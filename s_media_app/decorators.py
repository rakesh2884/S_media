from functools import wraps

from rest_framework.response import Response
from rest_framework import status

from s_media import settings


def is_user(f):
    @wraps(f)
    def decorator(self,request,*args, **kwargs):
        user=request.user
        if user:
            if user.role==settings.USER_ROLE:
                return f(self,request,*args, **kwargs)
            else:
                return Response({'message':'no acess'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':'User not exist'},status=status.HTTP_400_BAD_REQUEST)
    return decorator

def is_admin(f):
    @wraps(f)
    def decorator(self,request,*args, **kwargs):
        user=request.user
        if user:
            if user.role==settings.ADMIN_ROLE:
                return f(self,request,*args, **kwargs)
            else:
                return Response({'message':'no access'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':'User not exist'},status=status.HTTP_400_BAD_REQUEST)
    return decorator

def is_moderator(f):
    @wraps(f)
    def decorator(self,request,*args, **kwargs):
        user=request.user
        if user:
            if user.role==settings.MODERATOR_ROLE:
                return f(self,request,*args, **kwargs)
            else:
                return Response({'message':'no access'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':'User not exist'},status=status.HTTP_400_BAD_REQUEST)
    return decorator