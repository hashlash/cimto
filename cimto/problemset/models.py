from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint


class Problemset(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    problems = models.ManyToManyField('problems.Problem', related_name='problemsets', through='ProblemsetProblem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProblemsetProblem(models.Model):
    problemset = models.ForeignKey(
        'Problemset',
        on_delete=models.CASCADE,
        related_name='problem_mapping',
    )
    number = models.PositiveSmallIntegerField()
    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.PROTECT,
        related_name='problemset_mapping',
    )
    is_origin = models.BooleanField(default=False)

    class Meta:
        ordering = ['number']
        constraints = [
            UniqueConstraint(
                fields=['problemset', 'number'],
                name='unique_problemset_problem_number',
            ),
            UniqueConstraint(
                fields=['problem'],
                condition=Q(is_origin=True),
                name='unique_problem_origin',
            ),
        ]
