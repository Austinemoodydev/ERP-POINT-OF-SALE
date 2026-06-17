from .models import UserSession
from django.contrib.sessions.models import Session


def get_client_ip(request):

    x_forwarded_for = request.META.get(
        'HTTP_X_FORWARDED_FOR'
    )

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def logout_other_sessions(user, current):
    """Terminate all sessions for `user` except the `current` session key.

    Deletes server-side session objects and corresponding UserSession records.
    """

    sessions = UserSession.objects.filter(
        user=user).exclude(session_key=current)

    for s in list(sessions):
        Session.objects.filter(session_key=s.session_key).delete()
        s.delete()
