#!/usr/bin/env python3

# This script is supposed to be used only from `make garbage-collect-deployed-prods`.
# Please refer to `Makefile`'s `garbage-collect-deployed-prods` target for what this does.

import argparse
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("prod_branches_directory")
prod_branches_directory = parser.parse_args().prod_branches_directory

print("git fetch --prune")
print(
    subprocess.run("git fetch --prune".split(), stdout=subprocess.PIPE).stdout.decode(
        "utf-8"
    )
)

git_remote_branches_raw = subprocess.run(
    "git branch --remotes".split(), stdout=subprocess.PIPE
).stdout.decode("utf-8")
git_remote_branch_names = []

for line in git_remote_branches_raw.split("\n"):
    if line == "" or line.startswith("  origin/HEAD ->"):
        continue
    assert line.startswith("  origin/")
    git_remote_branch_names.append(line[len("  origin/") :])

print("Live remote branches: \n ", "\n  ".join(git_remote_branch_names))


def should_keep(dir):
    for git_remote_branch_name in git_remote_branch_names:
        git_remote_branch_name += "/"
        if dir.startswith(git_remote_branch_name) or git_remote_branch_name.startswith(
            dir
        ):
            return True
    return False


prod_branch_dirs = []
for rootdir, dirs, files in os.walk(prod_branches_directory):
    for subdir in dirs:
        full_path = os.path.join(rootdir, subdir)
        assert full_path.startswith(prod_branches_directory)
        prod_branch_dirs.append(
            full_path[len(prod_branches_directory) :].lstrip("/") + "/"
        )

for prod_branch_dir in prod_branch_dirs:
    if should_keep(prod_branch_dir):
        continue

    dir_to_remove = os.path.join(prod_branches_directory, prod_branch_dir)
    if os.path.exists(dir_to_remove):
        print("Removing", dir_to_remove)
        shutil.rmtree(dir_to_remove)
