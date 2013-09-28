# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework_extensions.mixins import DetailSerializerMixin
from rest_framework_extensions.decorators import action
from rest_framework.response import Response

from allmychanges.models import Repo
from allmychanges.serializers import RepoSerializer, RepoDetailSerializer, CreateChangelogSerializer


class RepoViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
    serializer_detail_class = RepoDetailSerializer
    queryset_detail = queryset.prefetch_related('versions__items__changes')

    @action(is_for_list=True, endpoint='create-changelog')
    def create_changelog(self, request, *args, **kwargs):
        serializer = CreateChangelogSerializer(data=request.DATA)
        if serializer.is_valid():
            repo = Repo.start_changelog_processing_for_url(url=serializer.data['url'])
            return Response(data={'id': repo.id})
        else:
            raise ParseError(detail=serializer.errors)

    def handle_exception(self, exc):
        if isinstance(exc, ParseError):
            return Response(data={u'error_messages': exc.detail}, status=400, exception=exc)
        return super(RepoViewSet, self).handle_exception(exc=exc)