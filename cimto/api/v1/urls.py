from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from cimto.problems.views import ProblemViewset

router = DefaultRouter()
router.register(r'problems', ProblemViewset, basename='problem')

urlpatterns = [
    path("auth/token/", obtain_auth_token, name='auth-token'),
    *router.urls,
]
