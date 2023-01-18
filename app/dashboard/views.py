from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    context = dict(
        title="Dashboard",
    )
    return render(
        request=request,
        template_name="dashboard/index.html",
        context=context,
    )
