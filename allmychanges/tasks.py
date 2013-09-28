# -*- coding: utf-8 -*-
from django_rq import job


@job
def update_repo(repo_id):
    from .models import Repo
    repo = Repo.objects.get(pk=repo_id)
    repo._update()
