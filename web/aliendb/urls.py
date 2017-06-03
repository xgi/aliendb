from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('aliendb.apps.analytics.urls')),
]
