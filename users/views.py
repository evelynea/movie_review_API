from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can perform CRUD

    # Override the default list method to prevent listing all users
    def list(self, request, *args, **kwargs):
        return Response({"detail": "Listing all users is not allowed."})

    # Ensure users can only update/delete their own account
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            raise PermissionDenied("you are not allowed to update this account.")
            
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            raise PermissionDenied("You are not allowed to delete this account")
        return super().destroy(request, *args, **kwargs)

     # Custom action to retrieve the current user's profile
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """ Return the authenticated user's data """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)