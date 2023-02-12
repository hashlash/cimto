from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from cimto.problems.models import Problem
from cimto.problems.serializers import ProblemSerializer


class ProblemViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
