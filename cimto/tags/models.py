from django.db import models, transaction


class TagQuerySet(models.QuerySet):
    def get_tags(self, labels, create_missing=False, raise_exception=True):
        if create_missing:
            tags = []
            with transaction.atomic(using=self.db):
                for l in labels:
                    tag, _ = self.get_or_create(label=l)
                    tags.append(tag)
            return tags
        tags = self.filter(label__in=labels)
        if raise_exception and len(tags) != len(labels):
            missing_tag_labels = [l for l in labels if l not in {t.label for t in tags}]
            raise self.model.DoesNotExist(
                f"Missing tags with labels: {', '.join(missing_tag_labels)}."
            )
        return tags


class Tag(models.Model):
    label = models.SlugField(unique=True)
    description = models.TextField()

    objects = TagQuerySet.as_manager()

    def __str__(self):
        return self.name
