from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from blog.models import Blog


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# class BlogSerializer(ModelSerializer):
#     author = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='pk')
#
#     class Meta:
#         model = Blog
#         fields = '__all__'


class BlogSerializer(HyperlinkedModelSerializer):
    author = serializers.HyperlinkedIdentityField(view_name='user-detail', many=True, lookup_field='id')

    class Meta:
        model = Blog
        fields = '__all__'

