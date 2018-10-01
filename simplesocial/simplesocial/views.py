import random

import requests
from constants import NEWS_SOURCE_DATA_ALL
from decouple import config
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

api_key = config('API_KEY')


class WelcomeView(View):
    def get(self, request):
        news_source_data_all = dict(NEWS_SOURCE_DATA_ALL)
        news_source = news_source_data_all.popitem()[1]
        url = ('https://newsapi.org/v2/top-headlines?sources={}&apiKey={}'.format(news_source['api_name'], api_key))
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
