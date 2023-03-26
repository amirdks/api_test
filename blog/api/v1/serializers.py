from django.http import HttpRequest
from rest_framework import serializers

from accounts.models import Profile
from blog.models import Post, Category


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostModelSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField(
        method_name="get_absolute_url", read_only=True
    )
    snipped = serializers.ReadOnlyField(source="get_snipped")
    # category = CategoryModelSerializer()

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request: HttpRequest = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request: HttpRequest = self.context.get("request")
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snipped")
            rep["category"] = CategoryModelSerializer(
                instance.category, context={"request": request}
            ).data
        else:
            rep.pop("content")
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user_id=self.context.get("request").user.id
        )
        return super(PostModelSerializer, self).create(validated_data)
