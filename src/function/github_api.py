from typing import Any

import requests
from click import ClickException
import os


def upload_github_release_asset(
    github_owner: str,
    github_repository: str,
    github_release_tag: str,
    asset_name: str,
    asset_path: str,
) -> str:
    github_token = os.environ["GITHUB_TOKEN"]
    release_url = f"https://api.github.com/repos/{github_owner}/{github_repository}/releases/tags/{github_release_tag}"
    release_response = get_github_response_body(release_url)
    upload_url = release_response["upload_url"].split("{")[0]
    upload_url = f"{upload_url}?name={asset_name}"

    with open(asset_path, "rb") as f:
        data = f.read()
    upload_response = requests.post(
        upload_url,
        data=data,
        headers={
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/octet-stream",
            "Authorization": f"Bearer {github_token}",
        },
    )
    if upload_response.status_code == 422:
        raise ClickException(
            f"Failed to upload asset {asset_name} due to existing asset with identical name. {upload_response.content}"
        )
    return upload_response.json()["browser_download_url"]


def get_github_response_body(url: str):
    github_token = os.environ["GITHUB_TOKEN"]
    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
        },
    )
    if response.status_code == 404:
        raise ClickException(
            f"GitHub API responded with 404 not found status code for url '{url}'."
        )
    if response.status_code != 200:
        raise ClickException(
            f"GitHub API responded with non-success HTTP status code: {response.text}'"
        )
    return response.json()


def post_github_response_body(url: str, json: Any):
    github_token = os.environ["GITHUB_TOKEN"]
    response = requests.post(
        url,
        json=json,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {github_token}",
        },
    )
    if response.status_code == 404:
        raise ClickException(
            f"GitHub API responded with 404 not found status code for url '{url}'."
        )
    if response.status_code != 201:
        raise ClickException(
            f"GitHub API responded with non-success HTTP status code: {response.text}'"
        )
    return response.json()
