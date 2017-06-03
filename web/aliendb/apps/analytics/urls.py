from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about', views.about, name='about'),
    url(r'^api', views.api, name='api'),
    url(r'^submission/(?P<id>[\w]+)', views.submission, name='submission'),
    url(r'^search', views.search, name='search')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
