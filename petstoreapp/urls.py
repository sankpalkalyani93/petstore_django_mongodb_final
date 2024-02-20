from django.urls import path
from . import views
from .views import PetDetailView

# create views and then add the views pages to the path
urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.pets_list, name='pets_list'),
    path('pets/create/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pets_detail'),
    path('search/', views.search_results, name='search_results'),
    path('pets/create/dog/', views.pet_create_dog, name='pet_create_dog'),
    path('pets/create/cat/', views.pet_create_cat,  name='pet_create_cat'),
    path('pets/create/bird/', views.pet_create_bird,  name='pet_create_bird'),
]
