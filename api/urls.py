from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from api.views import BlogAPIView, UserAPIView

router = routers.SimpleRouter()
router.register('blogs', BlogAPIView, basename='blogs')
router_2 = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserAPIView.as_view({'get': 'list'})),
    path('users/<int:pk>/', UserAPIView.as_view({'get': 'retrieve'}), name='user-detail'),
]