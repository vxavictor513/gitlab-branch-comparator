# gitlab-branch-comparator
A Python 3 script that checks if a feature branch has all changes from master branch in GitLab repository.

## Description
This script uses [`python-gitlab`](https://python-gitlab.readthedocs.io/en/stable/) to access your GitLab repository and compare two specified branches for multiple projects.

_Note: Currently only for GitLab v3 APIs._

## Get Started
### Installation
Install [`python-gitlab`](https://python-gitlab.readthedocs.io/en/stable/).
```
$ sudo pip3 install --upgrade python-gitlab
```

### GitLab Configuration
Configure `config.ini`.
* `url` (string): The URL of the GitLab server
* `email` (string): The user email or login
* `password` (str) – The user password (associated with email/login)
* `http_username` (string): Username for HTTP authentication.
* `http_password` (string): Password for HTTP authentication
* `projects` (string[]): Comma-separated list of project names
```
[GitLab]
url = https://gitlab.com/your-username
email = your-username
password = secretPassword
; http_username = your-username
; http_password = secretPassword
projects = project-A,project-B
```

### Usage
```
$ python3 compare.py [-m:f:a] [--only-commits]

-m --master-branch      Master branch name | default: 'master'
-f --feature-branch     Feature branch name | default: 'development'
-a --show-all           Show both summary and unmerged commit details | default: False
--only-commits          Only show the unmerged commit details | default: False
```
