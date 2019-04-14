from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^subreddits$', views.subreddits),
    url(r'^about$', views.about),
    url(r'^api$', views.api),
    url(r'^submission/(?P<id>[\w]+)$', views.submission),
    # url(r'^subreddit/(?P<subreddit>[\w]+)$', views.subreddit),
    url(r'^(subreddit|r)/(?P<subreddit>[\w]+)$', views.subreddit),
    url(r'^search$', views.search)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
