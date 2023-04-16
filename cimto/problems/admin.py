from django.contrib import admin

from cimto.problems.models import AnswerKey, Problem


class AnswerKeyInline(admin.TabularInline):
    model = AnswerKey
    extra = 0


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [AnswerKeyInline]
    prepopulated_fields = {'slug': ('title',)}
