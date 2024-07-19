import re
import requests

from .github_api import get_github_response_body

from click import ClickException, echo


def download_github_release(
    github_owner: str, github_repository: str, github_release_tag: str, folder
):
    validate_github_owner(github_owner)
    validate_github_repository(github_repository)
    validate_github_release_tag(github_release_tag)

    artifacts = get_github_release_artifacts(
        github_owner, github_repository, github_release_tag
    )

    echo("Downloading release artifacts...")
    for filename, url in artifacts:
        echo(f"  Downloading {filename} from {url}")
        download_github_artifact_to_folder(filename, url, folder)
    echo("Downloaded all release artifacts.")
    echo()

    pass


def get_github_release_artifacts(
    github_owner: str, github_repository: str, github_release_tag: str
) -> list[tuple[str, str]]:
    release_artifacts = []

    release_url = f"https://api.github.com/repos/{github_owner}/{github_repository}/releases/tags/{github_release_tag}"
    release_response = get_github_response_body(release_url)
    release_id = release_response["id"]

    # add all custom artifacts from release
    release_artifact_list_url = f"https://api.github.com/repos/{github_owner}/{github_repository}/releases/{release_id}/assets"
    release_artifact_list = get_github_response_body(release_artifact_list_url)

    for release_artifact in release_artifact_list:
        release_artifacts.append(
            (release_artifact["name"], release_artifact["browser_download_url"])
        )

    # add default artifacts from release
    code_zip_url = f"https://github.com/{github_owner}/{github_repository}/archive/refs/tags/{github_release_tag}.zip"
    release_artifacts.append(
        (find_github_code_archive_name(code_zip_url), code_zip_url)
    )

    code_tar_gz_url = f"https://github.com/{github_owner}/{github_repository}/archive/refs/tags/{github_release_tag}.tar.gz"
    release_artifacts.append(
        (find_github_code_archive_name(code_tar_gz_url), code_tar_gz_url)
    )

    # the tarball and zipball offered by the API is not identical to those downloadable from the release page
    # see also https://github.com/orgs/community/discussions/126140
    # release_artifacts.append((find_github_code_archive_name(release_response['tarball_url']), release_response['tarball_url']))
    # release_artifacts.append((find_github_code_archive_name(release_response['zipball_url']), release_response['zipball_url']))

    return release_artifacts


def validate_github_owner(github_owner: str) -> None:
    github_owner_regex = "^[a-zA-Z0-9-]+$"
    if re.fullmatch(github_owner_regex, github_owner) is None:
        raise ClickException(
            f"Argument 'github-owner' does not pass validation. Expected string of type '{ github_owner_regex }', received '{ github_owner }'."
        )


def validate_github_repository(github_repository: str) -> None:
    github_repository_regex = "^[a-zA-Z0-9-_.]+$"
    if re.fullmatch(github_repository_regex, github_repository) is None:
        raise ClickException(
            f"Argument 'github-repository' does not pass validation. Expected string of type '{ github_repository_regex }', received '{ github_repository }'."
        )


def validate_github_release_tag(github_release_tag: str) -> None:
    github_release_tag_regex = "^[a-zA-Z0-9-_.]+$"
    if re.fullmatch(github_release_tag_regex, github_release_tag) is None:
        raise ClickException(
            f"Argument 'github-release-tag' does not pass validation. Expected string of type '{ github_release_tag_regex }', received '{ github_release_tag }'."
        )


def download_github_artifact_to_folder(filename: str, url: str, folder: str) -> None:
    response = requests.get(url, stream=True)
    path = f"{folder}/{filename}"
    with open(path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)


def find_github_code_archive_name(url: str) -> str:
    response_one = requests.head(url)
    if response_one.status_code == 404:
        raise ClickException(
            f"GitHub API responded with 404 not found status code for url '{url}'."
        )
    if response_one.status_code != 302:
        raise ClickException(
            f"GitHub API responded with non-success HTTP status code: {response_one}"
        )

    response_two = requests.head(response_one.headers["location"])
    if response_two.status_code == 404:
        raise ClickException(
            f"GitHub API responded with 404 not found status code for url '{url}'."
        )
    if response_two.status_code != 200:
        raise ClickException(
            f"GitHub API responded with non-success HTTP status code: {response_two}"
        )

    return response_two.headers["content-disposition"].split("filename=")[1]
