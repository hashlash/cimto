from django.test import TestCase

from cimto.tags.models import Tag


class TagModelTest(TestCase):
    def test_get_tags_query(self):
        Tag.objects.bulk_create([
            Tag(label='tag1'),
            Tag(label='tag2'),
        ])
        # basic usage
        tags = Tag.objects.get_tags(['tag1', 'tag2'])
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0].label, 'tag1')
        self.assertEqual(tags[1].label, 'tag2')
        self.assertEqual(Tag.objects.count(), 2)
        # default raise exception on missing tags
        with self.assertRaisesMessage(Tag.DoesNotExist, 'Missing tags with labels: tag3, tag4'):
            tags = Tag.objects.get_tags(['tag1', 'tag3', 'tag4'])
        self.assertEqual(Tag.objects.count(), 2)
        # fails silently
        tags = Tag.objects.get_tags(['tag1', 'tag3', 'tag4'], raise_exception=False)
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].label, 'tag1')
        self.assertEqual(Tag.objects.count(), 2)
        # create missing 
        tags = Tag.objects.get_tags(['tag1', 'tag3', 'tag4'], create_missing=True)
        self.assertEqual(len(tags), 3)
        self.assertEqual(tags[0].label, 'tag1')
        self.assertEqual(tags[1].label, 'tag3')
        self.assertEqual(tags[2].label, 'tag4')
        self.assertEqual(Tag.objects.count(), 4)
