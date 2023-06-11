from django.views.generic.detail import DetailView

from cimto.problemset.models import Problemset


class ProblemsetDetailView(DetailView):
    model = Problemset
    context_object_name = 'problemset'
    template_name = 'cimto/problemset/problemset_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problems'] = []
        ancestor_map = {}
        prev_ancestors = []
        for mapping in self.object.problem_mapping.all():
            # store list of current problem ancestors to be referenced for the next problem
            curr_ancestors = []
            # list of ancestors to be displayed for the current problem
            display_ancestors = []
            ancestor = mapping.problem.parent
            while ancestor:
                if ancestor.id not in ancestor_map:
                    ancestor_map[ancestor.id] = {
                        'description': ancestor.description,
                        'numbers': [],
                    }
                ancestor_dict = ancestor_map[ancestor.id]
                ancestor_dict['numbers'].append(mapping.number)
                if ancestor.id not in prev_ancestors:
                    display_ancestors.insert(0, ancestor_dict)
                curr_ancestors.append(ancestor.id)
                ancestor = ancestor.parent
            context['problems'].append({
                'number': mapping.number,
                'description': mapping.problem.description,
                'ancestors': display_ancestors,
            })
            prev_ancestors = curr_ancestors
        return context
