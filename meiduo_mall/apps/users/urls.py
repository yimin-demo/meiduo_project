from django.urls import path
from django.urls import register_converter
from apps.users.views import *

urlpatterns = [
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view()),
    path('register/', RegisterView.as_view()),
]