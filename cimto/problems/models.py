from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.utils.text import Truncator
from rules import always_allow, is_authenticated
from rules.contrib.models import RulesModel

from cimto.problems.rules import is_problem_owner


class Problemset(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    problems = models.ManyToManyField('Problem', through='ProblemsetProblem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProblemsetProblem(models.Model):
    problemset = models.ForeignKey('Problemset', on_delete=models.CASCADE)
    problem = models.ForeignKey('Problem', on_delete=models.PROTECT)


class Problem(RulesModel):
    title = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.TextField()
    answer_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        rules_permissions = {
            'add': is_authenticated,
            'delete': is_problem_owner,
            'change': is_problem_owner,
            'view': always_allow,
        }

    def __str__(self):
        return self.title or Truncator(self.description).chars(100)
