from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django_bleach.models import BleachField

from cimto.problems.models import AnswerKey, Problem


class AnswerKeyInline(admin.TabularInline):
    model = AnswerKey
    extra = 0


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BleachField: {'widget': CKEditorWidget},
    }
    inlines = [AnswerKeyInline]
    prepopulated_fields = {'slug': ('title',)}
