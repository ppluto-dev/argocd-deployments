#!/usr/bin/env python3

# Update the argo application with all live branches from 'ppluto-main'

import argparse
import subprocess
from dataclasses import asdict, dataclass
from typing import List

import oyaml as yaml  # use `oyaml` for preserve the order in original YAML
from get_active_branches_on_pull_request import \
    get_active_branches_on_pull_request

ORIGINAL_VALUES_YAML = """
spec:
  destination:
    server: https://kubernetes.default.svc
  source:
    repoURL: https://github.com/ppluto-dev/argocd-test.git
    targetRevision: HEAD
  applications: []
"""


@dataclass
class Application:
    name: str
    path: str
    namespace: str


def add_all_applications(apps: List[Application], target: str):
    try:
        with open(target, "r") as f:
            data = yaml.safe_load(f)
            # check not valid yaml
            if type(data) == str or not (
                "spec" in data and "applications" in data["spec"]
            ):
                print("Invalid YAML format :", data)
                data = yaml.safe_load(ORIGINAL_VALUES_YAML)
    except FileNotFoundError as e:
        print("File not found", e)
        data = yaml.safe_load(ORIGINAL_VALUES_YAML)

    data["spec"]["applications"] = [asdict(app) for app in apps]
    with open(target, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)

    return data


def get_subdomain_from_branch_name(branch_name: str) -> str:
    subdomain = subprocess.run(
        ["../../subdomain_name_from_git_branch_name.bash", branch_name], # It should works on drone CI
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8")
    return repr(subdomain.strip("\n")).strip("'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="The path of target values.yaml in chart",
    )
    args = parser.parse_args()

    all_branches = get_active_branches_on_pull_request()
    print("active branches on opened pull requests : \n", all_branches)
    
    apps = [
        Application(
            name=get_subdomain_from_branch_name(branch),
            path=f"auto_branch_pushes/{branch}/ppluto-main/overlays/prod/",
            namespace=get_subdomain_from_branch_name(branch),
        )
        for branch in all_branches + ["main"] # add the main branch always working 
    ]

    add_all_applications(apps=apps, target=args.target)
    print("\nComplete an addition of all applications")
