# gitlab-branch-comparator
A Python 3 script that checks if a feature branch has all changes from master branch in GitLab repository.

## Description
This script uses [`python-gitlab`](https://python-gitlab.readthedocs.io/en/stable/) to access your GitLab repository and compare two specified branches for multiple projects.

## Get Started
### Installation
Install [`python-gitlab`](https://python-gitlab.readthedocs.io/en/stable/).
```
$ sudo pip3 install --upgrade python-gitlab
```

### GitLab Configuration
Configure `config.ini`.

## General Configuration: [GitLab]
* `url` (string): The URL of the GitLab server
* `http_username` (string): Username for Basic HTTP authentication
* `http_password` (string): Password for Basic HTTP authentication
* `private_token` (string): Personal access token with API scope. How to generate: https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token
* `project_group` (string[]): Comma-separated list of group
```
[GitLab]
url = https://gitlab.com/your-username
; http_username = your-username
; http_password = secretPassword
private_token = 8fuaiovn83wf9iwbvai
project_group = group-a,group-b
```

## Group Configuration: [group.group-a]
_Note: Remember to add `group.` as prefix._
* `included_project` (string[]): Comma-separated list of projects to be scanned.
* `excluded_project` (string[]): Comma-separated list of projects to be excluded. Not effective if `included_project` is configured.
```
[group.group-a]
excluded_projects = project-a,project-c

[group.group-b]
included_projects = project-z
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

////////////////////////////////////////
Accessing group: group-a
////////////////////////////////////////

Excluded projects:
project-a, project-c

Assessing projects:
project-b, project-d


RESULTS: 2 project(s) have unmerged changes:
* 3 change(s)   'project-b'
* 1 change(s)   'project-d'


////////////////////////////////////////
Accessing group: group-b
////////////////////////////////////////

Assessing projects:
project-z


RESULTS: No unmerged changes.

```

```
$ python3 compare.py -m master -f development --only-commits

Comparing from 'master' (master) to 'development' (feature)

////////////////////////////////////////
Accessing group: group-a
////////////////////////////////////////

Excluded projects:
project-a, project-c

Assessing projects:
project-b, project-d


Unmerged commit(s) for 'project-b'
1       Updated pom.xml
        >> created by dev-012 at 2017-11-09T11:45:40.000+00:00

2       Added feature YY
        >> created by dev-012 at 2017-11-10T17:04:25.000+00:00

3       Merge branch 'feature-YY' into 'development'
        >> created by dev-007 at 2017-12-04T11:27:32.000+00:00


Unmerged commit(s) for 'project-d'
1       Added feature X
        >> created by dev-007 at 2017-11-09T11:45:40.000+00:00




////////////////////////////////////////
Accessing group: group-b
////////////////////////////////////////

Assessing projects:
project-z


RESULTS: No unmerged changes.

```

### Changelog
## v3 to v4
* Upgraded to support GitLab v4 API. For GitLab v3 API, please use `v3` branch.
* This version should support only GitLab version 10.2 or above, as the program no longer support login using email and password. Instead, please login using private token.
* Added support to scan multiple groups.
* Instead of specifying projects to be scanned, now you can specify either `included_projects` or `excluded_projects` in configuration, for each group. When `included_projects` is specified, program will only scan the listed projects in the group; when `excluded_projects` is specified, program will scan all projects in the group EXCLUDING the listed projects. _NOTE: `included_projects` has precedence over `excluded_projects`._