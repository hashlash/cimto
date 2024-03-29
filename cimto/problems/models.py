from html import unescape

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django_bleach.models import BleachField
from rules import always_allow, is_authenticated
from rules.contrib.models import RulesModel

from cimto.problems.rules import is_problem_owner


class Problem(RulesModel):
    title = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='subproblems',
        null=True, blank=True,
    )
    description = BleachField()
    tags = models.ManyToManyField('tags.Tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['slug'],
                condition=~Q(slug=''),
                name='unique_problem_slug',
            ),
        ]
        rules_permissions = {
            'add': is_authenticated,
            'delete': is_problem_owner,
            'change': is_problem_owner,
            'view': always_allow,
        }

    def __str__(self):
        return self.title or Truncator(unescape(strip_tags(self.description))).chars(100)

    @cached_property
    def origin(self):
        try:
            return self.problemsets.get(problem_mapping__is_origin=True)
        except Problem.DoesNotExist:
            return None


class AnswerKey(models.Model):
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='answer_keys')
    answer = models.CharField(max_length=255)
