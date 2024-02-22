from django.urls import path
from . import views
from .views import ProductDetailView

# create views and then add the views pages to the path
urlpatterns = [
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('pets/', views.pets_list, name='pets_list'),
    path('pets/create/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/', views.pet_detail, name='pets_detail'),
    path('search/', views.search_results, name='search_results'),
    path('pets/create/dog/', views.pet_create_dog, name='pet_create_dog'),
    path('pets/create/cat/', views.pet_create_cat,  name='pet_create_cat'),
    path('pets/create/bird/', views.pet_create_bird,  name='pet_create_bird'),
    path('products/', views.products_list, name='products_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='products_detail'),
    path('products/create/food/', views.product_create_food, name='pet_create_food'),
    path('products/create/medicines/', views.product_create_medicines,  name='pet_create_medicines'),
    path('products/create/toys/', views.product_create_toys,  name='pet_create_toys'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('add_to_cart/pet/<int:pk>/', views.add_pet_to_cart, name='add_pet_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('proceed_to_pay/', views.proceed_to_pay, name='proceed_to_pay'),
]
