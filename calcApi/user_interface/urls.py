from django.urls import path
from . import views

urlpatterns = [
    path('login', views.signin, name='log in'),
    path('admin_panel', views.admin_page, name='admin panel')
]