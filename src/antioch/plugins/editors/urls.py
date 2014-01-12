from django.conf.urls import patterns, include, url

from ajax_select import urls as ajax_select_urls

urlpatterns = patterns('antioch.plugins.editors.views',
	url(r'^editor/object/(\d+)', 'object_editor', name='object_editor'),
	url(r'^editor/property/(\d+)', 'property_editor', name='property_editor'),
	url(r'^editor/verb/(\d+)', 'verb_editor', name='verb_editor'),
	url(r'^editor/access/(\w+)/(\d+)', 'access_editor', name='access_editor'),
) + patterns('',
	url(r'^editor/lookups/', include(ajax_select_urls)),
)
