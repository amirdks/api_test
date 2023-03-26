from django.test import SimpleTestCase
from django.urls import reverse, resolve

from blog.api.v1.views import PostModelViewSet
from blog.views import IndexView


class TestUrl(SimpleTestCase):
    def test_blog_url_resolve(self):
        url = reverse('blog:index_page')
        self.assertEqual(resolve(url).func.view_class, IndexView)
