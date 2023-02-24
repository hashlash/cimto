import rules


@rules.predicate
def is_problem_owner(user, problem):
    return problem.owner == user
