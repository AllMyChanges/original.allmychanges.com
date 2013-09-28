# -*- coding: utf-8 -*-
from rest_framework import viewsets, views
from rest_framework_extensions.mixins import DetailSerializerMixin

from allmychanges.models import Repo
from allmychanges.serializers import RepoSerializer, RepoDetailSerializer


class RepoViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
    serializer_detail_class = RepoDetailSerializer