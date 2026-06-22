from .models import WorkflowStep


def next_step(request):

    request.current_step += 1

    request.save()

    return request
