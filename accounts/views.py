from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from datetime import timedelta

from .models import LoginHistory, AccountLockout, UserSession
from .utils import get_client_ip, logout_other_sessions


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if account is locked
        if is_locked(username):
            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Account temporarily locked'
                }
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            # Remove lock record after successful login
            AccountLockout.objects.filter(
                username=username
            ).delete()

            login(request, user)

            LoginHistory.objects.create(
                user=user,
                ip_address=get_client_ip(request),
                user_agent=request.META.get(
                    'HTTP_USER_AGENT'
                )
            )

            # Ensure session key exists and record the session
            if not request.session.session_key:
                request.session.create()

            UserSession.objects.create(
                user=user,
                session_key=request.session.session_key,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )

            # Invalidate other sessions for this user
            logout_other_sessions(user, request.session.session_key)
            return redirect('/admin/')

        else:

            lock, created = AccountLockout.objects.get_or_create(
                username=username
            )

            lock.failed_attempts += 1

            if lock.failed_attempts >= 5:

                lock.locked_until = (
                    timezone.now() +
                    timedelta(minutes=15)
                )

            lock.save()

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid username or password'
                }
            )

    return render(
        request,
        'accounts/login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('login')


@login_required
def password_change_view(request):

    if request.method == 'POST':

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        'accounts/password_change.html',
        {
            'form': form
        }
    )


# Create your views here.


def is_locked(username):

    try:

        lock = AccountLockout.objects.get(
            username=username
        )

        if lock.locked_until:

            if lock.locked_until > timezone.now():
                return True

        return False

    except AccountLockout.DoesNotExist:
        return False
