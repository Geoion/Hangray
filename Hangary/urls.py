from django.conf.urls import patterns, include, url

from django.contrib import admin
from website import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Hangary.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^temp/$', views.temp, name='temp'),
    url(r'^index/$', views.requires_login(views.index), name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^articles/(?P<year>\d+)/$', views.articles),
    url(r'^user/home/self$', views.user_home, name='userhome'),
    url(r'^user/home/(?P<user_id>\d+)$', views.user_home_, name='user_home_other'),#todo other people can look home page
    url(r'^user/editinfo$', views.user_info_edit, name='usereditinfo'),
    url(r'^user/detail$', views.user_detail_info, name='userdetail'),
    url(r'^question/submit/$', views.ask_question, name='ask_question'),
    url(r'^question/detail/(?P<qid>\d+)/$', views.question, name='question'),
    url(r'^topic/detail/(?P<tp_name>\w+)/$', views.topic_detail, name='topic_detail'),
    url(r'^topic/list/$', views.topic_list, name='topic_list'),
    url(r'^comment/(?P<answer>\d+)/$', views.comment, name='comment'),
)
