from unittest.mock import Mock, patch

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import TestCase

from cimto.importer.kujawab import (
    KujawabProblemsetImporter, KujawabSiteImporter,
)
from cimto.problems.models import Problem
from cimto.problemset.models import Problemset, ProblemsetProblem
from cimto.tags.models import Tag


class KujawabProblemsetTest(TestCase):
    @patch('requests.get')
    def test_get_data(self, mock_req_get):
        with open('cimto/importer/tests/assets/oskkom17.html') as f:
            m = Mock()
            m.text = f.read()
            mock_req_get.return_value = m
        importer = KujawabProblemsetImporter('https://kujawab.com/OSKKOM17')
        importer.get_data()
        self.assertEqual(importer.title, 'Olimpiade Sains Kota (OSK) 2017 - Komputer')
        self.assertEqual(len(importer.shared_descriptions), 6)
        self.assertEqual(importer.shared_descriptions[5]['begin'], 39)
        self.assertEqual(importer.shared_descriptions[5]['end'], 40)
        self.assertHTMLEqual(
            importer.shared_descriptions[5]['description'],
            '''
            <p><em><strong>Perhatikan potongan kode berikut:</strong></em></p>
            <pre class="prettyprint">var
            n, count : integer;
            begin
            readln(n);
            count := 0;
            repeat
                n := (n * n + 5) mod 23;
            count := count + 1;
            until n = 0;
            end.</pre>
            <p>&nbsp;</p>
            ''',
        )
        self.assertEqual(len(importer.problems), 40)
        self.assertHTMLEqual(
            importer.problems[5],
            '''
            <p>Sebuah brankas dilengkapi dengan kunci kombinasi 4 dijit. Masing-masing dijit memiliki 2 kemungkinan nilai, yaitu 0 dan 1. Ternyata, diketahui diantara 4 dijit itu, hanya 2 dijit yang berfungsi untuk mengunci brankas tersebut. Berapakah banyak percobaan minimal untuk dapat membuka brankas tersebut?</p>
            <p>a. 3</p>
            <p>b. 6</p>
            <p>c. 12</p>
            <p>d. 18</p>
            <p>e. 24</p>
            '''
        )
    
    def test_import_data(self):
        importer = KujawabProblemsetImporter('https://kujawab.com/OSKKOM17', tag_labels=['tag1', 'tag2'])
        importer.title = 'Test Title'
        importer.problems = {
            1: '''
            <p>Example Description</p>
            <p>a. option 1</p>
            <p>b. option 2</p>
            <p>c. option 3</p>
            <p>d. option 4</p>
            <p>e. option 5</p>
            ''',
            2: '''
            <p>Example Description 2</p>
            <p>a. option 1</p>
            <p>b. option 2</p>
            <p>c. option 3</p>
            <p>d. option 4</p>
            <p>e. option 5</p>
            ''',
        }
        importer.shared_descriptions = [{
            'description': '''
            <p>This is a shared description</p>
            ''',
            'begin': 1,
            'end': 2,
        }]
        importer.import_data()
        self.assertEqual(Problemset.objects.count(), 1)
        self.assertEqual(Problem.objects.count(), 3)
        self.assertEqual(ProblemsetProblem.objects.count(), 2)
        problemset = Problemset.objects.first()
        self.assertEqual(problemset.title, importer.title)
        problems = []
        tags = Tag.objects.get_tags(labels=['tag1', 'tag2'])
        for pp in problemset.problem_mapping.all():
            problem = pp.problem
            problems.append(problem)
            self.assertHTMLEqual(importer.problems[pp.number], problem.description)
            self.assertQuerysetEqual(problem.tags.all(), tags, ordered=False)
        self.assertEqual(problems[0].parent, problems[1].parent)
        self.assertHTMLEqual(
            problems[0].parent.description,
            importer.shared_descriptions[0]['description'],
        )
        self.assertQuerysetEqual(problems[0].parent.tags.all(), tags, ordered=False)


class KujawabSiteTest(TestCase):
    @patch('requests.get')
    def test_get_problemset_links(self, mock_req_get):
        with open('cimto/importer/tests/assets/index.html') as f:
            m = Mock()
            m.text = f.read()
            mock_req_get.return_value = m
        cat_problem_num = {
            'Komputer': 26,
            'Matematika': 7,
            'Fisika': 3,
            'Kimia': 1,
            'Biologi': 1,
            'Astronomi': 2,
            'Kebumian': 1,
            'Ekonomi': 7,
            'Geografi': 1,
        }
        importer = KujawabSiteImporter()
        links = importer.get_problemset_links()
        validate_url = URLValidator()
        for key, value in links.items():
            self.assertEqual(len(value), cat_problem_num[key])
            for link in value:
                try:
                    validate_url(link['url'])
                except ValidationError as e:
                    self.fail(e.message)
