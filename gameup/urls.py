"""gameup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
import games.views
import users.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^games/$', games.views.GameList.as_view()),
    url(r'^games/(?P<pk>[0-9]+)/$', games.views.GameDetail.as_view()),
    url(r'^games/(?P<fk>[0-9]+)/evaluations/$', games.views.EvaluationList.as_view()),
    url(r'^games/(?P<fk>[0-9]+)/evaluations/(?P<pk>[0-9]+)$', games.views.EvaluationDetail.as_view()),
    url(r'^games/(?P<fk>[0-9]+)/reports/gamification$', games.views.GamificationReport.as_view()),
    url(r'^games/(?P<fk>[0-9]+)/reports/bloom$', games.views.BloomReport.as_view()),

    # url(r'^games/(?P<fk>[0-9]+)/reports/$', games.views.ReportList.as_view()),
    # url(r'^games/(?P<fk>[0-9]+)/reports/(?P<pk>[0-9]+)/$', games.views.ReportDetail.as_view()),

    url(r'^users/$', users.views.PersonList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', users.views.PersonDetail.as_view()),

    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]
urlpatterns = format_suffix_patterns(urlpatterns)
