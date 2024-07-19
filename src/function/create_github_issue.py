from .github_api import post_github_response_body


def create_github_issue(
    github_owner: str, github_repository: str, title: str, body: str, labels: list[str]
) -> str:
    response = post_github_response_body(
        f"https://api.github.com/repos/{github_owner}/{github_repository}/issues",
        {"title": title, "body": body, "labels": labels},
    )
    return response["html_url"]
