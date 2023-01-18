import requests  # type: ignore
from authlib.integrations.django_client import OAuth
from django.conf import settings
from jose import jwt

from .models import Token


def fetch_token(name, request):
    return request.user.token.to_dict()


def update_token(
    name: str,
    token: dict,
    refresh_token: str = None,
    access_token: str = None,
    **kwargs,
) -> None:
    if refresh_token:
        stored_token = Token.objects.get(name=name, refresh_token=refresh_token)
    elif access_token:
        stored_token = Token.objects.get(name=name, access_token=access_token)
    else:
        return

    stored_token.update(**token)


def validate_access_token(access_token: str) -> dict:
    """Validate a JWT access token retrieved from the EVE SSO.
    Returns the contents of the validated JWT access token if there are no errors
    """

    # fetch JWKs URL from meta data endpoint
    res = requests.get(settings.SSO_META_DATA_URL)
    res.raise_for_status()
    data = res.json()
    try:
        jwks_uri = data["jwks_uri"]
    except KeyError:
        raise RuntimeError(
            f"Invalid data received from the SSO meta data endpoint: {data}",
        ) from None

    # fetch JWKs from endpoint
    res = requests.get(jwks_uri)
    res.raise_for_status()
    data = res.json()
    try:
        jwk_sets = data["keys"]
    except KeyError:
        raise RuntimeError(
            f"Invalid data received from the the jwks endpoint: {data}",
        ) from None

    # pick the JWK with the requested algorithm
    jwk_set = [item for item in jwk_sets if item["alg"] == settings.JWK_ALGORITHM].pop()

    # try to decode the token and validate it against expected values
    # will raise JWT exceptions if decoding fails or expected values do not match
    return jwt.decode(
        token=access_token,
        key=jwk_set,
        algorithms=jwk_set["alg"],
        issuer=settings.JWK_ISSUERS,
        audience=settings.JWK_AUDIENCE,
    )


oauth = OAuth(
    fetch_token=fetch_token,
    update_token=update_token,
)

eve = oauth.register(
    name="eve",
    server_metadata_url=settings.SSO_META_DATA_URL,
)
