# -*- coding: utf-8 -*-
import logging

from django_rq import job
from allmychanges.utils import count_time


@job
def update_repo(repo_id):
    try:
        with count_time('task.update_repo.time'):
            from .models import Repo
            repo = Repo.objects.get(pk=repo_id)
            repo._update()
        
    except Exception:
        logging.getLogger('tasks').exception('Unhandler error in update_repo worker')
        raise
