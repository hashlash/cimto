from django.contrib import admin

from cimto.problemset.models import Problemset, ProblemsetProblem


class ProblemsetProblemInline(admin.TabularInline):
    model = ProblemsetProblem
    extra = 0


@admin.register(Problemset)
class ProblemsetAdmin(admin.ModelAdmin):
    inlines = [ProblemsetProblemInline]
    prepopulated_fields = {'slug': ('title',)}