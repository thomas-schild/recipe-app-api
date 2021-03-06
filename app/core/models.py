from django.db import models
from django.contrib.auth.models \
    import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """create a new user, persist and return him"""
        # create
        if not email:
            raise ValueError(
                "no email, though create_user demands a valid email"
            )
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)     # password gets hashed
        # persist
        user.save(using=self._db)
        # return
        return user

    def create_superuser(self, email, password):
        """create a new superuser, persist and return him"""
        # create
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        # (?) How to grant extended permissions?
        # persist
        user.save(using=self._db)
        # return
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model using email instead of a username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE    # delete a Tag if its User gets deleted
    )

    # overwrite __str__() for the class' string representation
    def __str__(self):
        return self.name
