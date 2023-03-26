from django.http import JsonResponse
from django.shortcuts import render
import requests

# Create your views here.
from django.core.cache import cache


def test(request):
    test = cache.get('test')
    if test is None:
        response = requests.get('https://bec071a2-57c5-4f69-a017-d70aea4ec953.mock.pstmn.io/test/delay/5')
        cache.set('test', response)
    else:
        response = cache.get('test')
    return JsonResponse(response.json())
