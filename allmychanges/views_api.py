# -*- coding: utf-8 -*-
from rest_framework import viewsets, views
from rest_framework_extensions.mixins import DetailSerializerMixin
from rest_framework_extensions.decorators import action
from rest_framework.response import Response

from allmychanges.models import Repo
from allmychanges.serializers import RepoSerializer, RepoDetailSerializer


class RepoViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
    serializer_detail_class = RepoDetailSerializer
    queryset_detail = queryset.prefetch_related('versions__items__changes')

    @action(is_for_list=True, endpoint='create-changelog')
    def create_changelog(self, request, *args, **kwargs):
        return Response(data={'id': 1})
