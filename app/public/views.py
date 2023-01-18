from django.conf import settings
from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect(to=settings.LOGIN_REDIRECT_URL)
    context = dict(
        title="Market Monitor",
    )
    return render(request=request, template_name="public/index.html", context=context)
