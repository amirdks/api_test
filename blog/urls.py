from django.urls import path, include
from .views import IndexView

app_name = "blog"
urlpatterns = [
    path("", IndexView.as_view(), name="index_page"),
    path("api/v1/", include("blog.api.v1.urls")),
]
