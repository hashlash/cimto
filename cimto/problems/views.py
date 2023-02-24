from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from cimto.problems.models import Problem
from cimto.problems.serializers import ProblemSerializer


class ProblemViewset(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
