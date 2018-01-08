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
* `http_username` (string): Username for Basic HTTP authentication.
* `http_password` (string): Password for Basic HTTP authentication
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
$ python3 compare.py [-m:f:ad] [--master-branch --feature-branch --show-all --only-commits --debug]

-m --master-branch      Master branch name | default: 'master'
-f --feature-branch     Feature branch name | default: 'development'
-a --show-all           Show both summary and unmerged commit details | default: False
--only-commits          Only show the unmerged commit details | default: False
-d --debug              Enable debug mode
```

### Sample Results
```
$ python3 compare.py -m master -f development

Comparing from 'master' (master) to 'development' (feature)

RESULTS: 2 project(s) have unmerged changes:
* 3 change(s)   'project-A'
* 1 change(s)   'project-B'

```

```
$ python3 compare.py -m master -f development --only-commits

Comparing from 'master' (master) to 'development' (feature)

Unmerged commit(s) for 'project-A'
1       Updated pom.xml
        >> created by dev-012 at 2017-11-09T11:45:40.000+00:00

2       Added feature YY
        >> created by dev-012 at 2017-11-10T17:04:25.000+00:00

3       Merge branch 'feature-YY' into 'development'
        >> created by dev-007 at 2017-12-04T11:27:32.000+00:00

Unmerged commit(s) for 'project-B'
1       Added feature X
        >> created by dev-007 at 2017-11-09T11:45:40.000+00:00

```
