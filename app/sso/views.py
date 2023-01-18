from django.conf import settings
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect

from .auth import eve, validate_access_token
from .models import Character, Token
from .tasks import get_public_info


def login(request):
    return eve.authorize_redirect(request, settings.CALLBACK_URL)


@login_required
def logout(request):
    request.user.token.delete()
    logout_user(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def callback(request):
    jwt = eve.authorize_access_token(request)

    jwt_contents = validate_access_token(jwt["access_token"])
    character_id = int(jwt_contents["sub"].split(":")[2])
    character_name = jwt_contents["name"]

    user, user_created = User.objects.get_or_create(
        username=character_name,
    )

    login_user(request, user)

    if user_created:
        Character.objects.create(
            user=user,
            name=character_name,
            id=character_id,
        )

    if hasattr(user, "token"):
        user.token.update(
            access_token=jwt["access_token"],
            refresh_token=jwt["refresh_token"],
            expires_at=jwt["expires_at"],
        )
    else:
        Token.objects.create(
            name="eve",
            token_type=jwt["token_type"],
            access_token=jwt["access_token"],
            refresh_token=jwt["refresh_token"],
            expires_at=jwt["expires_at"],
            user=user,
        )

    get_public_info(request)
    return redirect(to=settings.LOGIN_REDIRECT_URL)
