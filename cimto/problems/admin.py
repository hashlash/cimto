from django.contrib import admin

from cimto.problems.models import (
    AnswerKey, Problem, Problemset, ProblemsetProblem
)


class ProblemsetProblemInline(admin.TabularInline):
    model = ProblemsetProblem
    extra = 0


@admin.register(Problemset)
class ProblemsetAdmin(admin.ModelAdmin):
    inlines = [ProblemsetProblemInline]


class AnswerKeyInline(admin.TabularInline):
    model = AnswerKey
    extra = 0


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [AnswerKeyInline]
