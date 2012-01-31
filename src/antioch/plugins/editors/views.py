import urllib

from django import template, shortcuts
from django.conf import settings
from django.contrib.auth.decorators import login_required

from antioch.client import models
from antioch.plugins.editors import forms

import simplejson

@login_required
def object_editor(request, object_id):
	o = models.Object.objects.get(pk=object_id)
	if(request.method == 'POST'):
		form = forms.ObjectForm(request.POST, instance=o)
		if(form.is_valid()):
			# this needs to be centralized
			urllib.urlopen(settings.APPSERVER_URL + 'rest/modify-object', simplejson.dumps(dict(
				user_id		= request.user.avatar.id,
				object_id	= o.id,
				name		= request.POST['name'],
				# returns the int as a string
				location	= request.POST['location'],
				owner		= request.POST['owner'],
				parents		= ','.join([x for x in request.POST['parents'].split('|') if x]),
			))).read()
	else:
		form = forms.ObjectForm(instance=o)
	
	return shortcuts.render_to_response('object-editor.html', dict(
		title           = "object editor",
		form            = form,
	), context_instance=template.RequestContext(request))

@login_required
def property_editor(request, property_id):
	return shortcuts.render_to_response('property-editor.html', dict(
		title           = "property editor",
	), context_instance=template.RequestContext(request))

@login_required
def verb_editor(request, verb_id):
	return shortcuts.render_to_response('verb-editor.html', dict(
		title           = "verb editor",
	), context_instance=template.RequestContext(request))

@login_required
def access_editor(request, entity_type, entity_id):
	return shortcuts.render_to_response('access-editor.html', dict(
		title           = "access editor",
	), context_instance=template.RequestContext(request))

