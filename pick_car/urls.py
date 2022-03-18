from django.urls import path
from . import views

urlpatterns = [
    path("", views.front_page),
    path("test", views.test_api.as_view()),
    path("login", views.my_login)

]