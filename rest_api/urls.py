from django.conf.urls import url, include
from rest_framework import routers

from . import views

app_name = 'rest_api'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'users')
router.register(r'groups', views.GroupViewSet, 'groups')
router.register(r'posts', views.PostViewSet, 'posts')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-main/', views.RestApiMain.as_view(), name='api-main'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
