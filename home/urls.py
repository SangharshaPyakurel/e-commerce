from .views import *
from django.urls import path
app_name = "home"
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug>', CategoryView.as_view(), name='category'),
    path('brand/<slug>', BrandView.as_view(), name='brand'),
    path('product/<slug>', ProductDetailView.as_view(), name='product'),
    path('search', SearchView.as_view(), name='search'),
    path('product_review/<slug>', productReview, name='product_review'),
    path('cart', CartView.as_view(), name='cart_view'),
    path('signup', SignUp, name='signup'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('reduce_cart/<slug>', reduce_cart, name='reduce_cart'),
    path('delete_cart/<slug>', delete_cart, name='delete_cart'),
]