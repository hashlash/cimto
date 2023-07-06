from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Submission(models.Model):
    problemset = models.ForeignKey(
        'problemset.Problemset',
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()


class ProblemSubmission(models.Model):
    submission = models.ForeignKey(
        'Submission',
        on_delete=models.CASCADE,
        related_name='problem_submissions',
    )
    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.RESTRICT,
        related_name='problem_submissions',
    )
    answer = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['submission', 'problem'],
                name='unique_submission_problem',
            ),
        ]

    def clean(self):
        if self.problem not in self.submission.problemset.problems:
            raise ValidationError(_(
                "The submission's problemset does not have the selected problem."
            ))
