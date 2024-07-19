import os

import requests
from click import ClickException


def create_originstamp_timestamp(comment: str, hash: str) -> str:
    response = requests.post(
        "https://api.originstamp.com/v4/timestamp/create",
        json={"comment": comment, "hash": hash},
        headers={
            "Content-Type": "application/json",
            "Authorization": os.environ["ORIGINSTAMP_TOKEN"],
            "User-Agent": "GitHub action ember-nexus/action-attest",
        },
    )
    if response.status_code != 200:
        raise ClickException(
            f"Received bad response from Originstamp API: {response.status_code} - {response.content}"
        )
    return f"https://my.originstamp.com/my/timestamps/details/{hash}"
