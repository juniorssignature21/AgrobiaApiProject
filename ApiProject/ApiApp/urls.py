from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    ProductUploadView,
    ProductListView,
    ProductDetailView,
    AddToCartView,
    CartItemListView,
    OrderListView,
    OrderDetailView,
    CategoryListView,
    CategoryDetailView,
    CreatePaymentIntentAPIView
)



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/upload/', ProductUploadView.as_view(), name='product_upload'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartItemListView.as_view(), name='cart_item_list'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/create-payment-intent/', CreatePaymentIntentAPIView.as_view(), name='create_payment_intent'),
]
