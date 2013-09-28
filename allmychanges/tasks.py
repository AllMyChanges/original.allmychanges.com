# -*- coding: utf-8 -*-
import logging

from django_rq import job


@job
def update_repo(repo_id):
    try:
        from .models import Repo
        repo = Repo.objects.get(pk=repo_id)
        repo._update()
    except Exception:
        logging.getLogger('tasks').exception('Unhandler error in update_repo worker')
        raise
