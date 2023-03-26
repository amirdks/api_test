import requests
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from blog.api.v1.paginations import PostPagination
from blog.api.v1.permissions import IsOwnerOrReadOnly
from blog.api.v1.serializers import PostModelSerializer, CategoryModelSerializer
from blog.models import Post, Category

"""
@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list_api(reqeust):
    if reqeust.method == 'GET':
        posts = Post.objects.all()
        post_serializer = PostModelSerializer(posts, many=True)
        return Response(post_serializer.data, status=200)
    elif reqeust.method == 'POST':
        post_serializer = PostModelSerializer(data=reqeust.data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response(post_serializer.data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def post_detail_api(reqeust: HttpRequest, id):
    post = get_object_or_404(Post, id=id)
    if reqeust.method == 'GET':
        post_serializer = PostModelSerializer(post)
        return Response(post_serializer.data, status=200)
    elif reqeust.method == 'PUT':
        serializer = PostModelSerializer(post, data=reqeust.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif reqeust.method == 'DELETE':
        post.delete()
        return Response({'detail': 'post deleted'}, status=status.HTTP_204_NO_CONTENT)
"""


#
# class PostListAPIView(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostModelSerializer
#     permission_classes = [IsAuthenticated]
#

# class PostAPIViewSet(ViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostModelSerializer
#     permission_classes = [IsAuthenticated]
#
#     def list(self, request):
#         serializer = self.serializer_class(self.queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def retrieve(self, request, pk):
#         post = get_object_or_404(self.queryset, id=pk)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#

# class PostListAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostModelSerializer
#
#     def get(self, reqeust):
#         posts = Post.objects.all()
#         post_serializer = self.serializer_class(posts, many=True)
#         return Response(post_serializer.data, status=200)
#
#     def post(self, request):
#         post_serializer = self.serializer_class(data=request.data)
#         post_serializer.is_valid(raise_exception=True)
#         post_serializer.save()
#         return Response(post_serializer.data, status=status.HTTP_201_CREATED)

# class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostModelSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     lookup_field = 'id'

class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostModelSerializer

    def get(self, request:HttpRequest, id):
        post = get_object_or_404(Post, id=id)
        post_serializer = self.serializer_class(post)
        return Response(post_serializer.data, status=200)

    def put(self, reqeust, id):
        post = get_object_or_404(Post, id=id)
        serializer = self.serializer_class(post, data=reqeust.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return Response({'detail': 'post deleted'}, status=status.HTTP_204_NO_CONTENT)


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "author", "status"]
    search_fields = ["title", "content", "category__name"]
    ordering_fields = ["published_date"]
    pagination_class = PostPagination

    @action(
        methods=["get"],
        permission_classes=[IsAuthenticated],
        detail=True,
        url_name="test",
        url_path="test",
    )
    def test(self, reqeust, pk=None):
        return Response({"detail": "fuck u"}, status=status.HTTP_200_OK)


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticated]


class CacheAPITest(APIView):
    @method_decorator(cache_page(60))
    def get(self, reqeust):
        response = requests.get('https://bec071a2-57c5-4f69-a017-d70aea4ec953.mock.pstmn.io/test/delay/5')
        print(response)
        return Response({'detail': response.json()})
