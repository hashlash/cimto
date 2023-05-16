import re

import requests
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.text import slugify

from cimto.problems.models import Problem
from cimto.problemset.models import Problemset, ProblemsetProblem
from cimto.tags.models import Tag

DEFAULT_USER_USERNAME = 'kujawab'

osn_re = re.compile(
    r'Olimpiade Sains (?:Kota|Provinsi|Nasional) \((?P<stage>OSK|OSP|OSN)\) '
    r'(?P<year>\d+) - (?P<science>\w+)(?: (?P<grade>SMA))?'
)


def osn_repl(m):
    return f"{m['stage']} {m['science']} {m['grade'] or 'SMA'} {m['year']}"


class KujawabProblemsetImporter:
    def __init__(self, url, user=None, tag_labels=None):
        self.url = url
        if user is None:
            User = get_user_model()
            user, _ = User.objects.get_or_create(username='kujawab')
        self.user = user
        if tag_labels is None:
            tag_labels = []
        self.tags = Tag.objects.get_tags(labels=tag_labels, create_missing=True)
        self.problems = {}
        self.shared_descriptions = []

    def get_data(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.title = soup.h3.text.strip()

        for entry in soup.find('div', 'problems').find_all('div', recursive=False):
            if 'problem' in entry['class']:
                number, desc = entry.div.find_all('div', recursive=False)  # div.problem > div.row > div
                self.problems[int(number.text)] = desc.decode_contents().strip()
     
            elif 'extra-description' in entry['class']:
                m = re.search(r'Deskripsi untuk soal nomor\s+(\d+)\s+-\s+(\d+)', str(entry.p))
                number_begin, number_end = m.groups()
                self.shared_descriptions.append({
                    'description': ''.join(map(lambda t: str(t), entry.contents[3:-1])),
                    'begin': int(number_begin),
                    'end': int(number_end),
                })
    
    @transaction.atomic
    def import_data(self):
        problemset = Problemset.objects.create(
            title=self.title,
            slug=slugify(osn_re.sub(osn_repl, self.title)),
            owner=self.user,
        )

        # shared descriptions
        # TODO: change to bulk_create once common versions of SQLite support AutoField
        # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
        problems = []
        for desc in self.shared_descriptions:
            p = Problem(
                title=f"{self.title}: {desc['begin']} - {desc['end']}",
                slug=f"{problemset.slug}-{desc['begin']}-{desc['end']}",
                owner=self.user,
                description=desc['description'],
            )
            p.save()
            p.tags.add(*self.tags)
            problems.append(p)
        parents = {}
        for p, d in zip(problems, self.shared_descriptions):
            for i in range(d['begin'], d['end']+1):
                parents[i] = p

        # problems
        # TODO: change to bulk_create once common versions of SQLite support AutoField
        # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
        problem_tuples = self.problems.items()
        problems = []
        for number, desc in problem_tuples:
            p = Problem(
                title=f"{self.title}: {number}",
                slug=f'{problemset.slug}-{number}',
                owner=self.user,
                parent=parents.get(number, None),
                description=desc,
            )
            p.save()
            p.tags.add(*self.tags)
            problems.append(p)

        # problemset problems
        ProblemsetProblem.objects.bulk_create([
            ProblemsetProblem(
                problemset=problemset,
                number=number,
                problem=problem,
                is_origin=True,
            )
            for (number, _), problem in zip(problem_tuples, problems)
        ])


class KujawabSiteImporter:
    SOURCE_BASE_URL = 'https://kujawab.com/'
    CATEGORY_TAG = {
        'Komputer': 'informatics',
        'Matematika': 'mathematics',
        'Fisika': 'physics',
        'Kimia': 'chemistry',
        'Biologi': 'biology',
        'Astronomi': 'astronomy',
        'Kebumian': 'earth-science',
        'Ekonomi': 'economy',
        'Geografi': 'geography', 
    
    }

    def get_problemset_links(self):
        r = requests.get(self.SOURCE_BASE_URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        categories = (
            soup.body
            .find_all('div', recursive=False)[1]  # .container
            .find_all('div', recursive=False)[2]  # .container-fluid
            .div.div  # .row > .col-sm-8
        )
        return {
            cat.h4.a.text.strip(): {link['href'] for link in cat.table.find_all('a')}
            for cat in categories.find_all('div', recursive=False)
        }
    
    @transaction.atomic
    def import_data(self):
        cat_links = self.get_problemset_links()
        for cat, links in cat_links.items():
            for link in links:
                imp = KujawabProblemsetImporter(
                    link,
                    tag_labels=[self.CATEGORY_TAG[cat]]
                )
                imp.get_data()
                imp.import_data()
