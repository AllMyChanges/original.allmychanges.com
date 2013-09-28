# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework_extensions.fields import ResourceUriField

from allmychanges.models import Repo


class RepoSerializer(serializers.ModelSerializer):
    resource_uri = ResourceUriField(view_name='repo-detail')

    class Meta:
        model = Repo
        fields = (
            'id',
            'resource_uri',
            'url',
            'title'
        )


class RepoDetailSerializer(RepoSerializer):
    class Meta(RepoSerializer.Meta):
        fields = RepoSerializer.Meta.fields