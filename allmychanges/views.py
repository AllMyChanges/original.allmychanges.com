# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.utils import timezone

from .models import BlogPost


class IndexView(TemplateView):
    template_name = 'allmychanges/index.html'

    def get_context_data(self, **kwargs):
        result = super(IndexView, self).get_context_data(**kwargs)
        result['settings'] = settings
        return result


class BlogView(ListView):
    model = BlogPost

    def get_queryset(self):
        return BlogPost.objects \
            .filter(published_at__lte=timezone.now()) \
            .order_by('-published_at')


class HumansView(TemplateView):
    template_name = 'allmychanges/humans.txt'
    content_type = 'text/plain'
