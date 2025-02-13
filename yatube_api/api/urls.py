from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


jwt_endpoints = [
    path('create/', TokenObtainPairView.as_view(), name='token_create_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify')
]

urlpatterns = [
    path('v1/jwt/', include(jwt_endpoints)),
]
