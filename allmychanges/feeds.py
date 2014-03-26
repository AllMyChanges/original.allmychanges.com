from django.utils import timezone
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from .models import BlogPost


# docs: https://docs.djangoproject.com/en/1.5/ref/contrib/syndication/

class LatestEntriesFeed(Feed):
    title = "Allmychanges.com's Blog"
    link = "/blog/"
    description = "All about changelog parsing and delivering."

    def items(self):
        return BlogPost.objects \
            .filter(published_at__lte=timezone.now()) \
            .order_by('-published_at')[:5]


    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body_html

    def item_link(self, item):
        return '/blog/'
        #return reverse('news-item', args=[item.pk])
