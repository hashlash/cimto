from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django_bleach.models import BleachField

from cimto.problemset.models import Problemset, ProblemsetProblem


class ProblemsetProblemInline(admin.TabularInline):
    model = ProblemsetProblem
    extra = 0


@admin.register(Problemset)
class ProblemsetAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BleachField: {'widget': CKEditorWidget},
    }
    inlines = [ProblemsetProblemInline]
    prepopulated_fields = {'slug': ('title',)}
