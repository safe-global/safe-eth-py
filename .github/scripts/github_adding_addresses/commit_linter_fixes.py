"""
Commits linter fixes as a single verified commit via the GitHub API.
"""

import os
import subprocess

from github import Github, InputGitTreeElement


def commit_linter_fixes() -> None:
    repo = Github(os.environ["GITHUB_TOKEN"]).get_repo(os.environ["GITHUB_REPOSITORY"])
    branch = os.environ["BRANCH_NAME"]
    files = (
        subprocess.check_output(["git", "diff", "HEAD", "--name-only"])
        .decode()
        .strip()
        .split("\n")
    )

    if not files or not files[0]:
        print("No linter changes to commit.")
        return

    parent = repo.get_branch(branch).commit
    blobs = []
    for f in files:
        with open(f) as fh:
            blobs.append(repo.create_git_blob(fh.read(), "utf-8"))
    tree = repo.create_git_tree(
        [
            InputGitTreeElement(path=f, mode="100644", type="blob", sha=b.sha)
            for f, b in zip(files, blobs)
        ],
        parent.commit.tree,
    )
    commit = repo.create_git_commit("Apply linter fixes", tree, [parent.commit])
    repo.get_git_ref(f"heads/{branch}").edit(commit.sha)
    print(f"Committed linter fixes: {commit.sha}")


if __name__ == "__main__":
    commit_linter_fixes()
