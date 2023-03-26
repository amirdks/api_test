import datetime

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(email='test@test.com', password='61683550ali')
    return user


@pytest.mark.django_db
class TestPostApi:

    def test_get_post_response_200_status(self, api_client, common_user):
        url = reverse('blog:api-v1:post-list')
        api_client.force_authenticate(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self, api_client):
        url = reverse('blog:api-v1:post-list')
        data = {
            'title': 'test',
            'content': 'test',
            'status': True,
            # 'category': 'test',
            'published_date': datetime.datetime.now(),
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == 401

    def test_create_post_response_201_status(self, api_client, common_user):
        url = reverse('blog:api-v1:post-list')
        data = {
            'title': 'test',
            'content': 'test',
            'status': True,
            # 'category': 'test',
            'published_date': datetime.datetime.now(),
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201
