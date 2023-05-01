from django.db import models


class Tag(models.Model):
    name = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
