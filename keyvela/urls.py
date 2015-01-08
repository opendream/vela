from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^keyvela/create', 'keyvela.views.keyvela_create', name='keyvela_create'),
    url(r'^keyvela/(?P<keyvela_id>\d+)/$', 'keyvela.views.keyvela_detail', name='keyvela_detail'),
    url(r'^keyvela/(?P<keyvela_id>\d+)/edit/$', 'keyvela.views.keyvela_edit', name='keyvela_edit'),
)