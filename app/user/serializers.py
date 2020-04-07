from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
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

    # overwrite update
    def update(self, instance, data):
        """update a user and return it, password set correctly"""
        # extract password out of provided data
        # default value required for pop(), use None here
        passwd = data.pop('password', None)
        # simply update other fields
        user = super().update(instance, data)
        if passwd:
            user.set_password(passwd)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the auth token"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
     )

    def validate(self, attributes):
        """validate and authenticate the credentials"""
        email = attributes.get('email')
        passwd = attributes.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=passwd
        )
        if not user:
            msg = _('authentication failed for provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        # user was authenticated, return him within the attributes
        attributes['user'] = user
        return attributes
