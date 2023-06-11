from django.contrib.auth import get_user_model
from django.test import TestCase

from cimto.problems.models import Problem
from cimto.problemset.models import Problemset, ProblemsetProblem

User = get_user_model()


class ProblemsetViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username='test_user',
            password='secret',
        )

    def test_problem_ancestor_context(self):
        r"""Test the following structure
              A
            / |  \
          B   C    D
         / \     / | \
        E   F   G  H  I
        """
        a = Problem.objects.create(owner=self.test_user, description='A')
        b = Problem.objects.create(owner=self.test_user, parent=a, description='B')
        c = Problem.objects.create(owner=self.test_user, parent=a, description='C')
        d = Problem.objects.create(owner=self.test_user, parent=a, description='D')
        e = Problem.objects.create(owner=self.test_user, parent=b, description='E')
        f = Problem.objects.create(owner=self.test_user, parent=b, description='F')
        g = Problem.objects.create(owner=self.test_user, parent=d, description='G')
        h = Problem.objects.create(owner=self.test_user, parent=d, description='H')
        i = Problem.objects.create(owner=self.test_user, parent=d, description='I')
        ps = Problemset.objects.create(
            title='Test Problemset',
            slug='test-problemset',
            owner=self.test_user,
        )
        ProblemsetProblem.objects.bulk_create([
            ProblemsetProblem(problemset=ps, number=1, problem=e),
            ProblemsetProblem(problemset=ps, number=2, problem=f),
            ProblemsetProblem(problemset=ps, number=3, problem=c),
            ProblemsetProblem(problemset=ps, number=4, problem=g),
            ProblemsetProblem(problemset=ps, number=5, problem=h),
            ProblemsetProblem(problemset=ps, number=6, problem=i),
        ])
        response = self.client.get('/test-problemset/')
        problems = response.context['problems']
        self.assertEqual(problems, [
            {
                'number': 1,
                'description': 'E',
                'ancestors': [{'description': 'A', 'numbers': [1, 2, 3, 4, 5, 6]},
                              {'description': 'B', 'numbers': [1, 2]}],
            },
            {
                'number': 2,
                'description': 'F',
                'ancestors': [],
            },
            {
                'number': 3,
                'description': 'C',
                'ancestors': [],
            },
            {
                'number': 4,
                'description': 'G',
                'ancestors': [{'description': 'D', 'numbers': [4, 5, 6]}],
            },
            {
                'number': 5,
                'description': 'H',
                'ancestors': [],
            },
            {
                'number': 6,
                'description': 'I',
                'ancestors': [],
            },
        ])
