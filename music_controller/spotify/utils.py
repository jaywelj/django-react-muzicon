from requests import (
    get,
    patch,
    post,
    put,
)


BASE_URL = "https://api.spotify.com/v1/me/"

def execute_spotify_api_request(
    spotify_token,
    endpoint,
    is_post=False,
    is_put=False
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + spotify_token.access_token
    }

    if is_post:
        post(BASE_URL + endpoint, headers=headers)
    
    if is_put:
        put(BASE_URL + endpoint, headers=headers)
    
    response = get(BASE_URL + endpoint, headers=headers)
    try:
        return response.json()
    except Exception:
        return {"Error": "Issue with request"}
