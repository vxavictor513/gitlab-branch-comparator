import sys, getopt
from configparser import RawConfigParser
import gitlab

def getSettings():
    masterBranch = 'master'
    featureBranch = 'development'

    # By default only show number of unmerged changes but not commit details
    onlyCommits = False
    showAll = False
    
    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:],"m:f:a",["master-branch=","feature-branch=","only-commits","all"])
            for o, a in opts:
                if o in ("-m", "--master-branch"):
                    masterBranch = a
                elif o in ("-f", "--feature-branch"):
                    featureBranch = a
                elif o == "--only-commits":
                    onlyCommits = True
                elif o in ("-a", "--all"):
                    showAll = True
        except getopt.GetoptError:
            print('compare.py -m <master_branch> -f <feature_branch>')
            sys.exit(2)
    return masterBranch, featureBranch, onlyCommits, showAll

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

    httpUsername=None
    httpPassword=None
    if (config.has_option('GitLab', 'http_username') and config.has_option('GitLab', 'http_password')):
        httpUsername = config.get('GitLab', 'http_username')
        httpPassword = config.get('GitLab', 'http_password')

    gl = gitlab.Gitlab(
        url=config.get('GitLab', 'url'),
        email=config.get('GitLab', 'email'),
        password=config.get('GitLab', 'password'),
        http_username=httpUsername,
        http_password=httpPassword
    )
    gl.auth()

    projectNames = config['GitLab']['projects'].split(',')
    if len(projectNames) == 1 and projectNames[0] is '':
        print("Please configure list of projects in config.ini file.\n")
        return

    MASTER_BRANCH, FEATURE_BRANCH, ONLY_COMMITS, SHOW_ALL = getSettings()
    print("Comparing from {} (master) to {} (feature)".format(MASTER_BRANCH, FEATURE_BRANCH))
    for item in projectNames:
        ms = item.strip()
        projects = gl.projects.list(search=ms)
        project = getProject(projects, ms)
        if project is not None:
            result = project.repository_compare(MASTER_BRANCH, FEATURE_BRANCH)
            if (not ONLY_COMMITS) or SHOW_ALL:
                print("'{}' project has {} unmerged commit(s).".format(ms, len(result['commits'])))
            if (ONLY_COMMITS or SHOW_ALL) and result['commits']:
                i = 1
                print("\nUnmerged commit(s) for '{}'".format(ms))
                for commit in result['commits']:
                    printCommit(commit, i)
                    i += 1
        else:
            print("\n'{}' project is not found!".format(ms))
    print("")

if __name__ == "__main__":
    main()