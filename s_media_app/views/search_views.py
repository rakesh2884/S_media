from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from s_media_app.models import User,Post
from s_media_app.serializers import UserSerializer,PostSerializer

class search(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request):
        search_type=request.data.get('search_type')
        search_value=request.data.get('search_value')
        if search_type=="user":
            user = User.objects.filter(username__icontains=search_value)
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data,status=status.HTTP_302_FOUND)
        elif search_type=="post":
            post = Post.objects.filter(caption__icontains=search_value)
            serializer = PostSerializer(post, many=True)
            return Response(serializer.data,status=status.HTTP_302_FOUND)