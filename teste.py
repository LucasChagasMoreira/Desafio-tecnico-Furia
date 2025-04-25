import requests

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAL3p0gEAAAAA7eGe1aTSxd1LEG6uSm6yNO6NiXM%3DseH7AlCGtb6vZr9I20GdLTHxZOqoBeHR6bsBVSITJHWK7dS173"
HEADERS = {
    "Authorization": f"Bearer {requests.utils.unquote(BEARER_TOKEN)}",
    "User-Agent": "MyApp/1.0"
}

def get_user_id(username: str):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    r = requests.get(url, headers=HEADERS)
    print("STATUS:", r.status_code)
    print("JSON  :", r.json())
    r.raise_for_status()
    body = r.json()
    if "errors" in body:
        raise RuntimeError("Twitter error: " + str(body["errors"]))
    return body["data"]["id"]

def get_following(user_id: str):
    url = f"https://api.twitter.com/2/users/{user_id}/following"
    r = requests.get(url, headers=HEADERS)
    print("STATUS:", r.status_code)
    print("JSON  :", r.json())
    r.raise_for_status()
    body = r.json()
    if "errors" in body:
        raise RuntimeError("Twitter error: " + str(body["errors"]))
    return body.get("data", [])

if __name__ == "__main__":
    try:
        uid = get_user_id("TwitterDev")
        follows = get_following(uid)
        print(f"Found {len(follows)} follows.")
    except Exception as e:
        print("ERROR:", e)

