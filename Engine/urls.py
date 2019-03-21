from django.urls import path
from . import views

urlpatterns = [path("token-auth/", views.TokenAuth, name="TokenAuth")]
