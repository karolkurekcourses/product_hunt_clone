from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('create/', views.create, name='create'),
    path('product/<int:product_id>/', views.details, name='details'),
    path('product/<int:product_id>/esteem/', views.esteem, name='esteem'),
    path('about/', views.about, name='about'),
]
