# coding: utf-8

from vanilla import FormView
from .forms import GetChangeLogForm
from django.shortcuts import render
import random

class IndexView(FormView):
    form_class = GetChangeLogForm
    template_name = 'index.html'

    def form_valid(self, form):
        changes =    [
            {
                'version': '0.1.3',
                'sections': [
                    {
                        'items': [
                            'Исправлен баг с кодировками',
                            'Добавлена возможность шарить папки'
                            ]
                        }
                    ]
                },
            {
                'version': '0.1.2',
                'sections': [
                    {
                        'items': [
                            'Добавлен перевод на китайский язык',
                            'Цвет шапки теперь более привлекательный — красный',
                            'Наконец стали вести ChangeLog'
                            ]
                        }
                    ]
                }
            ]
        return self.render_to_response(dict(
                job_id=random.randint(0, 1000),
                changes=changes,
                form=form))

