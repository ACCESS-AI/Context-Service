from app.model.core.assignment_context import AssignmentContext
from app.model.core.repository_handler import RepositoryHandler



def test_repository_handler():
    repo_handler = RepositoryHandler('fake_course', 'tests/utils/')
    assigmnent_contexts = repo_handler.get_assignment_contexts()
    assert len(assigmnent_contexts) == 3
    for assignment_context in assigmnent_contexts:
        assert type(assignment_context) == AssignmentContext