# -*- coding: utf-8 -*-
from django.contrib import admin

from allmychanges.models import Repo


class RepoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Repo, RepoAdmin)