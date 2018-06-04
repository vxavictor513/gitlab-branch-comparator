import sys, getopt
from configparser import RawConfigParser, NoOptionError
import gitlab

def getSettings():
    masterBranch = 'master'
    featureBranch = 'development'

    # By default only show number of unmerged changes but not commit details
    onlyCommits = False
    showAll = False
    isDebug = False
    
    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:],"m:f:ad",["master-branch=","feature-branch=","only-commits","all","debug"])
            for o, a in opts:
                if o in ("-m", "--master-branch"):
                    masterBranch = a
                elif o in ("-f", "--feature-branch"):
                    featureBranch = a
                elif o == "--only-commits":
                    onlyCommits = True
                elif o in ("-a", "--all"):
                    showAll = True
                elif o in ("-d", "--debug"):
                    isDebug = True
        except getopt.GetoptError:
            print('compare.py -m <master_branch> -f <feature_branch>')
            sys.exit(2)
    return masterBranch, featureBranch, onlyCommits, showAll, isDebug

def getProject(projects, name):
    for proj in projects:
        if proj.name == name: return proj

def printCommit(commit, index):
    title = commit['title']
    author = commit['author_name']
    createdAt = commit['created_at']
    print("{}\t{}".format(index, title))
    print("\t>> created by {} at {}\n".format(author, createdAt))

def main():

    # Read from config.ini
    config = RawConfigParser()
    config.read('config.ini')

    # Read settings
    MASTER_BRANCH, FEATURE_BRANCH, ONLY_COMMITS, SHOW_ALL, IS_DEBUG = getSettings()
    print("\nComparing from '{}' (master) to '{}' (feature)".format(MASTER_BRANCH, FEATURE_BRANCH))

    # Login GitLab
    httpUsername=None
    httpPassword=None
    if (config.has_option('GitLab', 'http_username') and config.has_option('GitLab', 'http_password')):
        httpUsername = config.get('GitLab', 'http_username')
        httpPassword = config.get('GitLab', 'http_password')

    gl = gitlab.Gitlab(
        url=config.get('GitLab', 'url'),
        http_username=httpUsername,
        http_password=httpPassword,
        private_token=config.get('GitLab', 'private_token')
    )
    gl.auth()

    # Get Projects
    targetGroups = config.get('GitLab','project_group').split(',')

    for targetGroup in targetGroups:
        groupName = targetGroup
        group = gl.groups.get(groupName)
        print("\n////////////////////////////////////////")
        print("Accessing group: {}".format(groupName))
        print("////////////////////////////////////////")

        try:
            includedProjects = config.get('project.' + groupName,'included_projects').split(',')
        except NoOptionError:
            includedProjects = []

        if not len(includedProjects) == 0:
            print('\nAssessing projects:\n{}\n'.format(','.join(includedProjects)))
            projectNames = includedProjects
        else:
            try:
                excludedProjects = config.get('project.' + groupName,'excluded_projects').split(',')
            except NoOptionError:
                excludedProjects = []
            if not len(excludedProjects) == 0:
                print("\nExcluded projects:\n{}".format(','.join(excludedProjects)))
            projects = group.projects.list(all=True, order_by='name', sort='asc')
            projectList = ''
            for proj in projects:
                if (proj.name not in excludedProjects):
                    projectList += proj.name
                    projectList += ','
            projectList = projectList.rstrip(',')
            print('\nAssessing projects:\n{}\n'.format(projectList))
            projectNames = projectList.split(',')
            
        unmergedProjects = {}
        for item in projectNames:
            ms = item.strip()
            projects = gl.projects.list(search=ms)
            project = getProject(projects, ms)
            if project is not None:
                result = project.repository_compare(MASTER_BRANCH, FEATURE_BRANCH)
                numberOfUnmergedCommits = len(result['commits'])
                if IS_DEBUG and ((not ONLY_COMMITS) or SHOW_ALL):
                    print("'{}' project has {} unmerged commit(s).".format(ms, numberOfUnmergedCommits))
                if numberOfUnmergedCommits > 0:
                    unmergedProjects.update({ms: numberOfUnmergedCommits})
                if (ONLY_COMMITS or SHOW_ALL) and result['commits']:
                    i = 1
                    print("\nUnmerged commit(s) for '{}'".format(ms))
                    for commit in result['commits']:
                        printCommit(commit, i)
                        i += 1
            else:
                print("\n'{}' project is not found!".format(ms))
        print("")
        if unmergedProjects and not ONLY_COMMITS:
            print("RESULTS: {} project(s) have unmerged changes:".format(len(unmergedProjects)))
            for p in unmergedProjects:
                print("* {} change(s)\t'{}'".format(unmergedProjects[p], p))
        elif not unmergedProjects:
            print("RESULTS: No unmerged changes.")
        print("")

if __name__ == "__main__":
    main()