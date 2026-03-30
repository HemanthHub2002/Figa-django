from django.urls import path
from .views import AddToCart

from .views import view_cart, get_cart_item_count,IncreaseCartItem, DecreaseCartItem, RemoveCartItem

urlpatterns =[
    path('', view_cart, name = 'view_cart'),
    path('add/', AddToCart.as_view(), name = 'add_to_cart'),
    path('cart/count/', get_cart_item_count, name='cart_count'),
    path('increase/', IncreaseCartItem.as_view(), name='increase_cart'),
    path('decrease/', DecreaseCartItem.as_view(), name='decrease_cart'),
    path('remove/', RemoveCartItem.as_view(), name='remove_cart')
]