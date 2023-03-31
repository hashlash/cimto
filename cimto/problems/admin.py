from django.contrib import admin

from cimto.problems.models import Problem, Problemset, ProblemsetProblem

admin.site.register(Problem)


class ProblemsetProblemInline(admin.TabularInline):
    model = ProblemsetProblem
    extra = 0


@admin.register(Problemset)
class ProblemsetAdmin(admin.ModelAdmin):
    inlines = [ProblemsetProblemInline]
