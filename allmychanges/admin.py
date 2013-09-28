# -*- coding: utf-8 -*-
from django.contrib import admin

from allmychanges.models import Repo, RepoVersion, RepoVersionItem, RepoVersionItemChange


class RepoVersionInlines(admin.TabularInline):
    model = RepoVersion


class RepoVersionItemInlines(admin.TabularInline):
    model = RepoVersionItem


class RepoVersionItemChangeInlines(admin.TabularInline):
    model = RepoVersionItemChange


class RepoAdmin(admin.ModelAdmin):
    inlines = (RepoVersionInlines,)


class RepoVersionAdmin(admin.ModelAdmin):
    inlines = (RepoVersionItemInlines,)


class RepoVersionItemAdmin(admin.ModelAdmin):
    inlines = (RepoVersionItemChangeInlines,)


admin.site.register(Repo, RepoAdmin)
admin.site.register(RepoVersion, RepoVersionAdmin)
admin.site.register(RepoVersionItem, RepoVersionItemAdmin)