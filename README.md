# gitlab-branch-comparator
A Python 3 script that checks if a feature branch has all changes from master branch in GitLab repository.

## Usage
```
$ python3 compare.py [-m:f:a] [--only-commits]

-m --master-branch      Master branch name
-f --feature-branch     Feature branch name
-a --show-all           Show both summary and unmerged commit details
--only-commits          Only show the unmerged commit details
```