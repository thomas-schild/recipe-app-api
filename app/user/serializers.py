from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # setup restrictions for extra-keyword-args
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6,
             }
         }

    # overwrite django-rest's create method
    def create(self, data):
        """create a new user and return it, password gets encrypted"""
        # ensure 'create()' calls the specific 'create_user()' method
        # note that the 'data' gets validated
        user = get_user_model().objects.create_user(**data)
        return user
