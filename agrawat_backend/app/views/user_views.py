from agrawat_backend.app.models import User
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from agrawat_backend.app.services.user_service import sync_user
from agrawat_backend.app.serializers import UserPublicSerializer



class UserDetail(APIView):
    """
    Sync a user with Auth0
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request):
        user = self.get_object(request.user.id)
        resp_data = sync_user(user)
        return Response(resp_data)

    def get(self, request):
        user = self.get_object(request.user.id)
        serializer = UserPublicSerializer(user)
        return Response(serializer.data)


