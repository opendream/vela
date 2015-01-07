from django.conf.urls import url, patterns

urlpatterns = patterns('presentation.views',
    url(r'^$', 'home', name='home'),
    url(r'^delete/(?P<app_label>[A-Za-z0-9-_.]+)/(?P<model_name>[A-Za-z0-9-_.]+)/(?P<id>\d+)/$', 'presentation_delete', name='presentation_delete'),

)
