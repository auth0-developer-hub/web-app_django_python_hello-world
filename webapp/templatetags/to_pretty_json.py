import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django import template

register = template.Library()


@register.filter(name='to_pretty_json')
def to_pretty_json(obj):
    if isinstance(obj, QuerySet):
        return serialize('json', obj)
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4)
