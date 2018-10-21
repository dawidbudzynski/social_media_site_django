import random

import requests
from constants import NEWS_SOURCE_DATA_ALL
from decouple import config
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

API_KEY_NEWS = config('API_KEY_NEWS', cast=str)


class WelcomeView(View):
    def get(self, request):
        """pick random news from API and send it to welcome screen template"""
        news_source_data_all = dict(NEWS_SOURCE_DATA_ALL)
        news_source = news_source_data_all.popitem()[1]
        url = ('https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'.format(
            news_source['api_name'], API_KEY_NEWS))
        response = requests.get(url)
        response_to_display = response.json()['articles']
        single_response_to_display = random.choice(response_to_display)
        ctx = {
            'response': single_response_to_display,
        }
        return render(request,
                      template_name='welcome_page.html',
                      context=ctx)


class ThanksPage(TemplateView):
    template_name = 'thanks.html'
