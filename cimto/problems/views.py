from rest_framework import viewsets

from cimto.problems.models import Problem
from cimto.problems.serializers import ProblemSerializer


class ProblemViewset(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer