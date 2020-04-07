from rest_framework import generics
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    # define the serializer class
    # ... the rest is provided 'magically' by django rest framework
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    # support that UI gets rendered for the browser - just for convenience
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
