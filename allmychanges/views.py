from vanilla import FormView
from .forms import GetChangeLogForm
from django.shortcuts import render
import random

class IndexView(FormView):
    form_class = GetChangeLogForm
    template_name = 'index.html'

    def form_valid(self, form):
        return self.render_to_response(dict(
                job_id=random.randint(0, 1000),
                form=form))

