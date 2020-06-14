from django.urls import path
from . import views

urlpatterns = [
    path('contact', views.contact, name='contact'),
    path('api', views.contactApi, name='contact_api')
]
