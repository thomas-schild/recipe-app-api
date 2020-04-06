from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    # define the serializer class
    # ... the rest is provided 'magically' by django rest framework
    serializer_class = UserSerializer
