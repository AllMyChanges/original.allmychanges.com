# -*- coding: utf-8 -*-
from django.contrib import admin

from allmychanges.models import Repo, RepoVersion, RepoVersionItem, RepoVersionItemChange, Subscription


class RepoVersionInlines(admin.TabularInline):
    model = RepoVersion


class RepoVersionItemInlines(admin.TabularInline):
    model = RepoVersionItem


class RepoVersionItemChangeInlines(admin.TabularInline):
    model = RepoVersionItemChange


class RepoAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'requested_count')
    date_hierarchy = 'date_created'
    inlines = (RepoVersionInlines,)
    search_fields = ('url', 'title')


class RepoVersionAdmin(admin.ModelAdmin):
    inlines = (RepoVersionItemInlines,)


class RepoVersionItemAdmin(admin.ModelAdmin):
    inlines = (RepoVersionItemChangeInlines,)


class SubscriptionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Repo, RepoAdmin)
admin.site.register(RepoVersion, RepoVersionAdmin)
admin.site.register(RepoVersionItem, RepoVersionItemAdmin)
admin.site.register(Subscription, SubscriptionAdmin)