from django.db import models


class Problem(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    answer_key = models.CharField(max_length=255)

    def __str__(self):
        if self.title:
            return self.title
        return super().__str__()
