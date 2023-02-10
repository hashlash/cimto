from django.urls import path
from rest_framework.routers import DefaultRouter

from cimto.problems.views import ProblemViewset

router = DefaultRouter()
router.register(r'problems', ProblemViewset, basename='problem')
urlpatterns = router.urls
