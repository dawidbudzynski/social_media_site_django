import requests
from django.shortcuts import render
from django.views import View

from .keys import api_key


# Create your views here.


class NewsMainPage(View):
    def get(self, request):
        return render(request,
                      template_name='tech_news/news_main.html')


class NewsSelectedPage(View):
    def get(self, request, news_source):
        news_source_dict = {
            'ign': ['ign', 'ign'],
            'polygon': ['polygon', 'polygon'],
            'techradar': ['techradar', 'techradar'],
            'theverge': ['the-verge', 'theverge']
        }
        news_source_list = []
        for news_source_key, news_source_values in news_source_dict.items():
            if news_source == news_source_key:
                news_source_list = news_source_values
        url = ('https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'.format(news_source_list[0], api_key))
        response = requests.get(url)

        ctx = {
            'response': response.json()['articles'],
        }
        return render(request,
                      template_name='tech_news/news_{}.html'.format(news_source_list[1]),
                      context=ctx)
