from django.urls import path
from .views import (
    register,
    change_password,
    BookGenericAPIView,
    BookDetailGenericAPIView,
    ReviewGenericAPIView,
    ReviewDetailGenericAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', change_password, name='change_password'),

    path('books/', BookGenericAPIView.as_view(), name='books'),
    path('books/<int:pk>/', BookDetailGenericAPIView.as_view(), name='book_detail'),

    path('books/<int:book_id>/reviews/', ReviewGenericAPIView.as_view(), name='book_reviews'),
    path('reviews/<int:pk>/', ReviewDetailGenericAPIView.as_view(), name='review_detail'),
]
