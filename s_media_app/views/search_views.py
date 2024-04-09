from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from s_media_app.handlers.success_handler import success_response
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
            return success_response(serializer.data,302)
        elif search_type=="post":
            post = Post.objects.filter(caption__icontains=search_value)
            serializer = PostSerializer(post, many=True)
            return success_response(serializer.data,302)