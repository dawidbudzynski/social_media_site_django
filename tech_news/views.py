import requests
from constants import NEWS_SOURCE_DATA_ALL
from decouple import config
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

API_KEY_NEWS = config('API_KEY_NEWS', cast=str)


# Create your views here.

class NewsMainPage(View):
    def get(self, request):
        default_news_source = NEWS_SOURCE_DATA_ALL['Polygon']
        url = ('https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'.format(
            default_news_source['api_name'],
            API_KEY_NEWS))
        response = requests.get(url)
        ctx = {
            'response': response.json()['articles'],
        }
        return render(request,
                      template_name='tech_news/news_main.html',
                      context=ctx)


def news_generate(request):
    news_source = request.GET.get('news_source', None)
    news_source_data_single = {}
    for news_source_key, news_source_values in NEWS_SOURCE_DATA_ALL.items():
        if news_source == news_source_key:
            news_source_data_single = news_source_values
    url = ('https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'.format(
        news_source_data_single['api_name'],
        API_KEY_NEWS))
    response = requests.get(url)
    data = {
        'news_source': news_source_data_single['name'],
        'image_url': news_source_data_single['image_url'],
        'articles': response.json()['articles']
    }
    return JsonResponse(data)
