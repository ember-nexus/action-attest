import os
import tempfile

import click
from jinja2 import Template

from ..function.download_github_release import download_github_release
from ..function.create_merkle_tree_from_folder import create_merkle_tree_from_folder
from ..function.create_originstamp_timestamp import create_originstamp_timestamp
from ..function.create_github_issue import create_github_issue
from ..function.github_api import upload_github_release_asset


@click.command()
@click.argument("github-owner")
@click.argument("github-repository")
@click.argument("github-release-tag")
def run(github_owner: str, github_repository: str, github_release_tag: str):
    click.echo("Ember Nexus: Action Attest\n")
    temporary_folder = tempfile.mkdtemp()

    download_github_release(
        github_owner, github_repository, github_release_tag, temporary_folder
    )

    merkle_tree = create_merkle_tree_from_folder(temporary_folder)
    click.echo("Merkle tree of release assets:")
    click.echo(merkle_tree.to_pretty_json())
    click.echo()

    merkle_tree_path = f"{temporary_folder}/merkle_tree.json"
    with open(merkle_tree_path, "w") as file:
        file.write(merkle_tree.to_json())
        file.close()

    asset_url = upload_github_release_asset(
        github_owner,
        github_repository,
        github_release_tag,
        "attest-merkle-tree.json",
        merkle_tree_path,
    )
    click.echo(f"Uploaded merkle tree to {asset_url}\n")

    link_to_originstamp_certificate = create_originstamp_timestamp(
        f"Release {github_release_tag} of {github_owner}/{github_repository}",
        merkle_tree.hash,
    )
    click.echo(f"Initiated Originstamp certificate, available at {link_to_originstamp_certificate}\n")

    link_to_release_page = f"https://github.com/{github_owner}/{github_repository}/releases/tag/{github_release_tag}"

    with open(
        os.path.join(
            os.path.dirname(__file__), "../asset/post_release_issue_body.jinja2"
        )
    ) as file_:
        template = Template(file_.read())

    link_to_github_issue = create_github_issue(
        github_owner,
        github_repository,
        f"Post release tasks for {github_release_tag}",
        template.render(
            link_to_originstamp_certificate=link_to_originstamp_certificate,
            link_to_release_page=link_to_release_page,
            github_release_tag=github_release_tag,
        ),
        ["Post Release"],
    )
    click.echo(f"Created GitHub issue with post release tasks: {link_to_github_issue}")

    pass
