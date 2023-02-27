#!/usr/bin/env python3

# this has a permission that reads pull request (expired in 02.24.2024)
# TODO: it needs to be managed in env or other secret tools
ACCESS_TOKEN="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"

def get_active_branches_on_pull_request():
    import requests

    # Replace with your GitHub username and repository name
    username = "ppluto-dev"
    repository = "ppluto-main"

    # Replace with the number of the pull request that you want to get the branches for
    pull_request_number = 123

    # Set up the API endpoint URL
    url = f"https://api.github.com/repos/{username}/{repository}/pulls?state=open"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    response = requests.get(url, headers=headers)
    branches = [pull_request["head"]["ref"] for pull_request in response.json() if pull_request["draft"] == False]

    return branches
