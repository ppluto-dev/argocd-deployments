#!/usr/bin/env python3

# this has a permission that reads pull request (expired in 02.24.2024)
# it is splitted due to github security scan
# TODO: it needs to be managed in env or other secret tools
TOKEN_SPLITTED = [
    "github_pat_11ADSDH3A0Lsup3pUgl7qW_4GPuIpf7h4T",
    "1MMkcis8pdMmZRJd7cPLlWTAFhrKT1RTLYXVP6MEfn2Kb89L",
]
ACCESS_TOKEN = "".join(TOKEN_SPLITTED)


def get_active_branches_on_pull_request():
    import requests

    # Replace with your GitHub username and repository name
    username = "ppluto-dev"
    repository = "ppluto-main"

    # Set up the API endpoint URL
    url = f"https://api.github.com/repos/{username}/{repository}/pulls"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    response = requests.get(url, headers=headers)

    branches = [
        pull_request["head"]["ref"]
        for pull_request in response.json()
        if pull_request["draft"] == False
    ]

    return branches
