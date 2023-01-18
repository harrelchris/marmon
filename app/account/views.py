from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.signals import user_logged_out
from django.shortcuts import redirect, render


@login_required
def delete(request):
    user_logged_out.send(
        sender=request.user.__class__,
        request=request,
        user=request.user,
    )
    request.user.delete()
    request.session.flush()
    request.user = AnonymousUser()
    return redirect(settings.LOGOUT_REDIRECT_URL)


@login_required
def settings_view(request):
    context = dict(
        title="Settings",
    )
    return render(
        request=request,
        template_name="account/settings.html",
        context=context,
    )
