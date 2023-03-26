from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = "api-v1"
router = DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
router.register("category", views.CategoryModelViewSet, basename="category")
urlpatterns = [
    # path('post', views.post_list_api, name='post_list_api'),
    # path('post/<int:id>', views.post_detail_api, name='post_detail_api')
    # path('post', views.PostListAPIView.as_view(), name='post_list_api'),
    # path('post/<int:id>', views.PostDetailAPIView.as_view(), name='post_detail_api')
    # path('post/', views.PostAPIViewSet.as_view({'get': 'list'}), name='post_view_set_api'),
    # path('post/<int:id>', views.PostAPIViewSet.as_view({'get': 'retrieve'}), name='post_view_set_api_aha'),
    path("", include(router.urls)),
    path('test/', views.CacheAPITest.as_view())
]
