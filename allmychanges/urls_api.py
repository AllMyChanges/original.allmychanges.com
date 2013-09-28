# -*- coding: utf-8 -*-
from rest_framework_extensions.routers import ExtendedDefaultRouter as DefaultRouter

from allmychanges.views_api import RepoViewSet


router = DefaultRouter()
router.root_view_name = 'main_api_path'
router.register(r'repos', RepoViewSet, base_name='repo')

urlpatterns = router.urls