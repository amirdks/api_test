from django.urls import include, path
from . import views

app_name = "accounts"
urlpatterns = [
    path("api/v1/", include("accounts.api.v1.urls")),
    # path('api/v2/', include('djoser.urls')),
    # path('api/v2/', include('djoser.urls.jwt')),
    path('test/', views.test, name='test'),
    path("", include("django.contrib.auth.urls")),
]
