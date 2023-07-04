from django.conf import settings
from django.db import models


class Submission(models.Model):
    problemset = models.ForeignKey('problemset.Problemset', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()


class ProblemSubmission(models.Model):
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE)
    problem = models.ForeignKey('problems.Problem', on_delete=models.RESTRICT)
    answer = models.CharField(max_length=255)
