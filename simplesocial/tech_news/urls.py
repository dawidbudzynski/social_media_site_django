from django.conf.urls import url

from . import views

app_name = 'tech_news'

urlpatterns = [
    url(r'^news_main/', views.NewsMainPage.as_view(), name='news-main'),
    url(r'^news_select/(?P<news_source>\w+)/$', views.NewsSelectedPage.as_view(), name='news-selected'),
]
