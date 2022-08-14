from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import generics
from api.serializers import BlogSerializer, UserSerializer
from blog.models import Blog

User = get_user_model()


class BlogAPIView(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer



class UserAPIView(ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, context={'request', 'request'})
        return Response(serializer.data)