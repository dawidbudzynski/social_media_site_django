import requests
from decouple import config
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

api_key = config('API_KEY')


# Create your views here.

class NewsMainPage(View):
    def get(self, request):
        return render(request,
                      template_name='tech_news/news_main.html')


def news_generate(request):
    news_source = request.GET.get('news_source', None)

    news_source_data_all = {
        'IGN': {
            'name': 'IGN',
            'api_name': 'ign',
            'image_url': '/static/tech_news/img/IGN.jpg'
        },
        'Polygon': {
            'name': 'Polygon',
            'api_name': 'polygon',
            'image_url': '/static/tech_news/img/polygon.png'
        },
        'TechRadar': {
            'name': 'TechRadar',
            'api_name': 'techradar',
            'image_url': '/static/tech_news/img/techradar.png'
        },
        'The Verge': {
            'name': 'The Verge',
            'api_name': 'the-verge',
            'image_url': '/static/tech_news/img/verge.png'
        },
    }
    news_source_data_single = {}
    for news_source_key, news_source_values in news_source_data_all.items():
        if news_source == news_source_key:
            news_source_data_single = news_source_values

    url = ('https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'.format(news_source_data_single['api_name'],
                                                                              api_key))
    response = requests.get(url)
    data = {
        'news_source': news_source_data_single['name'],
        'image_url': news_source_data_single['image_url'],
        'articles': response.json()['articles']
    }
    return JsonResponse(data)
