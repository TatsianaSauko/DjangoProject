from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

]