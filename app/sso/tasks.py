from .auth import eve


def get_public_info(request):
    url = f"https://esi.evetech.net/latest/characters/{request.user.character.id}/?datasource=tranquility"
    response = eve.get(url, request=request)
    response.raise_for_status()
    request.user.character.update(response.json())
