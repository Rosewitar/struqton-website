"""URL configuration for the Struqton website app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prototype/<int:prototype_id>/', views.prototype, name='prototype'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('contact/success/', views.contact_success, name='contact_success'),
]
