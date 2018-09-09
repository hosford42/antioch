# antioch
# Copyright (c) 1999-2018 Phil Christensen
#
#
# See LICENSE for details

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from antioch.core import models

class VerbInline(admin.TabularInline):
    model = models.Verb
    fk_name = 'origin'
    extra = 1
    exclude = ('code',)
    raw_id_fields = ('owner',)
    readonly_fields = ('filename', 'admin_link')
    
    def admin_link(self, instance):
        if(instance.pk is None):
            return ''
        verb_url = reverse('admin:%s_%s_change' % (
           instance._meta.app_label,  'verb'),  args=[instance.pk] )
        object_url = reverse('admin:%s_%s_change' % (
          instance._meta.app_label,  'object'),  args=[instance.origin.pk] )
        link = '<a href="{vu}?goto={ou}&_popup=1">Edit</a>'.format(vu=verb_url, ou=object_url)
        return mark_safe(link)
    admin_link.short_description = "Edit"
    
class PropertyInline(admin.TabularInline):
    model = models.Property
    fk_name = 'origin'
    extra = 1
    readonly_fields = ('name', 'value', 'owner')

class ParentsInline(admin.TabularInline):
    model = models.Relationship
    fk_name = 'child'
    extra = 1
    raw_id_fields = ("parent",)

class ObjectAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'unique_name', 'owner', 'location')
    search_fields = ('name',)
    autocomplete_fields = ['owner', 'location', 'parents']
    inlines = [
        VerbInline,
        PropertyInline,
        ParentsInline
    ]
admin.site.register(models.Object, ObjectAdmin)

class VerbAdmin(admin.ModelAdmin):
    autocomplete_fields = ['owner', 'origin']
    search_fields = ('name',)
admin.site.register(models.Verb, VerbAdmin)

class PropertyAdmin(admin.ModelAdmin):
    autocomplete_fields = ['owner', 'origin']
    search_fields = ('name',)
admin.site.register(models.Property, PropertyAdmin)

class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('name',)
admin.site.register(models.Permission, PermissionAdmin)

class AccessAdmin(admin.ModelAdmin):
    list_display = ('rule', 'actor', 'action', 'entity', 'origin')
    list_filter = ['rule', 'permission', 'type', 'group']
    autocomplete_fields = ['accessor', 'permission', 'property', 'verb', 'object']
    
    def actor(self, obj):
        return obj.actor()
    
    def entity(self, obj):
        return obj.entity()
    
    def origin(self, obj):
        return obj.origin()
    
    def action(self, obj):
        return obj.permission.name
admin.site.register(models.Access, AccessAdmin)

class PlayerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['avatar']
admin.site.register(models.Player, PlayerAdmin)

class TaskAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user', 'origin']
admin.site.register(models.Task)