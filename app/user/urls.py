from django.urls import path
from . import views


# used within django.url.reverse() method calls
app_name = 'user'
urlpatterns = [
    # link the url path with the view, and define a pattern for the reverse()
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
