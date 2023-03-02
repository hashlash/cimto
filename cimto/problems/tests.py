from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cimto.problems.models import Problem

User = get_user_model()


class ProblemTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user',
            password='secret',
        )

    def setUp(self):
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

    def tearDown(self):
        self.token.delete()

    def test_authorized_problem_crud(self):
        # create problem
        data = {
            'title': 'New Problem',
            'description': 'New problem description.',
            'answer_key': 'answer123',
        }
        response = self.client.post(reverse('problem-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['answer_key'], data['answer_key'])
        data = response.data

        # get problem by id
        response = self.client.get(reverse('problem-detail', kwargs={'pk': data['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, data)

        # get all problems
        response = self.client.get(reverse('problem-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(response.content, [data])

        # update (patch) problem
        updated_desc = 'Updated description'
        response = self.client.patch(
            reverse('problem-detail', kwargs={'pk': data['id']}),
            data={'description': updated_desc},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data['description'] = updated_desc
        data['updated_at'] = response.data['updated_at']
        response = self.client.get(reverse('problem-detail', kwargs={'pk': data['id']}))
        self.assertJSONEqual(response.content, data)

        # update (put) problem
        updated_data = {
            'title': 'Updated Problem',
            'description': 'Updated problem description.',
            'answer_key': 'answer345',
        }
        response = self.client.put(
            reverse('problem-detail', kwargs={'pk': data['id']}),
            data=updated_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data.update(updated_data)
        data['updated_at'] = response.data['updated_at']
        response = self.client.get(reverse('problem-detail', kwargs={'pk': data['id']}))
        self.assertJSONEqual(response.content, data)

        # delete problem
        response = self.client.delete(reverse('problem-detail', kwargs={'pk': data['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse('problem-detail', kwargs={'pk': data['id']}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def _test_unauthenticated_problem_creation(self):
        # Current implementation of django-rules returns 403 instead of 401 when no credential is provided.
        # PR: https://github.com/dfunckt/django-rules/pull/175
        # TODO: remove the _ prefix to activate this test when the auth on django-rules is fixed.
        self.client.credentials()
        response = self.client.post(
            reverse('problem-list'),
            {
                'title': 'New Problem',
                'description': 'New problem description.',
                'answer_key': 'answer123',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_problem_modification(self):
        user2 = User.objects.create_user(
            username='user2',
            password='secret',
        )
        problem = Problem.objects.create(
            title='User2 Problem',
            owner=user2,
            description='Problem Description',
            answer_key='answer1234',
        )

        # update (patch) problem
        updated_desc = 'Updated description'
        response = self.client.patch(
            reverse('problem-detail', kwargs={'pk': problem.pk}),
            data={'description': updated_desc},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # update (put) problem
        updated_data = {
            'title': 'Updated Problem',
            'description': 'Updated problem description.',
            'answer_key': 'answer345',
        }
        response = self.client.put(
            reverse('problem-detail', kwargs={'pk': problem.pk}),
            data=updated_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete problem
        response = self.client.delete(reverse('problem-detail', kwargs={'pk': problem.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
